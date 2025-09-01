from collections.abc import Iterable

# Simple shadowcasting stub (v0 we fake FOV as a diamond radius; upgrade later).


def visible_points(cx: int, cy: int, radius: int, w: int, h: int) -> Iterable[tuple[int, int]]:
    for y in range(cy - radius, cy + radius + 1):
        for x in range(cx - radius, cx + radius + 1):
            if 0 <= x < w and 0 <= y < h and abs(x - cx) + abs(y - cy) <= radius:
                yield x, y
