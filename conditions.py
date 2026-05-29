from gamestate import game_state
class condition:

    def check(self, game_state):
        return True

class NoLargePatternSpins(condition):

    def __init__(self, spins):

        self.spins = spins

    def check(self, game_state):

        return (
            game_state.failed_large_patterns
            >= self.spins
        )
    
class NoPatternSpins(condition):
    def __init__(self, spins):
        
        self.spins = spins
    
    def check(self, game_state):

        return (
            game_state.failed_patterns
            >= self.spins
        )