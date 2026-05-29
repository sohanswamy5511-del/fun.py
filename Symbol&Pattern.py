# ============================================================
# SYMBOL BASE CLASS
# ============================================================

class Symbol:
    """
    Base class for all symbols.
    Each symbol has:
      - name
      - base_value
      - current_value
      - display_name
      - is_golden (modifier flag)
    """

    weight = 1  # default weight if not overridden

    def __init__(self, name, base_value, current_value=None):
        self.name = name
        self.base_value = base_value
        self.current_value = current_value if current_value is not None else base_value
        self.display_name = name
        self.is_golden = False
        self.modifiers = []

    def apply_golden_modifier(self):
        """
        Golden modifier effect:
        For every symbol with the GOLD modifier that is scored in a pattern,
        the symbol's type gains +base_value permanently (applied next spin).
        Only one GOLD symbol is needed in a pattern to trigger this for its
        symbol type; multiple GOLD symbols in the same pattern stack.
        Retriggers multiply the total amount queued (i.e., multiplied by
        the number of triggers).
        """
        pass

    def apply_multiplier(self, mult):
        """
        Multiply the symbol using its current value if set,
        otherwise use the base value.
        """
        base = self.current_value if self.current_value is not None else self.base_value
        self.current_value = base * mult

    def activate(self):
        """
        Each subclass overrides this to roll/spin/draw.
        """
        raise NotImplementedError


# ============================================================
# COIN
# ============================================================

class Coin(Symbol):
    weight = 30

    def __init__(self):
        super().__init__("Coin", base_value=3)

    def activate(self):
        """
        Flip the coin:
          Heads → x5
          Tails → x1
        """
        result = random.choice(["Heads", "Tails"])
        mult = 5 if result == "Heads" else 1
        self.apply_multiplier(mult)
        self.display_name = f"Coin ({result})"
        return self.current_value


# ============================================================
# SPINNER
# ============================================================

class Spinner(Symbol):
    weight = 25

    def __init__(self):
        super().__init__("Spinner", base_value=2)

    def activate(self):
        """
        Spin: multiplier 1–12
        """
        mult = random.randint(1, 12)
        self.apply_multiplier(mult)
        self.display_name = f"Spinner (x{mult})"
        return self.current_value


# ============================================================
# DICE
# ============================================================

class Dice(Symbol):
    weight = 20

    def __init__(self):
        super().__init__("Dice", base_value=5)
        self.sidemult = None

    def activate(self):
        """
        Roll: multiplier 1–6
        """
        self.sidemult = random.randint(1, 6)
        self.apply_multiplier(self.sidemult)
        self.display_name = f"Dice (x{self.sidemult})"
        return self.current_value


# ============================================================
# CARD
# ============================================================

class Card(Symbol):
    weight = 15

    def __init__(self):
        super().__init__("Card", base_value=3)

    def activate(self):
        """
        Draw: multiplier 1–13
        """
        value = random.randint(1, 13)
        self.apply_multiplier(value)
        self.display_name = f"Card (x{value})"
        return self.current_value


# ============================================================
# WHEEL
# ============================================================

class Wheel(Symbol):
    weight = 10

    def __init__(self):
        super().__init__("Wheel", base_value=5)

    def activate(self):
        """
        Spin: multiplier 1–10
        """
        mult = random.randint(1, 10)
        self.apply_multiplier(mult)
        self.display_name = f"Wheel (x{mult})"
        return self.current_value


# ============================================================
# SEVEN (for 777)
# ============================================================

class Seven(Symbol):
    weight = 0

    def __init__(self):
        super().__init__("Seven", base_value=777)

    def activate(self):
        pass


# ============================================================
# LIST OF ALL SYMBOL TYPES
# ============================================================

BASE_SYMBOL_CLASSES = [Dice, Coin, Spinner, Card, Wheel, Seven]

# ============================================================
# PATTERN BASE CLASS
# ============================================================

class Pattern:
    """
    Base class for all patterns.

    Each pattern has:
      - name
      - formations: list of lists of (dx, dy) offsets OR absolute coords
      - base_multiplier_value
      - current_multiplier_value
      - absolute: if True, formations are absolute board coordinates
    """

    def __init__(self, name, formations, base_multiplier_value, absolute=False):
        self.name = name
        self.formations = formations
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = base_multiplier_value
        self.absolute = absolute

    # --------------------------------------------------------
    # MATCHING LOGIC
    # --------------------------------------------------------

    def matches(self, board):
        """
        Returns a list of matches.
        Each match is a tuple: (pattern, set_of_cells)
        """
        rows = len(board)
        cols = len(board[0])
        found = []

        for formation in self.formations:

            # ------------------------------------------------
            # ABSOLUTE PATTERN (coordinates are fixed)
            # ------------------------------------------------
            if self.absolute:
                anchor_symbol = board[formation[0][0]][formation[0][1]].name
                match = True

                for (x, y) in formation:
                    if not (0 <= x < rows and 0 <= y < cols):
                        match = False
                        break
                    if board[x][y].name != anchor_symbol:
                        match = False
                        break

                if match:
                    found.append(set(formation))
                continue

            # ------------------------------------------------
            # RELATIVE PATTERN (slide across board)
            # ------------------------------------------------
            for start_x in range(rows):
                for start_y in range(cols):

                    anchor_symbol = board[start_x][start_y].name
                    match = True
                    cells = set()

                    for dx, dy in formation:
                        x = start_x + dx
                        y = start_y + dy

                        if not (0 <= x < rows and 0 <= y < cols):
                            match = False
                            break

                        if board[x][y].name != anchor_symbol:
                            match = False
                            break

                        cells.add((x, y))

                    if match:
                        found.append(cells)

        return found

    # --------------------------------------------------------
    # MULTIPLIER
    # --------------------------------------------------------

    def get_multiplier(self, symbol_sum):
        return symbol_sum * self.current_multiplier_value


