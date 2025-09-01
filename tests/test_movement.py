from tec.shared.components import Actor, Position
from tec.shared.systems.movement import try_move
from tec.shared.world import World


def test_try_move_blocks_walls() -> None:
    w = World()
    e = w.create()
    w.add(e, Position(1, 1))
    w.add(e, Actor())
    tiles = [
        [False, False, False],
        [False, True, False],
        [False, False, False],
    ]
    p = w.get(Position)[e]
    try_move(p, 1, 0, tiles)  # into wall (should not move)
    assert (p.x, p.y) == (1, 1)
    try_move(p, 0, 1, tiles)  # into wall (should not move)
    assert (p.x, p.y) == (1, 1)
