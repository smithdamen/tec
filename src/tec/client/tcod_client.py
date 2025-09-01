import asyncio
import json
from dataclasses import dataclass, field
from pathlib import Path

import tcod
import tcod.event

from tec.client.keymap import map_key_to_action
from tec.settings import SETTINGS
from tec.shared.actions import Action, ActLogin, ActMove

RIGHT_PANEL_W = 24
LOG_H = 6

# Key repeat tuning
INITIAL_REPEAT_DELAY = 0.25  # seconds before repeats begin
REPEAT_INTERVAL = 0.12  # seconds between repeats once repeating


@dataclass
class ViewModel:
    x: int = 0
    y: int = 0
    vx0: int = 0
    vy0: int = 0
    w: int = SETTINGS.view_w
    h: int = SETTINGS.view_h
    tiles: list[str] = field(default_factory=list)
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
        # Hold-to-move state
        self.hold_move: tuple[int, int] | None = None
        self.hold_since: float | None = None
        self.last_repeat_at: float | None = None

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
                self.vm.vx0 = int(msg["x"])
                self.vm.vy0 = int(msg["y"])
                self.vm.w = int(msg["w"])
                self.vm.h = int(msg["h"])
                tiles_str = msg["tiles"]
                self.vm.tiles = [
                    tiles_str[i : i + self.vm.w] for i in range(0, len(tiles_str), self.vm.w)
                ]
            elif mtype == "LOG":
                self.vm.log.append(str(msg["text"]))
                self.vm.log = self.vm.log[-LOG_H:]
            elif mtype == "STATS":
                self.vm.speed = float(msg["speed"])
                self.vm.energy = float(msg["energy"])
                self.vm.aps = float(msg["aps"])
                self.vm.eta = float(msg["eta"])

    # ---------- Drawing helpers ----------
    @staticmethod
    def _draw_hline(console: tcod.console.Console, x: int, y: int, w: int, ch: str = "-") -> None:
        for i in range(w):
            console.print(x + i, y, ch)

    @staticmethod
    def _draw_vline(console: tcod.console.Console, x: int, y: int, h: int, ch: str = "|") -> None:
        for i in range(h):
            console.print(x, y + i, ch)

    def _draw_box(self, console: tcod.console.Console, x: int, y: int, w: int, h: int) -> None:
        console.print(x, y, "+")
        console.print(x + w - 1, y, "+")
        console.print(x, y + h - 1, "+")
        console.print(x + w - 1, y + h - 1, "+")
        self._draw_hline(console, x + 1, y, w - 2, "-")
        self._draw_hline(console, x + 1, y + h - 1, w - 2, "-")
        self._draw_vline(console, x, y + 1, h - 2, "|")
        self._draw_vline(console, x + w - 1, y + 1, h - 2, "|")

    def _load_tileset(self) -> tcod.tileset.Tileset:
        candidates = [
            Path("DejaVuSansMono.ttf"),
            Path("/usr/share/fonts/TTF/DejaVuSansMono.ttf"),
            Path("/usr/share/fonts/TTF/DejaVuSansMonoNerdFontMono.ttf"),
        ]
        for path in candidates:
            if path.exists():
                return tcod.tileset.load_truetype_font(str(path), 16, 16)
        raise RuntimeError(
            "Could not locate a TrueType font for tcod.\n"
            "Install 'ttf-dejavu' or edit _load_tileset() with a local monospace TTF path."
        )

    def draw(self, console: tcod.console.Console) -> None:
        console.clear()

        W = console.width
        H = console.height

        # Outer border
        self._draw_box(console, 0, 0, W, H)

        # Inner usable area
        inner_x = 1
        inner_y = 1
        inner_w = W - 2
        inner_h = H - 2

        # Layout
        map_w = inner_w - RIGHT_PANEL_W - 1
        map_h = inner_h - LOG_H - 1

        sep_x = inner_x + map_w
        log_y = inner_y + map_h

        # Separators
        self._draw_vline(console, sep_x, inner_y, map_h + 1, "|")
        self._draw_hline(console, inner_x, log_y, inner_w, "-")

        # Map area
        map_x0 = inner_x
        map_y0 = inner_y
        max_rows = min(self.vm.h, map_h)
        max_cols = min(self.vm.w, map_w)
        for row_i in range(max_rows):
            row = self.vm.tiles[row_i] if row_i < len(self.vm.tiles) else ""
            row = (row[:max_cols]).ljust(max_cols, "#")
            for col_i, ch in enumerate(row):
                console.print(map_x0 + col_i, map_y0 + row_i, ch)

        # Player '@' relative to view origin
        rx = self.vm.x - self.vm.vx0
        ry = self.vm.y - self.vm.vy0
        if 0 <= rx < max_cols and 0 <= ry < max_rows:
            console.print(map_x0 + rx, map_y0 + ry, "@")

        # Right panel
        panel_x0 = sep_x + 1
        line = 0

        def pl(text: str) -> None:
            nonlocal line
            console.print(panel_x0, inner_y + line, text)
            line += 1

        pl(f"POS: {self.vm.x},{self.vm.y}")
        pl(f"Speed: {self.vm.speed:.2f}")
        pl(f"APS: {self.vm.aps:.2f}")
        pl(f"Energy: {self.vm.energy:.2f}")
        pl(f"ETA: {self.vm.eta:.2f}s")

        # Log
        for i, text in enumerate(self.vm.log[-LOG_H:]):
            console.print(inner_x, log_y + 1 + i, text)

        console.print(inner_x, H - 1, " Arrows/vi/numpad move  '.'/5 wait  ESC quit ")

    async def run(self) -> None:
        tileset = self._load_tileset()
        with tcod.context.new(
            width=100,
            height=40,
            tileset=tileset,
            title="TEC",
            vsync=True,
        ) as context:
            console = tcod.Console(100, 40, order="F")
            loop = asyncio.get_running_loop()
            while True:
                self.draw(console)
                context.present(console)

                # --- Input processing ---
                for event in tcod.event.get():
                    if isinstance(event, tcod.event.Quit):
                        return
                    if isinstance(event, tcod.event.KeyDown):
                        if event.sym == tcod.event.K_ESCAPE:
                            return

                        is_repeat = bool(getattr(event, "repeat", False))
                        sym_name = getattr(event.sym, "name", None)
                        action = None
                        if sym_name:
                            action = map_key_to_action(sym_name)
                        if not action:
                            u = getattr(event, "unicode", "")
                            if u:
                                action = map_key_to_action(u)

                        if action and not is_repeat:
                            # Send one immediate step on first press
                            await self.send(action)
                            # Start hold tracking for possible repeats
                            if isinstance(action, ActMove):
                                dx, dy = action.dx, action.dy
                                if dx or dy:
                                    self.hold_move = (dx, dy)
                                    self.hold_since = loop.time()
                                    self.last_repeat_at = None

                    if isinstance(event, tcod.event.KeyUp):
                        # Stop repeating
                        self.hold_move = None
                        self.hold_since = None
                        self.last_repeat_at = None

                # --- Deterministic key repeat (after initial delay) ---
                if self.hold_move and self.hold_since is not None:
                    now = loop.time()
                    # Only start repeating after an initial delay
                    if now - self.hold_since >= INITIAL_REPEAT_DELAY:
                        if (
                            self.last_repeat_at is None
                            or (now - self.last_repeat_at) >= REPEAT_INTERVAL
                        ):
                            dx, dy = self.hold_move
                            await self.send(ActMove("MOVE", dx, dy))
                            self.last_repeat_at = now

                # Keep the loop responsive
                await asyncio.sleep(0.01)


async def main() -> None:
    client = Client()
    await client.connect("127.0.0.1", 4000, "player")
    await client.run()


if __name__ == "__main__":
    asyncio.run(main())
