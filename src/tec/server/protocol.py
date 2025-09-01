import json

from tec.settings import SETTINGS
from tec.shared.components import Actor


def ev_welcome(msg: str) -> bytes:
    return (json.dumps({"type": "WELCOME", "msg": msg}) + "\n").encode()


def ev_pos(x: int, y: int) -> bytes:
    return (json.dumps({"type": "POS", "x": x, "y": y}) + "\n").encode()


def ev_view(x: int, y: int, tiles: list[list[bool]]) -> bytes:
    w, h = SETTINGS.view_w, SETTINGS.view_h
    x0 = x - w // 2
    y0 = y - h // 2
    chars: list[str] = []
    for yy in range(y0, y0 + h):
        for xx in range(x0, x0 + w):
            inside = 0 <= yy < len(tiles) and 0 <= xx < len(tiles[0])
            c = "." if (inside and tiles[yy][xx]) else "#"
            chars.append(c)
    payload = {
        "type": "VIEW",
        "x": x0,
        "y": y0,
        "w": w,
        "h": h,
        "tiles": "".join(chars),
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
