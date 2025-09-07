"""ECS-style components shared by the server and client.

Coordinates are integer tile positions with (0, 0) at the top-left of world space.
Units:
- Tiles for positions and distances.
- Seconds for time; ticks derived from Settings.tick_rate_hz.
"""

from dataclasses import dataclass


@dataclass
class Position:
    """Tile-space position.

    Attributes:
        x: Column index (0-based).
        y: Row index (0-based).
    """

    x: int
    y: int


@dataclass
class Actor:
    """Actor stats used by the simulation tick.

    Attributes:
        energy: Accumulated action energy (consumed by moves/waits).
        speed: Energy gained per tick (higher = acts more often).
    """

    energy: float = 0.0
    speed: float = 1.0  # energy per tick


@dataclass
class PlayerTag:
    """Tag component identifying a player-controlled entity.

    Attributes:
        name: Player display name.
    """

    name: str


@dataclass
class Needs:
    """Simple survival needs that increase over time.

    Attributes:
        hunger: Increases gradually; 0..∞ (clamped for UI later).
        thirst: Increases gradually; 0..∞ (clamped for UI later).
    """

    hunger: float = 0.0  # increases over time
    thirst: float = 0.0
    exposure: float = 0.0
