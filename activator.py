from resolver import CharmResolver
from executor import EffectExecutor

resolver = CharmResolver()
executor = EffectExecutor()

#============================================================
#CHARM ACTIVATION
#============================================================

def activate_charms(
    owned_charms,
    game_state
    ):

    available = [

        d for d in owned_charms

        if d['cooldown'] == 0
    ]

    if not available:

        print(
            "No charms available."
        )

        return

    print(
        "\n🎯 Activating ALL available charms...\n"
    )

    for d in available:

        charm = d['charm']

        print(
            f"✓ {charm.name} activated!"
        )

        effects = resolver.resolve(charm)

        for effect in effects:

            executor.execute(
                effect,
                d,
                game_state
            )

        d['uses'] += 1
        d['activations_this_round'] += 1

        # ----------------------------------------------------
        # APPLY COOLDOWN
        # ----------------------------------------------------

        if charm.cooldown_rounds > 0:

            d['cooldown'] = (
                charm.cooldown_rounds
            )