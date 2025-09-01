from tec.shared.components import Actor, Needs

# Very simple v0: tick needs slowly so we can visualize in HUD later.


def tick_needs(needs: Needs, actor: Actor) -> None:
    # Increase needs a tiny bit each action window; tune later.
    needs.hunger += 0.001
    needs.thirst += 0.002
    needs.exposure += 0.0005
