# Ticks, Energy, Speed
- Tick = 100ms (10Hz).
- Actor.speed = energy per tick. Action.cost consumes energy.
- actions/sec = speed * tick_rate_hz / cost
- ETA (sec) = max(0, (cost - energy)) / (speed * tick_rate_hz)
