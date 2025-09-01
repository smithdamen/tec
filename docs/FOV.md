# Field of View (FOV)

## Model
- World grid: `tiles[y][x]` → `True = floor (transparent)`, `False = wall (opaque)`.
- Player FOV radius: `SETTINGS.fov_radius` (Chebyshev distance, i.e., king moves).

## Algorithm
We use **Symmetric Shadowcasting**:

- Sweep 8 octants around the origin `(px, py)`.
- For each octant, iterate rows at increasing distance (1..radius).
- Maintain a visible slope interval `[start, end]` for that row.
- When an opaque cell segment is encountered, shrink the interval for deeper rows
  by recursing with a new `[start, right_slope]` or `[left_slope, end]`.

This creates a smooth, natural FOV that respects walls.

## Integration
- `tec.shared.fov.shadowcast(px, py, radius, is_opaque) -> set[(x,y)]`.
- `ev_view(..., visible=...)` blanks any tile not in the `visible` set.
- The server computes FOV on each snapshot to keep `VIEW` and `POS` consistent.

## Future
- **Memory (explored)**: retain last seen tiles and draw them dimmed.
- **Lighting**: multiple light sources; combine FOV with light intensity.
- **Performance**: cache per-player FOV when neither pos nor map changes.
