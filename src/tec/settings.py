from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
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
