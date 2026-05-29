# ============================================================
# CENTRAL GAME STATE
# ============================================================

game_state = {
    # Persistent modifiers
    'active_bonuses': {},

    # Multipliers
    'symbols_mult': 1,
    'patterns_mult': 1,

    # Runtime combat-style effects
    'repetition_targets': [],
    'chain_targets': [],
    'recharge_targets': [],

    # Misc
    'pending_luck': 0,
    'spins_left': 0
}