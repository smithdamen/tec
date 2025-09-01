from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Actor:
    energy: float = 0.0
    speed: float = 1.0  # energy per tick


@dataclass
class PlayerTag:
    name: str


@dataclass
class Needs:
    hunger: float = 0.0  # increases over time
    thirst: float = 0.0
    exposure: float = 0.0
