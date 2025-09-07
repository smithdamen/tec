r"""JSONL wire protocol helpers.

All messages are UTF-8 JSON objects terminated by a newline (b"\n").
Unknown keys MUST be ignored by clients for forward compatibility.

Message types (examples):
- WELCOME: {"type":"WELCOME","msg":"..."}
- POS: {"type":"POS","x":10,"y":5}
- VIEW: {"type":"VIEW","x":0,"y":0,"w":80,"h":45,
         "tiles":"....##....", "base":"....##....", "mem":"0000111100"}
- STATS: {"type":"STATS","speed":1.0,"energy":0.4,"aps":0.5,"eta":3.2}
"""

from __future__ import annotations

import json
from typing import Any

from tec.settings import SETTINGS
from tec.shared.components import Actor


def ev_welcome(msg: str) -> bytes:
    """Build a server→client WELCOME event.

    Args:
        msg: Human-friendly text to show once on connect.

    Returns:
        Newline-terminated JSON bytes representing the message.
    """
    return (json.dumps({"type": "WELCOME", "msg": msg}) + "\n").encode()


def ev_pos(x: int, y: int) -> bytes:
    """Build a server→client POS event for the player's position.

    Args:
        x: Player x coordinate in tiles.
        y: Player y coordinate in tiles.

    Returns:
        Newline-terminated JSON bytes.
    """
    return (json.dumps({"type": "POS", "x": x, "y": y}) + "\n").encode()


def _encode_tile(
    is_floor: bool,
    wx: int,
    wy: int,
    mask: bool,
    visible: set[tuple[int, int]],
    explored: set[tuple[int, int]],
) -> str:
    """Return a single-character glyph for a world tile.

    Glyphs:
        Visible: '.' for floor, '#' for wall.
        Explored-only (not currently visible): ',' for floor, '%' for wall.
        Unseen & unexplored: ' ' (space).
    """
    if (not mask) or ((wx, wy) in visible):
        return "." if is_floor else "#"
    if (wx, wy) in explored:
        return "," if is_floor else "%"
    return " "


def _build_base_str(tiles: list[list[bool]]) -> str:
    """Return unmasked '.'/'#' map (row-major) as a single string."""
    chars: list[str] = []
    for row in tiles:
        for is_floor in row:
            chars.append("." if is_floor else "#")
    return "".join(chars)


def _build_mem_str(w: int, h: int, x0: int, y0: int, explored: set[tuple[int, int]]) -> str:
    """Return memory string (row-major): '1' if explored tile else '0'."""
    chars: list[str] = []
    for r in range(h):
        wy = y0 + r
        for c in range(w):
            wx = x0 + c
            chars.append("1" if (wx, wy) in explored else "0")
    return "".join(chars)


def ev_view(
    x0: int,
    y0: int,
    tiles: list[list[bool]],
    visible: set[tuple[int, int]] | None = None,
    explored: set[tuple[int, int]] | None = None,
) -> bytes:
    """Build a VIEW event containing a rectangular viewport.

    Encodes the viewport as row-major strings:
    - tiles: masked glyphs ('.','#',',','%',' ')
    - base: unmasked '.'/'#' floor/wall map
    - mem: '1' where explored, '0' otherwise

    Args:
        x0: World-space x of the top-left tile of the viewport.
        y0: World-space y of the top-left tile of the viewport.
        tiles: Row-major 2D array of booleans; True=floor, False=wall.
        visible: Set of world (x, y) currently visible. If None, no masking
            is applied (all tiles rendered as visible glyphs).
        explored: Set of world (x, y) previously explored (dim glyphs / mem).

    Returns:
        Newline-terminated JSON bytes encoding the viewport payload.
    """
    h = len(tiles)
    w = len(tiles[0]) if h else 0

    vis = visible or set()
    exp = explored or set()
    mask = visible is not None  # only mask when visibility set is provided

    # tiles: possibly masked glyphs
    glyphs: list[str] = []
    for r in range(h):
        wy = y0 + r
        row = tiles[r]
        for c in range(w):
            wx = x0 + c
            is_floor = row[c]
            glyphs.append(_encode_tile(is_floor, wx, wy, mask, vis, exp))
    tiles_str = "".join(glyphs)

    # base: always full '.'/'#' map
    base_str = _build_base_str(tiles)

    # mem: per-tile explored mask ('1' or '0')
    mem_str = _build_mem_str(w, h, x0, y0, exp)

    payload: dict[str, Any] = {
        "type": "VIEW",
        "x": x0,
        "y": y0,
        "w": w,
        "h": h,
        "tiles": tiles_str,
        "base": base_str,
        "mem": mem_str,
    }
    return (json.dumps(payload) + "\n").encode()


def ev_stats(speed: float, energy: float, aps: float, eta: float) -> bytes:
    """Build a STATS event for the sidebar.

    Args:
        speed: Energy gained per tick (actor speed).
        energy: Current accumulated action energy.
        aps: Actions per second at current speed/cost.
        eta: Estimated seconds until the next action is available.

    Returns:
        Newline-terminated JSON bytes.
    """
    payload = {"type": "STATS", "speed": speed, "energy": energy, "aps": aps, "eta": eta}
    return (json.dumps(payload) + "\n").encode()


def derive_stats(actor: Actor, move_cost: float) -> dict[str, float]:
    """Compute sidebar stats derived from an actor and a move cost.

    Args:
        actor: Actor component with `speed` and `energy`.
        move_cost: Energy cost of a single tile move.

    Returns:
        Dict with keys: "speed", "energy", "aps", "eta".
    """
    tick_rate = SETTINGS.tick_rate_hz
    aps = actor.speed * tick_rate / move_cost if move_cost > 0 else 0.0
    # Seconds until enough energy to perform one move.
    denom = actor.speed * tick_rate
    eta = 0.0 if denom <= 0 else max(0.0, (move_cost - actor.energy) / denom)
    return {"speed": actor.speed, "energy": actor.energy, "aps": aps, "eta": eta}
