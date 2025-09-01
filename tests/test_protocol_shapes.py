import json

from tec.server.protocol import ev_pos, ev_view


def test_ev_pos_shape() -> None:
    msg = json.loads(ev_pos(1, 2).decode())
    assert msg["type"] == "POS"
    assert msg["x"] == 1 and msg["y"] == 2


def test_ev_view_shape_and_size() -> None:
    tiles = [
        [True, False, True],
        [False, True, False],
    ]
    msg = json.loads(ev_view(0, 0, tiles, visible=None, explored=set()).decode())
    assert msg["type"] == "VIEW"
    assert set(msg.keys()) == {"type", "x", "y", "w", "h", "tiles", "base", "mem"}
    w, h = msg["w"], msg["h"]
    for key in ("tiles", "base", "mem"):
        assert isinstance(msg[key], str)
        assert len(msg[key]) == w * h
