from __future__ import annotations

from collections.abc import Callable

Coord = tuple[int, int]
OpaqueFn = Callable[[int, int], bool]  # (x, y) -> True if this cell BLOCKS light


def shadowcast(px: int, py: int, radius: int, is_opaque: OpaqueFn) -> set[Coord]:
    """Symmetric Shadowcasting with a Euclidean cutoff (rounded FOV).

    The blocking cells themselves are considered visible.
    """
    visible: set[Coord] = {(px, py)}

    octants = (
        (+1, 0, 0, -1),  # NNE
        (0, +1, +1, 0),  # ENE
        (0, +1, -1, 0),  # ESE
        (+1, 0, 0, +1),  # SSE
        (-1, 0, 0, +1),  # SSW
        (0, -1, -1, 0),  # WSW
        (0, -1, +1, 0),  # WNW
        (-1, 0, 0, -1),  # NNW
    )
    for octant in octants:
        _cast_octant(px, py, radius, is_opaque, octant, visible)
    return visible


def _within_euclid(px: int, py: int, wx: int, wy: int, r: int) -> bool:
    dx = wx - px
    dy = wy - py
    return (dx * dx + dy * dy) <= (r * r)


def _cast_octant(
    px: int,
    py: int,
    radius: int,
    is_opaque: OpaqueFn,
    octant: tuple[int, int, int, int],
    out: set[Coord],
) -> None:
    xx, xy, yx, yy = octant
    start_slope = -1.0
    end_slope = 1.0

    for row in range(1, radius + 1):
        if start_slope > end_slope:
            break

        col_start = int(round(row * start_slope))
        col_end = int(round(row * end_slope))
        prev_blocked = False

        for col in range(col_start, col_end + 1):
            wx = px + col * xx + row * xy
            wy = py + col * yx + row * yy

            if not _within_euclid(px, py, wx, wy, radius):
                continue

            left_slope = (col - 0.5) / (row + 0.0)
            right_slope = (col + 0.5) / (row + 0.0)

            blocked = is_opaque(wx, wy)

            # Mark visible if within the current interval (even if blocked).
            if right_slope >= start_slope and left_slope <= end_slope:
                out.add((wx, wy))

            if prev_blocked:
                if not blocked:
                    start_slope = left_slope
                    prev_blocked = False
            else:
                if blocked:
                    _cast_deeper(
                        px,
                        py,
                        row + 1,
                        radius,
                        is_opaque,
                        (xx, xy, yx, yy),
                        start_slope,
                        right_slope,
                        out,
                    )
                    prev_blocked = True
                    start_slope = right_slope

        if prev_blocked:
            break


def _cast_deeper(
    px: int,
    py: int,
    row: int,
    radius: int,
    is_opaque: OpaqueFn,
    octant: tuple[int, int, int, int],
    start_slope: float,
    end_slope: float,
    out: set[Coord],
) -> None:
    xx, xy, yx, yy = octant

    for r in range(row, radius + 1):
        if start_slope > end_slope:
            break

        col_start = int(round(r * start_slope))
        col_end = int(round(r * end_slope))
        prev_blocked = False
        cur_start = start_slope

        for col in range(col_start, col_end + 1):
            wx = px + col * xx + r * xy
            wy = py + col * yx + r * yy

            if not _within_euclid(px, py, wx, wy, radius):
                continue

            left_slope = (col - 0.5) / (r + 0.0)
            right_slope = (col + 0.5) / (r + 0.0)

            blocked = is_opaque(wx, wy)

            if right_slope >= start_slope and left_slope <= end_slope:
                out.add((wx, wy))

            if prev_blocked:
                if not blocked:
                    cur_start = left_slope
                    prev_blocked = False
            else:
                if blocked:
                    _cast_deeper(
                        px, py, r + 1, radius, is_opaque, octant, cur_start, right_slope, out
                    )
                    prev_blocked = True
                    cur_start = right_slope

        if prev_blocked:
            break
