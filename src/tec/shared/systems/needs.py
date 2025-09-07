"""Simple needs progression updated each tick."""

from tec.shared.components import Actor, Needs

# Very simple v0: tick needs slowly so we can visualize in HUD later.


def tick_needs(needs: Needs, actor: Actor) -> None:
    """Increase survival needs a small amount each tick.

    Args:
        needs: Needs component to mutate (hunger/thirst).
        actor: Actor providing speed/energy context if needed.

    Notes:
        Tuning is intentionally conservative until a full needs system lands.
    """
    needs.hunger += 0.001
    needs.thirst += 0.002
    needs.exposure += 0.0005
