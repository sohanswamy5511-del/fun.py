# ============================================================
# SCORE ENGINE
# ============================================================

class ScoreEngine:
    """
    Calculates scores for matched patterns on the board.
    
    Handles:
    - Base symbol values
    - Pattern multipliers
    - Global pattern multipliers
    - Chain bonuses
    - Repetition bonuses
    - Chain count tracking
    """

    def score_patterns(
        self,
        matches,
        board,
        game_state
    ):
        """
        Score all matched patterns.

        Args:
            matches: List of tuples (pattern, cells)
                where cells is a list of (x, y) coordinates
            board: Board instance with grid containing Symbol objects
            game_state: Dict containing multipliers, chain_counts, etc.

        Returns:
            int: total_score across all patterns
        """

        total_score = 0

        for pattern, cells in matches:

            score = self.score_pattern(
                pattern,
                cells,
                board,
                game_state
            )

            total_score += score

        return total_score

    def score_pattern(
        self,
        pattern,
        cells,
        board,
        game_state
    ):
        """
        Score a single pattern.

        Args:
            pattern: Pattern instance with name and get_multiplier() method
            cells: List of (x, y) coordinates in the pattern
            board: Board instance with grid containing Symbol objects
            game_state: Dict with 'patterns_mult', 'chain_counts', 
                       'repetition_targets'

        Returns:
            int: score for this pattern after all multipliers and bonuses
        """

        # --------------------------------
        # BASE SYMBOL VALUE
        # --------------------------------

        symbol_sum = self._calculate_symbol_sum(
            cells,
            board
        )

        # --------------------------------
        # PATTERN MULTIPLIER
        # --------------------------------

        score = pattern.get_multiplier(
            symbol_sum
        )

        # --------------------------------
        # GLOBAL PATTERN MULT
        # --------------------------------

        score *= game_state.get('patterns_mult', 1)

        # --------------------------------
        # CHAIN BONUS
        # --------------------------------

        chain_count = game_state.get(
            'chain_counts',
            {}
        ).get(pattern.name, 0)

        score += chain_count

        # --------------------------------
        # REPETITIONS
        # --------------------------------

        repetitions = self._count_repetitions(
            pattern.name,
            game_state
        )

        total = score

        for _ in range(repetitions):
            total += score

        # --------------------------------
        # UPDATE CHAIN
        # --------------------------------

        self._update_chain_count(
            pattern.name,
            game_state
        )

        # --------------------------------
        # DISPLAY
        # --------------------------------

        print(
            f"{pattern.name} -> {total}"
        )

        board.print_board(
            highlight_cells=cells,
            pattern_score=total
        )

        return total

    # ========================================================
    # HELPER METHODS
    # ========================================================

    def _calculate_symbol_sum(self, cells, board):
        """
        Calculate the sum of symbol values for cells.
        
        Converts symbol instances to their IDs (names) for processing,
        then reconstructs values to prevent circular imports.
        """
        symbol_sum = 0

        for x, y in cells:
            symbol = board.grid[x][y]
            # Use symbol.current_value (already a number, not a class)
            symbol_sum += symbol.current_value

        return symbol_sum

    def _count_repetitions(self, pattern_name, game_state):
        """
        Count how many times this pattern appears in repetition_targets.
        
        Works with symbol IDs (names) to avoid class dependencies.
        """
        repetitions = 0

        for target in game_state.get('repetition_targets', []):
            if target == pattern_name:
                repetitions += 1

        return repetitions

    def _update_chain_count(self, pattern_name, game_state):
        """
        Increment the chain count for this pattern.
        """
        if 'chain_counts' not in game_state:
            game_state['chain_counts'] = {}

        game_state['chain_counts'][pattern_name] = (
            game_state['chain_counts']
            .get(pattern_name, 0)
            + 1
        )
