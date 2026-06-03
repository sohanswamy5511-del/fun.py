from gamestate import game_state

# ============================================================
# BASE CONDITION CLASS
# ============================================================

class Condition:
    """Base class for all conditions."""

    def check(self, game_state):
        """Check if condition is met."""
        return True


# ============================================================
# PATTERN FAILURE CONDITIONS
# ============================================================

class NoLargePatternSpins(Condition):
    """
    Checks if no large patterns (4+ symbols) have appeared 
    for N consecutive spins.
    
    Used by: Spoons charm
    """

    def __init__(self, spins):
        self.spins = spins

    def check(self, game_state):
        return (
            game_state.get('failed_large_patterns', 0)
            >= self.spins
        )


class NoPatternSpins(Condition):
    """
    Checks if no patterns (any size) have appeared 
    for N consecutive spins.
    
    Used by: X charm (5 spins), N charm (4 spins), 
             Sunflower (2 spins), CatWink (1 spin)
    """

    def __init__(self, spins):
        self.spins = spins

    def check(self, game_state):
        return (
            game_state.get('failed_patterns', 0)
            >= self.spins
        )


# ============================================================
# PATTERN SUCCESS CONDITIONS
# ============================================================

class NumPatternScored(Condition):
    """
    Checks if in N consecutive spins or across Z spins at least M patterns were scored in each
    
    Used by: LuckyStar charm (3 consecutive spins with 1 patterns)
    """

    def __init__(self, patterns_required, consecutive_spins, across_spins_number):
        self.patterns_required = patterns_required
        self.consecutive_spins = consecutive_spins
        self.across_spins = across_spins_number

    def check(self, game_state):
        consecutive_scored = game_state.get(
            'consecutive_pattern_spins',
            0
        )
        return consecutive_scored >= self.consecutive_spins and game_state.get('last_spin_patterns', 0) >= self.patterns_required


# ============================================================
# CHARM-SPECIFIC CONDITIONS
# ============================================================

class FirstSpinAfterCharmBought(Condition):
    """
    Checks if this is the first spin after buying a charm.
    
    Used by: Cornerstone charm
    """

    def check(self, game_state):
        return game_state.get('charm_just_bought', False)


class RoundsSkipped(Condition):
    """
    Checks how many rounds have been skipped this deadline.
    
    Used by: NotGreedy charm (bonus increases by 3% per skipped charm)
    """

    def check(self, game_state):
        rounds_skipped = game_state.get('rounds_skipped_this_deadline', 0)
        return rounds_skipped == 0


class ScorelessRound(Condition):
    """
    Checks if the current round resulted in no patterns scored.
    
    Used by: BeefBrisket charm
    """

    def check(self, game_state):
        return game_state.get('round_scoreless', False)


class EarningsThreshold(Condition):
    """
    Checks if earnings exceeded a multiplier threshold this deadline.
    
    Used by: EverythingInExcess charm (1.5x threshold)
    """

    def __init__(self, multiplier):
        self.multiplier = multiplier

    def check(self, game_state):
        earnings = game_state.get('current_earnings', 0)
        deadline_amount = game_state.get('deadline_amount', 1)
        threshold = deadline_amount * self.multiplier
        return earnings >= threshold


class PatternTypeScored(Condition):
    """
    Checks if a specific pattern count was scored this spin.
    
    Used by: Ramen (5 patterns), etc.
    """

    def __init__(self, count):
        self.count = count

    def check(self, game_state):
        patterns_scored_this_spin = game_state.get('patterns_scored_this_spin', 0)
        return patterns_scored_this_spin >= self.count


class SymbolTypeScored(Condition):
    """
    Checks if patterns containing only a specific symbol type were scored.
    
    Used by: Coin Rush, etc.
    """

    def __init__(self, symbol_type):
        self.symbol_type = symbol_type

    def check(self, game_state):
        last_pattern_symbols = game_state.get('last_pattern_symbols', [])
        return all(sym.name == self.symbol_type.name for sym in last_pattern_symbols)


class JackpotScored(Condition):
    """
    Checks if jackpot patterns were scored this spin.
    
    Used by: SymbolFrenzy (5 jackpots), etc.
    """

    def __init__(self, count):
        self.count = count

    def check(self, game_state):
        jackpots_scored_this_spin = game_state.get('jackpots_scored_this_spin', 0)
        return jackpots_scored_this_spin >= self.count


class UniquePatternCount(Condition):
    """
    Checks if N unique pattern types were scored in one spin.
    
    Used by: SymbolRitual (5+ different patterns)
    """

    def __init__(self, count):
        self.count = count

    def check(self, game_state):
        unique_patterns = game_state.get('unique_patterns_this_spin', set())
        return len(unique_patterns) >= self.count


class ScorelessSpinFollowup(Condition):
    """
    Checks if patterns were scored after a scoreless spin.
    
    Used by: PatternChain (5 patterns after scoreless)
    """

    def __init__(self, pattern_count):
        self.pattern_count = pattern_count

    def check(self, game_state):
        last_spin_scoreless = game_state.get('last_spin_scoreless', False)
        patterns_this_spin = game_state.get('patterns_scored_this_spin', 0)
        return last_spin_scoreless and patterns_this_spin >= self.pattern_count

class UniqueSymbolCount(Condition):
    """
    Checks if patterns containing N unique symbol types were scored.
    
    Used by: SymbolEcho (3+ different symbols in scored patterns)
    """

    def __init__(self, count):
        self.count = count

    def check(self, game_state):
        unique_symbols = game_state.get('unique_symbols_this_spin', set())
        return len(unique_symbols) >= self.count

class SameSymbolCount(Condition):
    """
    Checks if patterns containing N of the same symbol type were scored.
    
    Used by: SymbolRally (6+ of the same symbol in scored patterns)
    """

    def __init__(self, count, time_requirement=None):
        self.count = count
        self.time_requirement = time_requirement

    def check(self, game_state):
        symbol_counts = game_state.get('symbol_counts_this_spin', {})
        return any(count >= self.count for count in symbol_counts.values())