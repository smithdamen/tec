"""Movement system utilities."""

from tec.shared.components import Position


def try_move(pos: Position, dx: int, dy: int, tiles: list[list[bool]]) -> None:
    """Attempt to move an entity by (dx, dy) if the target tile is walkable.

    Args:
        pos: Mutable position component to update.
        dx: Delta x in tiles (-1, 0, +1).
        dy: Delta y in tiles (-1, 0, +1).
        tiles: World tile grid; True=floor, False=wall.

    Notes:
        Does nothing if the target is out of bounds or a wall.
    """
    nx, ny = pos.x + dx, pos.y + dy
    if 0 <= ny < len(tiles) and 0 <= nx < len(tiles[0]) and tiles[ny][nx]:
        pos.x, pos.y = nx, ny
