from tec.shared.components import Position


def try_move(pos: Position, dx: int, dy: int, tiles: list[list[bool]]) -> None:
    nx, ny = pos.x + dx, pos.y + dy
    if 0 <= ny < len(tiles) and 0 <= nx < len(tiles[0]) and tiles[ny][nx]:
        pos.x, pos.y = nx, ny
