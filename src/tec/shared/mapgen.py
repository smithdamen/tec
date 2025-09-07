"""Tiny map generation helpers for building a walkable tile grid.

Tiles are booleans where True=floor (walkable) and False=wall (blocks).
"""

import random

# True = floor, False = wall


def generate_map(width: int, height: int, seed: int) -> list[list[bool]]:
    """Return a width×height boolean grid seeded by `seed`.

    Args:
        width: Number of columns.
        height: Number of rows.
        seed: RNG seed for deterministic maps in tests.

    Returns:
        Row-major 2D array where True=floor and False=wall.
    """
    rng = random.Random(seed)
    tiles = [[False for _ in range(width)] for _ in range(height)]
    x, y = width // 2, height // 2
    tiles[y][x] = True
    for _ in range(width * height * 3):
        dx, dy = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        x = max(1, min(width - 2, x + dx))
        y = max(1, min(height - 2, y + dy))
        tiles[y][x] = True
        if rng.random() < 0.015:
            rw, rh = rng.randint(3, 7), rng.randint(3, 5)
            for yy in range(max(1, y - rh // 2), min(height - 1, y + rh // 2 + 1)):
                for xx in range(max(1, x - rw // 2), min(width - 1, x + rw // 2 + 1)):
                    tiles[yy][xx] = True
    return tiles
