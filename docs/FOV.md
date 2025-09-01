# Field of View (FOV)

## Problem
Reveal only what the actor could plausibly see, without leaking information to clients.

## Algorithm
- **Symmetric Shadowcasting**, Euclidean cutoff (rounded circle).
- We sweep 8 octants. For each we scan rows outward, tracking a slope interval `[start,end]` which remains unobstructed. Opaque cells shrink the interval for deeper rows, producing shadows behind walls.
- We mark **blocking cells visible** when hit, so walls at the edge of sight appear.

## Integration
- Server computes `visible = shadowcast(px, py, radius, is_opaque)`.
- `ev_view(origin, tiles, visible, explored)` builds three strings:
  - `tiles`: masked by current visibility.
  - `base`: ground truth glyphs (unmasked).
  - `mem`: explored mask (1 = has been seen).
- Client renders:
  - visible: `.`/`#`
  - explored-but-not-visible: dim ASCII (`,` for floor, `%` for wall)
  - unknown: space.

## Dynamic radius
- Ambient factor from a sine day/night (`SETTINGS.day_seconds`) maps between `fov_night` and `fov_day`.
- Future modifiers: carried lights, indoors, weather.

## Why server-side?
- Prevents map/ESP cheats; keeps view consistent across clients.
