import random
from time import sleep

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

    def apply_golden_modifier(self):
        """
        Golden modifier effect:
        When a golden symbol scores, it gains +base_value.
        This is applied during scoring, not here.
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
# LIST OF ALL SYMBOL TYPES
# ============================================================

BASE_SYMBOL_CLASSES = [Dice, Coin, Spinner, Card, Wheel]

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
          - Formation 0 = relative
          - Formation 1 = absolute
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
    Jackpot()
]

# ============================================================
# BOARD SYSTEM
# ============================================================

class Board:
    """
    The Board manages:
      - Grid of symbols
      - Filling and activating symbols
      - Applying global bonuses
      - Pattern detection
      - Pattern scoring
      - Golden modifier logic
      - Delayed gold bonus system (stacking)
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

        # Permanent bonuses applied to all symbols of a type
        self.global_symbol_bonuses = {}  # {SymbolClass: int}

        # Delayed bonuses (stacking)
        self.delayed_bonuses = []  # list of dicts:
        # {
        #   "symbol_type": Coin or Dice,
        #   "increase": int,
        #   "delay": int
        # }

        self.grand_total = 0

    # --------------------------------------------------------
    # APPLY PENDING BONUSES (start of each spin)
    # --------------------------------------------------------

    def apply_pending_bonuses(self):
        """
        Apply any delayed bonuses whose delay has expired.
        """
        to_apply = [b for b in self.delayed_bonuses if b["delay"] <= 0]

        for bonus in to_apply:
            stype = bonus["symbol_type"]
            inc = bonus["increase"]

            self.global_symbol_bonuses[stype] = (
                self.global_symbol_bonuses.get(stype, 0) + inc
            )

            print(f"Delayed bonus applied! All {stype.__name__}s gain +{inc} permanently.")

        # Remove applied bonuses
        self.delayed_bonuses = [b for b in self.delayed_bonuses if b["delay"] > 0]

    # --------------------------------------------------------
    # FILL BOARD WITH SYMBOLS
    # --------------------------------------------------------

    def fill_cells(self, symbol_classes, weights_override, owned_charms):
        """
        Fill empty cells with symbols, applying:
          - Weight overrides
          - Global bonuses
          - Golden modifier chance
          - Activation (roll/spin/draw)
        """

        # Build weights
        weights = []
        for cls in symbol_classes:
            base_w = getattr(cls, "weight", 1)
            w = weights_override.get(cls, base_w)
            weights.append(w)

        # Check charms
        has_golden_coins = any(c.kind == "modifier" and c.target is Coin for c in owned_charms)
        has_rigged_dice = any(c.kind == "modifier" and c.target is Dice for c in owned_charms)

        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y] is None:

                    # Choose symbol class
                    symbol_class = random.choices(symbol_classes, weights=weights, k=1)[0]
                    symbol = symbol_class()

                    # Apply permanent global bonus to current value so the
                    # symbol's multiplier uses the increased value.
                    bonus = self.global_symbol_bonuses.get(symbol_class, 0)
                    if bonus:
                        symbol.current_value += bonus

                    # Activate (roll/spin/draw)
                    symbol.activate()

                    # Golden modifier chance
                    if isinstance(symbol, Coin) and has_golden_coins:
                        if random.randint(1, 100) <= 20:
                            symbol.is_golden = True
                            symbol.display_name += " [GOLD]"

                    if isinstance(symbol, Dice) and has_rigged_dice:
                        if random.randint(1, 100) <= 30:
                            symbol.is_golden = True
                            symbol.display_name += " [GOLD]"

                    self.grid[x][y] = symbol

    # --------------------------------------------------------
    # SPIN
    # --------------------------------------------------------

    def current_spin(self, symbol_classes, weights_override, owned_charms):
        """
        Perform a new spin:
          - Apply pending bonuses
          - Reset grid
          - Fill grid
        """
        self.apply_pending_bonuses()

        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.fill_cells(symbol_classes, weights_override, owned_charms)
        self.print_board()
        sleep(1)

    # --------------------------------------------------------
    # PRINT BOARD
    # --------------------------------------------------------

    def print_board(self):
        print("\n=== BOARD ===")
        for row in self.grid:
            print(" | ".join(f"{s.display_name:12}" for s in row))
        print("=============\n")

    # --------------------------------------------------------
    # SCORING
    # --------------------------------------------------------

    def display_total(self, owned_charms):
        """
        Score all patterns:
          - Detect matches
          - Apply golden modifier
          - Apply retrigger logic
          - Add delayed bonuses
        """

        total = 0
        all_matches = []

        # ----------------------------------------------------
        # FIND ALL MATCHES
        # ----------------------------------------------------
        for pattern in PATTERNS:
            matches = pattern.matches(self.grid)
            for cells in matches:
                all_matches.append((pattern, cells))

        # Sort by size (largest first)
        all_matches.sort(key=lambda x: -len(x[1]))

        # ----------------------------------------------------
        # SELECT MATCHES
        # ----------------------------------------------------
        chosen = []

        def is_contained_in_non_jackpot(candidate_cells):
            return any(
                candidate_cells <= outer_cells and outer_pattern.name != "Jackpot"
                for outer_pattern, outer_cells in chosen
            )

        for pattern, cells in all_matches:
            if is_contained_in_non_jackpot(cells):
                continue

            chosen.append((pattern, cells))

        # ----------------------------------------------------
        # RETRIGGER LOGIC
        # ----------------------------------------------------
        retrigger_count = sum(1 for c in owned_charms if c.kind == "retrigger")
        triggers = 1 + retrigger_count

        # ----------------------------------------------------
        # SCORE EACH PATTERN
        # ----------------------------------------------------
        print("\n=== PATTERN BREAKDOWN ===")

        patterns_this_spin = len(chosen)

        for pattern, cells in chosen:

            symbol_values = []
            golden_symbols = []
            symbol_details = []

            for (x, y) in cells:
                s = self.grid[x][y]
                value = s.current_value

                detail = f"{s.display_name} @({x},{y}) = {s.current_value}"
                if s.is_golden:
                    detail += " (golden bonus queued for next spin)"
                symbol_details.append(detail)

                if s.is_golden:
                    golden_symbols.append(s)

                symbol_values.append(value)

            pattern_sum = sum(symbol_values)
            pattern_score = pattern.get_multiplier(pattern_sum) * triggers
            total += pattern_score

            print(f"\nPattern: {pattern.name}")
            print(f"Cells: {sorted(list(cells))}")
            print("Symbols:")
            for detail in symbol_details:
                print(f"  - {detail}")
            print(f"Sum after increases: {pattern_sum}")
            print(f"Multiplier: x{pattern.current_multiplier_value}")
            print(f"Triggers: {triggers}")
            print(f"Contribution: {pattern_score}")
            sleep(1)

            # ------------------------------------------------
            # GOLDEN PATTERN TRIGGER → APPLY PERMANENT BONUS
            # ------------------------------------------------
            if len(golden_symbols) == len(cells):  # all symbols golden
                stype = type(golden_symbols[0])

                if stype is Coin:
                    increase = 3 * len(golden_symbols)
                elif stype is Dice:
                    increase = 5 * len(golden_symbols)
                else:
                    increase = 0

                if increase > 0:
                    self.delayed_bonuses.append({
                        "symbol_type": stype,
                        "increase": increase,
                        "delay": 1
                    })
                    print(f"Golden pattern! A delayed +{increase} bonus for all {stype.__name__}s has been queued for the next spin.")

        # ----------------------------------------------------
        # UPDATE DELAYED BONUSES
        # ----------------------------------------------------
        for bonus in self.delayed_bonuses:
            bonus["delay"] -= 1

        # ----------------------------------------------------
        # FINAL OUTPUT
        # ----------------------------------------------------
        print("\n=========================")
        print(f"Total Matches: {patterns_this_spin}")
        print(f"Total Value: {total}")
        print("=========================\n")

        self.grand_total += total
        return total

