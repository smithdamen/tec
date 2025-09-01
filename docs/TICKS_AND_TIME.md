# Ticks, Energy, and Time

## Tick loop
- Server runs at `SETTINGS.tick_rate_hz` (default 10 Hz).
- Each tick:
  - `Simulation.time_s += tick_len`.
  - Actors: `energy += speed`.
  - If queue has an action and `energy >= cost`, resolve the action and deduct cost.

## Costs & speed
- Movement cost: `MOVE_COST` (shared constant).
- Waiting cost: `WAIT_COST`.
- Derived stats:
  - `APS` (actions/sec) = `speed * tick_rate_hz / MOVE_COST`.
  - `ETA` (sec until next action) = max(0, `(MOVE_COST - energy) / (speed * tick_rate_hz)`).

## Day/night
- `SETTINGS.day_seconds` controls a simple sine-curve daylight factor `[0..1]`.
- FOV radius lerps from `fov_night` to `fov_day` using this factor.
- Future: weather, biome, indoors → modifiers to ambient factor.

## Input cadence
- Client sends one MOVE on first press, then repeats after `INITIAL_REPEAT_DELAY` with `REPEAT_INTERVAL`. OS repeats are ignored.
