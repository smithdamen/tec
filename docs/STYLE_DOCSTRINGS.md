# TEC Docstring & Comment Style

**Docstrings** explain *what* a module/class/function does and *how to call it*.
**Inline comments** explain *why* the code is doing something non-obvious.

- **Convention:** PEP 257 + Google style sections.
- **Audience:** New contributors learning the engine (server-authoritative tick loop, JSONL protocol, FOV, terminal client).
- **Keep it practical:** Focus on intent, invariants, units, and examples.

## Module docstrings
- 1–3 sentence summary
- Key concepts (bullets)
- Invariants / coordinate system / threading/network notes (as relevant)

## Function/method docstrings
- One-line summary
- **Args:** names, types, units (e.g., `radius: int (tiles)`)
- **Returns:** types and meaning
- **Raises:** expected exceptions (ValueError, ProtocolError, etc.)
- **Example:** small, copyable usage if non-obvious

## Inline comments
- Prefer *why* over *what*
- Cross-reference ADRs when a design decision influences code

### Examples

```python
def compute_fov(origin: tuple[int, int], radius: int, occluders: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """Compute visible tiles using a Euclidean radius.

    Args:
        origin: (x, y) world-tile coordinates of the viewer; (0, 0) is top-left.
        radius: Maximum visible distance in tiles before occlusion.
        occluders: Set of blocking tiles (walls).

    Returns:
        Set of (x, y) tiles visible from `origin`.

    Raises:
        ValueError: If `radius` < 0.
    """
    # Why: Using Euclidean radius keeps circles visually smooth in ASCII.
    ...
