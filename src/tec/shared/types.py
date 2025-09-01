from typing import Literal, TypedDict

# JSON message shapes for clarity and mypy checking


class MsgWelcome(TypedDict):
    type: Literal["WELCOME"]
    msg: str


class MsgPos(TypedDict):
    type: Literal["POS"]
    x: int
    y: int


class MsgView(TypedDict):
    type: Literal["VIEW"]
    x: int
    y: int
    w: int
    h: int
    tiles: str  # row-major string of '.' and '#'


class MsgLog(TypedDict):
    type: Literal["LOG"]
    text: str


class MsgStats(TypedDict):
    type: Literal["STATS"]
    speed: float
    energy: float
    aps: float
    eta: float
