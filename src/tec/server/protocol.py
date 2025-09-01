import json

from tec.settings import SETTINGS
from tec.shared.components import Actor

Coord = tuple[int, int]


def ev_welcome(msg: str) -> bytes:
    return (json.dumps({"type": "WELCOME", "msg": msg}) + "\n").encode()


def ev_pos(x: int, y: int) -> bytes:
    return (json.dumps({"type": "POS", "x": x, "y": y}) + "\n").encode()


def ev_view(
    x0: int,
    y0: int,
    tiles: list[list[bool]],
    visible: set[Coord] | None = None,
    explored: set[Coord] | None = None,
) -> bytes:
    """Build a VIEW snapshot.

    Args:
        x0, y0: top-left of the view window.
        tiles: world grid; True=floor (.), False=wall (#).
        visible: cells visible right now (mask for 'tiles' field). If None, no masking.
        explored: cells the player has seen before (makes 'mem' bits 1).

    Fields:
        - tiles: string of length w*h where NOT visible is ' ' (space).
        - base:  string of length w*h of the true glyphs ('.' or '#'), unmasked.
        - mem:   string of length w*h; '1' if explored else '0'.
    """
    w, h = SETTINGS.view_w, SETTINGS.view_h
    masked: list[str] = []
    base: list[str] = []
    mem: list[str] = []

    for yy in range(y0, y0 + h):
        for xx in range(x0, x0 + w):
            inside = 0 <= yy < len(tiles) and 0 <= xx < len(tiles[0])
            if not inside:
                masked.append(" ")
                base.append(" ")
                mem.append("0")
                continue

            ch = "." if tiles[yy][xx] else "#"
            base.append(ch)

            vis = (visible is None) or ((xx, yy) in visible)
            masked.append(ch if vis else " ")

            was_seen = (explored is not None) and ((xx, yy) in explored)
            mem.append("1" if was_seen else ("1" if vis else "0"))

    payload = {
        "type": "VIEW",
        "x": x0,
        "y": y0,
        "w": w,
        "h": h,
        "tiles": "".join(masked),
        "base": "".join(base),
        "mem": "".join(mem),
    }
    return (json.dumps(payload) + "\n").encode()


def ev_stats(speed: float, energy: float, aps: float, eta: float) -> bytes:
    payload = {
        "type": "STATS",
        "speed": speed,
        "energy": energy,
        "aps": aps,
        "eta": eta,
    }
    return (json.dumps(payload) + "\n").encode()


def derive_stats(actor: Actor, move_cost: float) -> dict[str, float]:
    aps = actor.speed * SETTINGS.tick_rate_hz / move_cost
    eta = max(0.0, (move_cost - actor.energy) / (actor.speed * SETTINGS.tick_rate_hz))
    return {"speed": actor.speed, "energy": actor.energy, "aps": aps, "eta": eta}
