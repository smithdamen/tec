from dataclasses import dataclass
from typing import Literal


@dataclass
class ActLogin:
    type: Literal["LOGIN"]
    name: str


@dataclass
class ActMove:
    type: Literal["MOVE"]
    dx: int
    dy: int


@dataclass
class ActWait:
    type: Literal["WAIT"]


Action = ActLogin | ActMove | ActWait

# Action costs (server-side authoritative semantics)
MOVE_COST = 1.0
WAIT_COST = 1.0
