class Board:
    """
    Effect-driven Board system.

    - Charms unlock modifiers
    - Board executes effects
    - Scoring system restored (pattern detection + highlight)
    """

    # ============================================================
    # INIT
    # ============================================================

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols

        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.grand_total = 0

        # -----------------------------
        # MODIFIER UNLOCK STATE
        # -----------------------------
        self.modifier_unlocked = {
            "repetition": False,
            "recharge": False,
            "chain": False,
            "symbol_mult": False,
            "pattern_mult": False,
        }

        # -----------------------------
        # MODIFIER DATA
        # -----------------------------
        self.repetition_map = {}
        self.recharge_pool = []
        self.chain_map = {}

        self.symbol_mult = 1
        self.pattern_mult = 1

        self.delayed_bonuses = []

    # ============================================================
    # CONTROL
    # ============================================================

    def unlock(self, name):
        if name in self.modifier_unlocked:
            self.modifier_unlocked[name] = True

    def has(self, name):
        return self.modifier_unlocked.get(name, False)

    # ============================================================
    # CHARM SYSTEM
    # ============================================================

    def apply_charm(self, charm):
        for effect in charm.effects:
            self.apply_effect(effect)

    def apply_effect(self, effect):

        if effect.type == "UNLOCK":
            self.unlock(effect.target)

        elif effect.type == "ADD_REPETITION":
            self.unlock("repetition")

            targets = effect.target
            if not isinstance(targets, tuple):
                targets = (targets,)

            for t in targets:
                self.repetition_map[t.__name__] = (
                    self.repetition_map.get(t.__name__, 0)
                    + effect.amount
                )

        elif effect.type == "ADD_RECHARGE":
            self.unlock("recharge")

            targets = effect.target
            if not isinstance(targets, tuple):
                targets = (targets,)

            for t in targets:
                if t not in self.recharge_pool:
                    self.recharge_pool.append(t)

        elif effect.type == "ADD_CHAIN":
            self.unlock("chain")

            targets = effect.target
            if not isinstance(targets, tuple):
                targets = (targets,)

            for t in targets:
                self.chain_map[t.__name__] = (
                    self.chain_map.get(t.__name__, 0)
                    + effect.amount
                )

        elif effect.type == "ADD_SYMBOL_MULT":
            self.unlock("symbol_mult")
            self.symbol_mult += effect.amount

        elif effect.type == "ADD_PATTERN_MULT":
            self.unlock("pattern_mult")
            self.pattern_mult += effect.amount

    # ============================================================
    # CONTROL HUB
    # ============================================================

    def print_modifier_hub(self):

        print("\n=== MODIFIER HUB ===")

        if self.has("repetition"):
            print("Repetition:", self.repetition_map or "none")

        if self.has("recharge"):
            print("Recharge:", [c.__name__ for c in self.recharge_pool] or "none")

        if self.has("chain"):
            print("Chain:", self.chain_map or "none")

        if self.has("symbol_mult"):
            print("Symbol Mult:", self.symbol_mult)

        if self.has("pattern_mult"):
            print("Pattern Mult:", self.pattern_mult)

    # ============================================================
    # PATTERN SCORING CORE
    # ============================================================

    def calculate_pattern_score(self, pattern, base_score):

        score = base_score

        if self.has("chain"):
            score += self.chain_map.get(pattern.name, 0)

        if self.has("pattern_mult"):
            score *= self.pattern_mult

        return score

    # ============================================================
    # PATTERN ACTIVATION
    # ============================================================

    def activate_pattern(self, pattern, base_score, highlight_cells=None):

        base = self.calculate_pattern_score(pattern, base_score)
        repeats = self.repetition_map.get(pattern.name, 0)

        total = base

        print(f"\n{pattern.name} -> {base}")

        # highlight main trigger
        self.print_board(highlight_cells, base)

        # repetition triggers
        for i in range(repeats):
            extra = self.calculate_pattern_score(pattern, base_score)
            print(f"Repeat {i+1}: {extra}")
            total += extra

            self.print_board(highlight_cells, extra)

        self.grand_total += total

        if self.has("chain"):
            self.chain_map[pattern.name] = self.chain_map.get(pattern.name, 0) + pattern.base_value

        if self.has("recharge"):
            self.trigger_recharge()

    # ============================================================
    # RECHARGE
    # ============================================================

    def trigger_recharge(self):
        if not self.recharge_pool:
            return

        chosen = random.choice(self.recharge_pool)
        print(f"{chosen.__name__} gains +1 charge!")

    # ============================================================
    # GRID
    # ============================================================

    def fill_board(self, symbol_classes, weights):

        for x in range(self.rows):
            for y in range(self.cols):

                if self.grid[x][y] is not None:
                    continue

                self.grid[x][y] = random.choices(
                    symbol_classes,
                    weights=weights,
                    k=1
                )[0]

    # ============================================================
    # SPIN
    # ============================================================

    def spin(self, symbol_classes, weights):

        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.fill_board(symbol_classes, weights)

        print("\n=== BOARD ===")
        for row in self.grid:
            print(" | ".join(s.display_name for s in row))

        self.print_modifier_hub()

    # ============================================================
    # FULL SCORING + HIGHLIGHT SYSTEM
    # ============================================================

    def display_total(self, patterns):
        """
        patterns = list of (pattern, cells)
        """

        total = 0

        for pattern, cells in patterns:

            base_score = sum(self.grid[x][y].current_value for x, y in cells)

            score = self.calculate_pattern_score(pattern, base_score)

            print(f"{pattern.name} scored {score}")

            self.print_board(cells, score)

            total += score

        self.grand_total += total
        return total

    # ============================================================
    # BOARD PRINT WITH HIGHLIGHT
    # ============================================================

    def print_board(self, highlight_cells=None, pattern_score=None):

        print("\n=== BOARD ===")

        highlight = set(highlight_cells or [])

        for x, row in enumerate(self.grid):
            line = []
            for y, s in enumerate(row):

                text = f"{s.display_name:14}"

                if (x, y) in highlight:
                    text = f"[{text}]"

                line.append(text)

            print(" | ".join(line))

        if pattern_score is not None:
            print(f"\nScore: {pattern_score}")