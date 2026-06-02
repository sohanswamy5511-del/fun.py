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
    'repetition_targets': {},
    "repetition_counts": {},
    'chain_targets': {},
    "chain_counts": {},
    'recharge_targets': {},
    "recharge_counts": {},

    # Misc
    'pending_luck': 0,
    'spins_left': 0,
    'balance': 0,
    'total_winnings': 0
}