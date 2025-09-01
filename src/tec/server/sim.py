import time
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
    world: World = field(default_factory=World)
    tiles: list[list[bool]] = field(default_factory=_new_map)
    action_queues: dict[EID, deque[Action]] = field(default_factory=dict)
    tick_len: float = field(default=1.0 / SETTINGS.tick_rate_hz)

    def ensure_queue(self, eid: EID) -> deque[Action]:
        return self.action_queues.setdefault(eid, deque())

    def spawn_player(self) -> EID:
        eid = self.world.create()
        self.world.add(eid, Position(SETTINGS.map_width // 2, SETTINGS.map_height // 2))
        self.world.add(eid, Actor())
        self.world.add(eid, Needs())
        self.ensure_queue(eid)
        return eid

    def enqueue_move(self, eid: EID, dx: int, dy: int) -> None:
        self.ensure_queue(eid).append(("move", (dx, dy)))

    def enqueue_wait(self, eid: EID) -> None:
        self.ensure_queue(eid).append(("wait", None))

    def tick(self) -> None:
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

    def run_forever(self) -> None:
        next_time = time.perf_counter()
        while True:
            now = time.perf_counter()
            if now >= next_time:
                self.tick()
                next_time += self.tick_len
            remain = next_time - time.perf_counter()
            if remain > 0:
                time.sleep(min(remain, 0.01))
