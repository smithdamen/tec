import asyncio
import json
import math
from typing import Any

from tec.server.protocol import derive_stats, ev_pos, ev_stats, ev_view, ev_welcome
from tec.server.sim import Simulation
from tec.settings import SETTINGS
from tec.shared.actions import MOVE_COST
from tec.shared.components import Actor, Position
from tec.shared.fov import shadowcast


class JsonServer:
    def __init__(self, sim: Simulation) -> None:
        self.sim = sim
        self.sessions: dict[asyncio.StreamWriter, int] = {}
        self.explored: dict[int, set[tuple[int, int]]] = {}  # per-entity explored cells

    # ---------- helpers ----------

    def _ambient_factor(self) -> float:
        """Return ambient light factor in [0,1] based on time of day."""
        if SETTINGS.day_seconds <= 0:
            return 1.0
        phase = (self.sim.time_s % SETTINGS.day_seconds) / SETTINGS.day_seconds  # 0..1
        # Day peaks at factor=1.0 mid-day, night dips to ~0.2 (tweakable)
        return 0.6 + 0.4 * math.sin(2 * math.pi * (phase - 0.25))  # shift so noon at sin=+1

    def _effective_radius(self, eid: int) -> int:
        amb = self._ambient_factor()
        base = round(SETTINGS.fov_night + (SETTINGS.fov_day - SETTINGS.fov_night) * amb)
        # TODO: add carried light sources, e.g., torch_bonus
        torch_bonus = 0
        return max(1, base + torch_bonus)

    def _compute_visible(self, px: int, py: int, radius: int) -> set[tuple[int, int]]:
        tiles = self.sim.tiles

        def is_opaque(x: int, y: int) -> bool:
            if y < 0 or y >= len(tiles) or x < 0 or x >= len(tiles[0]):
                return True
            return not tiles[y][x]

        return shadowcast(px, py, radius, is_opaque)

    def _view_origin(self, px: int, py: int) -> tuple[int, int]:
        w, h = SETTINGS.view_w, SETTINGS.view_h
        map_h = len(self.sim.tiles)
        map_w = len(self.sim.tiles[0]) if map_h else 0
        vx0 = px - w // 2
        vy0 = py - h // 2
        vx0 = max(0, min(vx0, max(0, map_w - w)))
        vy0 = max(0, min(vy0, max(0, map_h - h)))
        return vx0, vy0

    # ---------- protocol ----------

    async def handle_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        eid = self.sim.spawn_player()
        self.sessions[writer] = eid
        self.explored[eid] = set()
        writer.write(ev_welcome("Welcome to TEC (prototype)."))
        await writer.drain()

        # initial snapshot
        pos = self.sim.world.get(Position)[eid]
        actor = self.sim.world.get(Actor)[eid]
        radius = self._effective_radius(eid)
        vis = self._compute_visible(pos.x, pos.y, radius)
        self.explored[eid].update(vis)
        vx0, vy0 = self._view_origin(pos.x, pos.y)
        writer.write(ev_pos(pos.x, pos.y))
        writer.write(ev_view(vx0, vy0, self.sim.tiles, vis, self.explored[eid]))
        stats = derive_stats(actor, MOVE_COST)
        writer.write(ev_stats(stats["speed"], stats["energy"], stats["aps"], stats["eta"]))
        await writer.drain()

        asyncio.create_task(self._snapshot_pump(writer, eid))

        try:
            while not reader.at_eof():
                line = await reader.readline()
                if not line:
                    break
                try:
                    msg: dict[str, Any] = json.loads(line.decode("utf-8"))
                except Exception:
                    continue
                await self.dispatch(msg, writer, eid)
        finally:
            self.sessions.pop(writer, None)
            self.explored.pop(eid, None)
            writer.close()
            await writer.wait_closed()

    async def _snapshot_pump(self, writer: asyncio.StreamWriter, eid: int) -> None:
        """Keep client snapshots fresh even without input."""
        try:
            while writer in self.sessions:
                pos = self.sim.world.get(Position)[eid]
                radius = self._effective_radius(eid)
                vis = self._compute_visible(pos.x, pos.y, radius)
                self.explored[eid].update(vis)
                vx0, vy0 = self._view_origin(pos.x, pos.y)
                writer.write(ev_pos(pos.x, pos.y))
                writer.write(ev_view(vx0, vy0, self.sim.tiles, vis, self.explored[eid]))
                await writer.drain()
                await asyncio.sleep(0.1)
        except Exception:
            pass

    async def dispatch(
        self,
        msg: dict[str, Any],
        writer: asyncio.StreamWriter,
        eid: int,
    ) -> None:
        mtype = msg.get("type")
        if mtype == "MOVE":
            dx = int(msg.get("dx", 0))
            dy = int(msg.get("dy", 0))
            self.sim.enqueue_move(eid, dx, dy)
        elif mtype == "WAIT":
            self.sim.enqueue_wait(eid)
        elif mtype == "LOGIN":
            pass
        else:
            pass

        pos = self.sim.world.get(Position)[eid]
        actor = self.sim.world.get(Actor)[eid]
        radius = self._effective_radius(eid)
        vis = self._compute_visible(pos.x, pos.y, radius)
        self.explored[eid].update(vis)
        vx0, vy0 = self._view_origin(pos.x, pos.y)
        writer.write(ev_pos(pos.x, pos.y))
        writer.write(ev_view(vx0, vy0, self.sim.tiles, vis, self.explored[eid]))
        stats = derive_stats(actor, MOVE_COST)
        writer.write(ev_stats(stats["speed"], stats["energy"], stats["aps"], stats["eta"]))
        await writer.drain()

    async def start(self) -> None:
        server = await asyncio.start_server(
            self.handle_client,
            SETTINGS.listen_host,
            SETTINGS.listen_port,
        )
        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets or [])
        print(f"Server listening on {addrs}")
        async with server:
            await server.serve_forever()
