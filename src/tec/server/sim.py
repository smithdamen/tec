"""Server-authoritative simulation loop and helpers.

Simulation advances at a fixed tick rate. Inputs are queued per-entity and
applied at the start of each tick. Network I/O is handled elsewhere; this
module owns world state and game rules.
"""

from collections import deque
from dataclasses import dataclass, field

from tec.settings import SETTINGS
from tec.shared.actions import MOVE_COST, WAIT_COST
from tec.shared.components import Actor, Needs, Position
from tec.shared.mapgen import generate_map
from tec.shared.systems.movement import try_move
from tec.shared.systems.needs import tick_needs
from tec.shared.world import EID, World

Action = tuple[str, tuple[int, int] | None]  # ("move",(dx,dy)) or ("wait", None)


def _new_map() -> list[list[bool]]:
    return generate_map(SETTINGS.map_width, SETTINGS.map_height, SETTINGS.seed)


@dataclass
class Simulation:
    """World state plus tick-advancement routines.

    Attributes:
        world: ECS-style storage for components.
        tiles: 2D map of walkable tiles; True=floor, False=wall.
        time_s: Simulated seconds since world start.
        tick_len: Seconds per tick (1 / Settings.tick_rate_hz).
    """

    world: World = field(default_factory=World)
    tiles: list[list[bool]] = field(default_factory=_new_map)
    action_queues: dict[EID, deque[Action]] = field(default_factory=dict)
    tick_len: float = field(default=1.0 / SETTINGS.tick_rate_hz)
    time_s: float = 0.0  # simulated seconds since world start

    def ensure_queue(self, eid: EID) -> deque[Action]:
        """Return (and create if missing) the action queue for an entity."""
        return self.action_queues.setdefault(eid, deque())

    def spawn_player(self) -> EID:
        """Create a new player entity at world center and return its id."""
        eid = self.world.create()
        self.world.add(eid, Position(SETTINGS.map_width // 2, SETTINGS.map_height // 2))
        self.world.add(eid, Actor())
        self.world.add(eid, Needs())
        self.ensure_queue(eid)
        return eid

    def enqueue_move(self, eid: EID, dx: int, dy: int) -> None:
        """Queue a relative move for an entity.

        Args:
            eid: Entity id to move.
            dx: Delta x in tiles (-1, 0, +1).
            dy: Delta y in tiles (-1, 0, +1).
        """
        self.ensure_queue(eid).append(("move", (dx, dy)))

    def enqueue_wait(self, eid: EID) -> None:
        """Queue a no-op action (advance time and accrue energy)."""
        self.ensure_queue(eid).append(("wait", None))

    def tick(self) -> None:
        """Advance the simulation by one tick.

        Steps:
            1) Increase `time_s` by `tick_len`.
            2) For each entity with queued input, apply one action.
            3) Update any systems that progress every tick (e.g., needs).
        """
        self.time_s += self.tick_len

        actors = self.world.get(Actor)
        positions = self.world.get(Position)
        needz = self.world.get(Needs)
        for eid, act in list(actors.items()):
            act.energy += act.speed
            q = self.action_queues.get(eid)
            if not q:
                continue
            kind, payload = q[0]  # peek
            cost = MOVE_COST if kind == "move" else WAIT_COST
            if act.energy < cost:
                continue
            q.popleft()
            if kind == "move" and payload is not None:
                dx, dy = payload
                try_move(positions[eid], dx, dy, self.tiles)
            act.energy -= cost
            if eid in needz:
                tick_needs(needz[eid], act)
