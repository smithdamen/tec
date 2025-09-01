import asyncio
import json
from dataclasses import dataclass, field

import tcod
import tcod.event

from tec.client.keymap import map_key_to_action
from tec.settings import SETTINGS
from tec.shared.actions import Action, ActLogin, ActMove


@dataclass
class ViewModel:
    x: int = 0
    y: int = 0
    tiles: list[str] = field(default_factory=list)  # rows of width w
    w: int = SETTINGS.view_w
    h: int = SETTINGS.view_h
    log: list[str] = field(default_factory=list)
    speed: float = 1.0
    energy: float = 0.0
    aps: float = 1.0
    eta: float = 0.0


class Client:
    def __init__(self) -> None:
        self.reader: asyncio.StreamReader
        self.writer: asyncio.StreamWriter
        self.vm = ViewModel()
        self.hold_move: tuple[int, int] | None = None

    async def connect(self, host: str, port: int, name: str) -> None:
        self.reader, self.writer = await asyncio.open_connection(host, port)
        await self.send(ActLogin("LOGIN", name))
        asyncio.create_task(self.recv_loop())

    async def send(self, action: Action) -> None:
        self.writer.write((json.dumps(action.__dict__) + "\n").encode())
        await self.writer.drain()

    async def recv_loop(self) -> None:
        while True:
            line = await self.reader.readline()
            if not line:
                break
            msg = json.loads(line.decode("utf-8"))
            mtype = msg.get("type")
            if mtype == "POS":
                self.vm.x = int(msg["x"])
                self.vm.y = int(msg["y"])
            elif mtype == "VIEW":
                self.vm.w = int(msg["w"])
                self.vm.h = int(msg["h"])
                tiles_str = msg["tiles"]
                self.vm.tiles = [
                    tiles_str[i : i + self.vm.w] for i in range(0, len(tiles_str), self.vm.w)
                ]
            elif mtype == "LOG":
                self.vm.log.append(str(msg["text"]))
                self.vm.log = self.vm.log[-6:]
            elif mtype == "STATS":
                self.vm.speed = float(msg["speed"])
                self.vm.energy = float(msg["energy"])
                self.vm.aps = float(msg["aps"])
                self.vm.eta = float(msg["eta"])

    def draw(self, console: tcod.console.Console) -> None:
        console.clear()
        # map viewport (top-left with 1-char padding)
        ox = 1
        oy = 1
        for row_i, row in enumerate(self.vm.tiles):
            for col_i, ch in enumerate(row):
                console.print(ox + col_i, oy + row_i, ch)
        # side status bar
        sx = SETTINGS.view_w + 3
        console.print(sx, 1, f"POS: {self.vm.x},{self.vm.y}")
        console.print(sx, 2, f"Speed: {self.vm.speed:.2f}")
        console.print(sx, 3, f"APS: {self.vm.aps:.2f}")
        console.print(sx, 4, f"Energy: {self.vm.energy:.2f}")
        console.print(sx, 5, f"ETA: {self.vm.eta:.2f}s")
        # bottom log
        height = console.height
        for i, line in enumerate(self.vm.log[-6:]):
            console.print(1, height - 7 + i, line)
        console.print(
            1,
            height - 1,
            "Arrows/vi/numpad to move, '.'/5 wait, ESC quit.",
        )

    async def run(self) -> None:
        tileset = tcod.tileset.get_default()
        with tcod.context.new(
            width=100,
            height=40,
            tileset=tileset,
            title="TEC",
            vsync=True,
        ) as context:
            console = tcod.Console(100, 40, order="F")
            while True:
                self.draw(console)
                context.present(console)
                for event in tcod.event.get():
                    if isinstance(event, tcod.event.Quit):
                        return
                    if isinstance(event, tcod.event.KeyDown):
                        if event.sym == tcod.event.K_ESCAPE:
                            return
                        # try symbolic name (e.g., "UP", "LEFT")
                        sym_name = getattr(event.sym, "name", None)
                        action = None
                        if sym_name:
                            action = map_key_to_action(sym_name)
                        # fallback to printable unicode (e.g., "h", ".")
                        if not action:
                            u = getattr(event, "unicode", "")
                            if u:
                                action = map_key_to_action(u)
                        if action:
                            await self.send(action)
                            if isinstance(action, ActMove):
                                dx, dy = action.dx, action.dy
                                if dx or dy:
                                    self.hold_move = (dx, dy)
                    if isinstance(event, tcod.event.KeyUp):
                        self.hold_move = None
                # hold-to-move: send repeated MOVE every 120ms
                if self.hold_move:
                    await asyncio.sleep(0.12)
                    dx, dy = self.hold_move
                    await self.send(ActMove("MOVE", dx, dy))
                else:
                    await asyncio.sleep(0.01)


async def main() -> None:
    client = Client()
    await client.connect("127.0.0.1", 4000, "player")
    await client.run()


if __name__ == "__main__":
    asyncio.run(main())
