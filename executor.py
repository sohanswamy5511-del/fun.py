#============================================================
#EXECUTOR
#============================================================

from effects import EffectType

class EffectExecutor:

    def __init__(self):

        self.handlers = {

            EffectType.LUCK:
                self.apply_luck,

            EffectType.EXTRA_SPIN:
                self.apply_extra_spin,

            EffectType.WEIGHT_ACTIVE:
                self.apply_weight_active,

            EffectType.ADD_SYMBOL_MULT:
                self.apply_symbol_mult,

            EffectType.ADD_PATTERN_MULT:
                self.apply_pattern_mult,

            EffectType.ADD_REPETITION:
                self.apply_repetition,

            EffectType.ADD_CHAIN:
                self.apply_chain,

            EffectType.ADD_RECHARGE:
                self.apply_recharge,

            EffectType.GOLD_MODIFIER:
                self.apply_gold,
        }

    # ========================================================
    # MAIN EXECUTION
    # ========================================================

    def execute(self, effect, charm_data, game_state):

        handler = self.handlers.get(effect.type)

        if not handler:

            print(f"⚠ Unknown effect: {effect.type}")
            return

        handler(effect, charm_data, game_state)

    # ========================================================
    # LUCK
    # ========================================================

    def apply_luck(
        self,
        effect,
        charm_data,
        game_state
    ):

        game_state['pending_luck'] += effect.amount

        print(f"  ✓ +{effect.amount} luck")

    # ========================================================
    # EXTRA SPIN
    # ========================================================

    def apply_extra_spin(
        self,
        effect,
        charm_data,
        game_state
    ):

        game_state['spins_left'] += effect.amount

        print(f"  ✓ +{effect.amount} spins")

    # ========================================================
    # WEIGHT ACTIVE
    # ========================================================

    def apply_weight_active(
        self,
        effect,
        charm_data,
        game_state
    ):

        target_cls = effect.target

        bonuses = game_state['active_bonuses']

        increase = calculate_weight_increase(target_cls)

        if charm_data['activations_this_round'] == 0:

            bonuses[target_cls] = (
                bonuses.get(
                    target_cls,
                    getattr(target_cls, "weight", 1)
                ) + increase
            )

            charm_data['last_increase'] = increase

        else:

            increase = charm_data['last_increase'] * 0.9

            bonuses[target_cls] += increase

            charm_data['last_increase'] = increase

        print(
            f"  ✓ {target_cls.__name__} "
            f"weight +{increase:.1f}"
        )

    # ========================================================
    # SYMBOL MULT
    # ========================================================

    def apply_symbol_mult(
        self,
        effect,
        charm_data,
        game_state
    ):

        game_state['symbols_mult'] += effect.amount

        print(
            f"  ✓ symbols mult +{effect.amount}"
        )

    # ========================================================
    # PATTERN MULT
    # ========================================================

    def apply_pattern_mult(
        self,
        effect,
        charm_data,
        game_state
    ):

        game_state['patterns_mult'] += effect.amount

        print(
            f"  ✓ patterns mult +{effect.amount}"
        )

    # ========================================================
    # REPETITION
    # ========================================================

    def apply_repetition(
        self,
        effect,
        charm_data,
        game_state
    ):

        game_state['repetition_targets'].append(
            effect.target
        )

        print(
            "  ✓ repetition modifier added"
        )

    # ========================================================
    # CHAIN
    # ========================================================

    def apply_chain(
        self,
        effect,
        charm_data,
        game_state
    ):

        game_state['chain_targets'].append(
            effect.target
        )

        print(
            "  ✓ chain modifier added"
        )

    # ========================================================
    # RECHARGE
    # ========================================================

    def apply_recharge(
        self,
        effect,
        charm_data,
        game_state
    ):

        game_state['recharge_targets'].append(
            effect.target
        )

        print(
            "  ✓ recharge modifier added"
        )
    
    def apply_gold(
        self,
        effect,
        charm_data,
        game_state
    ):
        
        game_state['gold_targets'].append(
            effect.target
        )

        print(
            " gold modifier added"
        )