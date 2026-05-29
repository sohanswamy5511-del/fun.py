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