# ============================================================
# CHARM SYSTEM
# ============================================================

class Charm:
    """
    A charm modifies gameplay in one of several ways:
      - extra_spin: +1 max spin per round
      - weight: increases spawn weight of a symbol type
      - modifier: gives a chance for symbols to spawn golden
      - retrigger: patterns trigger one extra time
    """

    def __init__(self, name, description, kind, target=None, amount=0):
        self.name = name
        self.description = description
        self.kind = kind          # "extra_spin", "weight", "modifier", "retrigger"
        self.target = target      # Symbol class (Coin, Dice, etc.)
        self.amount = amount      # numeric effect (weight +5, chance %, etc.)

    def __str__(self):
        return f"{self.name}: {self.description}"


# ============================================================
# CHARM DEFINITIONS
# ============================================================

Spare_Change = Charm(
    "Spare Change",
    "Gain +1 max spin per round.",
    kind="extra_spin"
)

ImBadAtMath = Charm(
    "I'm Bad At Math",
    "Patterns trigger one more time.",
    kind="retrigger"
)

Struck_Gold = Charm(
    "Struck Gold",
    "Coins appear more often (+5 weight).",
    kind="weight",
    target=Coin,
    amount=5
)

Trick_Deck = Charm(
    "Trick Deck",
    "Cards appear more often (+5 weight).",
    kind="weight",
    target=Card,
    amount=5
)

ILoveTops = Charm(
    "I Love Tops",
    "Spinners appear more often (+5 weight).",
    kind="weight",
    target=Spinner,
    amount=5
)

Dice_Hard = Charm(
    "Dice Hard",
    "Dice appear more often (+5 weight).",
    kind="weight",
    target=Dice,
    amount=5
)

WheelOfFortune = Charm(
    "Wheel of Fortune",
    "Wheels appear more often (+5 weight).",
    kind="weight",
    target=Wheel,
    amount=5
)

