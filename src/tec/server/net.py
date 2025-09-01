import asyncio
import json
from typing import Any

from tec.server.protocol import derive_stats, ev_pos, ev_stats, ev_view, ev_welcome
from tec.server.sim import Simulation
from tec.settings import SETTINGS
from tec.shared.actions import MOVE_COST
from tec.shared.components import Actor, Position


class JsonServer:
    def __init__(self, sim: Simulation) -> None:
        self.sim = sim
        self.sessions: dict[asyncio.StreamWriter, int] = {}

    async def handle_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        eid = self.sim.spawn_player()
        self.sessions[writer] = eid
        writer.write(ev_welcome("Welcome to TEC (prototype)."))
        await writer.drain()

        # initial snapshot
        pos = self.sim.world.get(Position)[eid]
        actor = self.sim.world.get(Actor)[eid]
        writer.write(ev_pos(pos.x, pos.y))
        writer.write(ev_view(pos.x, pos.y, self.sim.tiles))
        stats = derive_stats(actor, MOVE_COST)
        writer.write(ev_stats(stats["speed"], stats["energy"], stats["aps"], stats["eta"]))
        await writer.drain()

        # periodic snapshot pump
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
            writer.close()
            await writer.wait_closed()

    async def _snapshot_pump(self, writer: asyncio.StreamWriter, eid: int) -> None:
        """Keep client view and pos in sync even when they didn't press a key."""
        try:
            while writer in self.sessions:
                pos = self.sim.world.get(Position)[eid]
                # IMPORTANT: send POS and VIEW together, in that order.
                writer.write(ev_pos(pos.x, pos.y))
                writer.write(ev_view(pos.x, pos.y, self.sim.tiles))
                await writer.drain()
                await asyncio.sleep(0.1)
        except Exception:
            # Client disconnected or writer broken; let handle_client clean up.
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

        # Send a quick snapshot right after input (still pre-tick, but consistent)
        pos = self.sim.world.get(Position)[eid]
        actor = self.sim.world.get(Actor)[eid]
        writer.write(ev_pos(pos.x, pos.y))
        writer.write(ev_view(pos.x, pos.y, self.sim.tiles))
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