# ============================================================
# BASIC PATTERNS
# ============================================================

class VerticalLine(Pattern):
    def __init__(self):
        super().__init__(
            "Vertical Line",
            formations=[[(0, 0), (1, 0), (2, 0)]],
            base_multiplier_value=1
        )


class HorizontalLine(Pattern):
    def __init__(self):
        super().__init__(
            "Horizontal Line",
            formations=[[(0, 0), (0, 1), (0, 2)]],
            base_multiplier_value=1
        )


class DiagonalLine(Pattern):
    def __init__(self):
        super().__init__(
            "Diagonal Line",
            formations=[
                [(0, 0), (1, 1), (2, 2)],
                [(0, 2), (1, 1), (2, 0)]
            ],
            base_multiplier_value=1
        )


class HorizontalLineLarge(Pattern):
    def __init__(self):
        super().__init__(
            "Horizontal Line Large",
            formations=[[(0, 0), (0, 1), (0, 2), (0, 3)]],
            base_multiplier_value=2
        )


class HorizontalLineXL(Pattern):
    def __init__(self):
        super().__init__(
            "Horizontal Line XL",
            formations=[[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]],
            base_multiplier_value=3
        )

# ============================================================
# SPOON PATTERN (A = relative, B = absolute)
# ============================================================

class Spoon(Pattern):
    def __init__(self):
        super().__init__(
            "Spoon",
            formations=[
                # Spoon A (relative)
                [(0, 0), (1, 0), (2, 0),
                 (0, 1), (1, 1), (2, 1),
                 (1, 2), (1, 3), (1, 4)],

                # Spoon B (absolute)
                [(1, 0), (1, 1), (1, 2),
                 (1, 3), (1, 4),
                 (2, 3), (2, 4),
                 (0, 3), (0, 4)]
            ],
            base_multiplier_value=5,
            absolute=False  # Spoon A is relative; Spoon B handled manually
        )

    def matches(self, board):
        """
        Custom override:
          - Formation 0 = relative (Spoon A)
          - Formation 1 = absolute (Spoon B)
        """
        rows = len(board)
        cols = len(board[0])
        found = []

        # ----------------------------
        # Spoon A (relative)
        # ----------------------------
        formationA = self.formations[0]

        for start_x in range(rows):
            for start_y in range(cols):

                anchor_symbol = board[start_x][start_y].name
                match = True
                cells = set()

                for dx, dy in formationA:
                    x = start_x + dx
                    y = start_y + dy

                    if not (0 <= x < rows and 0 <= y < cols):
                        match = False
                        break

                    if board[x][y].name != anchor_symbol:
                        match = False
                        break

                    cells.add((x, y))

                if match:
                    found.append(cells)

        # ----------------------------
        # Spoon B (absolute)
        # ----------------------------
        formationB = self.formations[1]
        anchor_symbol = board[formationB[0][0]][formationB[0][1]].name
        match = True
        cells = set()

        for (x, y) in formationB:
            if not (0 <= x < rows and 0 <= y < cols):
                match = False
                break
            if board[x][y].name != anchor_symbol:
                match = False
                break
            cells.add((x, y))

        if match:
            found.append(cells)

        return found

class XPattern(Pattern):
    def __init__(self):
        super().__init__(
            "X Pattern",
            formations=[
                [(0, 0), (0, 1), (0, 3), (0, 4),
                (1, 1), (1, 2), (1, 3),
                 (2, 0), (2, 1), (2, 3), (2, 4)]
            ],
            base_multiplier_value=7,
            absolute=True
        )

class NPatternA(Pattern):
    def __init__(self):
        super().__init__(
            "N Pattern A",
            formations=[
                [(0, 0), (0, 3), (0, 4),
                 (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                 (2, 0), (2, 1), (2, 4)]
            ],
            base_multiplier_value=8,
            absolute=True
        )

class NPatternB(Pattern):
    def __init__(self):
        super().__init__(
            "N Pattern B",
            formations=[
                [(0, 0), (0, 1), (0, 4),
                 (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                 (2, 0), (2, 3), (2, 4)]
            ],
            base_multiplier_value=8,
            absolute=True
        )

# ============================================================
# JACKPOT PATTERN
# ============================================================

class Jackpot(Pattern):
    def __init__(self):
        super().__init__(
            "Jackpot",
            formations=[[(x, y) for x in range(3) for y in range(5)]],
            base_multiplier_value=10
        )


# ============================================================
# PATTERN LIST
# ============================================================

PATTERNS = [
    VerticalLine(),
    HorizontalLine(),
    DiagonalLine(),
    HorizontalLineLarge(),
    HorizontalLineXL(),
    Spoon(),
    NPatternA(),
    NPatternB(),
    XPattern(),
    Jackpot()
]