GoldenCoins = Charm(
    "Golden Coins",
    "20% chance for Coins to spawn with the GOLD modifier.",
    kind="modifier",
    target=Coin,
    amount=20
)

Rigged_Dice = Charm(
    "Rigged Dice",
    "30% chance for Dice to spawn with the GOLD modifier.",
    kind="modifier",
    target=Dice,
    amount=30
)

ALL_CHARMS = [
    Spare_Change,
    Struck_Gold,
    Trick_Deck,
    ILoveTops,
    Dice_Hard,
    WheelOfFortune,
    ImBadAtMath,
    GoldenCoins,
    Rigged_Dice
]


# ============================================================
# CHARM HELPERS
# ============================================================

def compute_effective_max_spins(base_max_spins, owned_charms):
    """
    Extra spin charms increase max spins per round.
    """
    extra = sum(1 for c in owned_charms if c.kind == "extra_spin")
    return base_max_spins + extra


def compute_weight_overrides(owned_charms):
    """
    Weight charms increase spawn weight for specific symbol types.
    """
    overrides = {}

    for c in owned_charms:
        if c.kind == "weight" and c.target is not None:
            overrides[c.target] = overrides.get(c.target, getattr(c.target, "weight", 1)) + c.amount

    return overrides


# ============================================================
# STORE SYSTEM
# ============================================================

def store_phase(money, owned_charms):
    """
    Store logic:
      - Shows 4 random charms not yet owned
      - Charms cost $5
      - Player may buy one charm per visit
    """

    print("\nWelcome to the store.")
    print(f"You have ${money}. Charms cost $5 each.")

    # Filter out charms already owned
    available = [c for c in ALL_CHARMS if c not in owned_charms]

    if not available:
        print("No more charms available.")
        return money, owned_charms

    # Show up to 4 random charms
    stock = random.sample(available, min(4, len(available)))

    for i, charm in enumerate(stock):
        print(f"{i+1}: {charm}")

    print("Enter the number of the charm to buy, or press Enter to leave the store.")
    choice = input("> ").strip()

    if choice == "":
        print("Leaving the store.")
        return money, owned_charms

    if not choice.isdigit():
        print("Invalid choice. Leaving the store.")
        return money, owned_charms

    idx = int(choice) - 1

    if idx < 0 or idx >= len(stock):
        print("Invalid index. Leaving the store.")
        return money, owned_charms

    if money < 5:
        print("Not enough money to buy a charm.")
        return money, owned_charms

    # Purchase charm
    chosen = stock[idx]
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)
    owned_charms.append(chosen)

    money -= 5

    print(f"You bought: {chosen.name}")
    return money, owned_charms

# ============================================================
# INPUT HELPERS
# ============================================================

def get_spin_amount(money, max_spins):
    """
    Ask the player how many spins they want.
    Options:
      - Enter a number (1 to max_spins)
      - Enter 'store' to visit the store
      - Enter 'q' to quit
    """

    while True:
        print(f"You have ${money}. Each spin costs $1.")
        print(f"Enter number of spins (max {max_spins}), 'store' to visit store, or 'q' to quit.")
        choice = input("> ").strip().lower()

        if choice == "q":
            return "q"

        if choice == "store":
            return "store"

        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue

        spins = int(choice)

        if spins < 1:
            print("You must spin at least once.")
            continue

        if spins > max_spins:
            print(f"Maximum spins is {max_spins}.")
            continue

        if spins > money:
            print(f"You don't have enough money for {spins} spins.")
            continue

        return spins


# ============================================================
# MAIN GAME LOOP
# ============================================================

def main():
    print("Welcome to the Slot Machine Game!")

    money = 16
    BASE_MAX_SPINS = 8
    owned_charms = []

    while money > 0:
        board = Board(3, 5)

        # Compute max spins with charms
        max_spins = compute_effective_max_spins(BASE_MAX_SPINS, owned_charms)

        # Ask user for spin amount
        choice = get_spin_amount(money, max_spins)

        if choice == "q":
            print("Thanks for playing!")
            break

        if choice == "store":
            money, owned_charms = store_phase(money, owned_charms)
            continue

        spins = choice
        money -= spins

        # Weight overrides from charms
        weight_overrides = compute_weight_overrides(owned_charms)

        # Reset grand total for this round
        board.grand_total = 0

        # Perform spins
        for i in range(spins):
            print(f"\n--- SPIN {i+1} ---")
            board.current_spin(BASE_SYMBOL_CLASSES, weight_overrides, owned_charms)
            board.display_total(owned_charms)

        # Round summary
        print("\n==============================")
        print("      FINAL GRAND TOTAL")
        print("==============================")
        print(board.grand_total)
        print()

        # Add winnings
        money += board.grand_total
        print(f"You now have ${money}.\n")

    # Out of money
    if money <= 0:
        print("You lost all your money. Game over.")
        return


# ============================================================
# RUN GAME
# ============================================================

if __name__ == "__main__":
    main()
