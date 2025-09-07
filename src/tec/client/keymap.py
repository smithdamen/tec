"""Keyboard mapping for roguelike input.

Supported movement keys:
- Arrow keys
- Vi keys: h j k l (plus y/u/b/n diagonals if enabled)
- Numpad (if available in the terminal)
"""

from tec.shared.actions import Action, ActMove, ActWait

VIM_DIRS = {
    "h": (-1, 0),
    "j": (0, 1),
    "k": (0, -1),
    "l": (1, 0),
    "y": (-1, -1),
    "u": (1, -1),
    "b": (-1, 1),
    "n": (1, 1),
}

ARROWS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

NUMPAD = {
    "KP_8": (0, -1),
    "KP_2": (0, 1),
    "KP_4": (-1, 0),
    "KP_6": (1, 0),
    "KP_7": (-1, -1),
    "KP_9": (1, -1),
    "KP_1": (-1, 1),
    "KP_3": (1, 1),
    "KP_5": (0, 0),
}


def map_key_to_action(key: str) -> Action | None:
    """Translate a normalized key name to an Action.

    We accept upper-case special key names (ARROWS/NUMPAD),
    and lower-case characters for vim keys / '.' wait.
    """
    key_upper = key.upper()
    if key_upper in ARROWS:
        dx, dy = ARROWS[key_upper]
        return ActMove("MOVE", dx, dy)

    if key_upper in NUMPAD:
        dx, dy = NUMPAD[key_upper]
        if (dx, dy) == (0, 0):
            return ActWait("WAIT")
        return ActMove("MOVE", dx, dy)

    # Fall back to lower-case for vim keys and '.'
    key_lower = key.lower()
    if key_lower in VIM_DIRS:
        dx, dy = VIM_DIRS[key_lower]
        return ActMove("MOVE", dx, dy)

    if key_lower == ".":
        return ActWait("WAIT")

    return None
