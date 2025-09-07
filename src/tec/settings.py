"""Global engine settings shared by server and client.

Centralizes knobs like tick rate and world dimensions so tests and gameplay
can agree on consistent values. Import from this module rather than hard-coding.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Immutable configuration values used across the engine.

    Attributes:
        tick_rate_hz: Simulation ticks per second (Hz).
        map_width: World width in tiles.
        map_height: World height in tiles.
    """

    tick_rate_hz: int = 10
    map_width: int = 100
    map_height: int = 40
    seed: int = 1337
    listen_host: str = "127.0.0.1"  # change to 0.0.0.0 to accept LAN
    listen_port: int = 4000

    # viewport size
    view_w: int = 73  # server-sent viewport window width (odd number)
    view_h: int = 31  # height (odd number)

    # field of view distance
    fov_radius: int = 8

    # FOV baselines (Euclidean radius)
    fov_day: int = 9
    fov_night: int = 4

    # simple day/night cycle for now: number of seconds per full day
    day_seconds: int = 300  # 5 minutes for testing purposes


SETTINGS = Settings()
