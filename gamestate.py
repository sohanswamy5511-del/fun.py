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
    'symbol_targets': {},
    "symbol_counts": {},
    'pattern_targets': {},
    "pattern_counts": {},
    'earning_targets': {},
    "earning_counts": {},

    # percentages
    "repetition_percent": 0,
    "chain_percent": 0,
    "recharge_percent": 0,
    "symbol_percent": 0,
    "pattern_percent": 0,
    "earning_percent": 0,

    # Misc
    'pending_luck': 0,
    'spins_left': 0,
    'balance': 0,
    'total_winnings': 0,
    'charms': {},
    'last_bought_charm': None
}