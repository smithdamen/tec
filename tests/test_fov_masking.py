import json
from collections.abc import Callable

from tec.server.protocol import ev_view
from tec.shared.fov import shadowcast


def _is_opaque_from_tiles(tiles: list[list[bool]]) -> Callable[[int, int], bool]:
    def f(x: int, y: int) -> bool:
        if y < 0 or y >= len(tiles) or x < 0 or x >= len(tiles[0]):
            return True
        return not tiles[y][x]

    return f


def test_fov_masks_unseen_cells() -> None:
    # 5x5 room with a vertical wall in the middle (x==2).
    # True=floor, False=wall
    tiles = [
        [True, True, False, True, True],
        [True, True, False, True, True],
        [True, True, False, True, True],
        [True, True, False, True, True],
        [True, True, False, True, True],
    ]
    px, py = 1, 2  # left side of the wall
    vis = shadowcast(px, py, radius=8, is_opaque=_is_opaque_from_tiles(tiles))

    # Build a VIEW covering the whole map
    msg = json.loads(ev_view(0, 0, tiles, vis).decode())
    s = msg["tiles"]
    w = msg["w"]
    rows = [s[i : i + w] for i in range(0, len(s), w)]

    # Player side (x <= 1) should be visible floor; the wall at x==2 should be visible '#'.
    for y in range(5):
        assert rows[y][0] == "." and rows[y][1] == "."
        assert rows[y][2] == "#"  # wall is visible from the left

    # On the player's own row, straight behind the wall must be hidden (can't see through).
    assert rows[py][3] == " " and rows[py][4] == " "
