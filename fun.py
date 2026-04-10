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

    def fill_cells(self, symbol_classes, weights, owned_charms):
        """
        Fill empty cells with symbols, applying:
          - Weight overrides
          - Global bonuses
          - Golden modifier chance
          - Activation (roll/spin/draw)
        """

        # Build weights list in order
        weights_list = [weights[cls] for cls in symbol_classes]

        # Check charms
        has_golden_coins = any(d['charm'].kind == "modifier" and d['charm'].target is Coin for d in owned_charms)
        has_rigged_dice = any(d['charm'].kind == "modifier" and d['charm'].target is Dice for d in owned_charms)
        has_golden_spinners = any(d['charm'].kind == "modifier" and d['charm'].target is Spinner for d in owned_charms)
        has_golden_cards = any(d['charm'].kind == "modifier" and d['charm'].target is Card for d in owned_charms)
        has_golden_wheels = any(d['charm'].kind == "modifier" and d['charm'].target is Wheel for d in owned_charms)

        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y] is None:

                    # Choose symbol class
                    symbol_class = random.choices(symbol_classes, weights=weights_list, k=1)[0]
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
                        if random.randint(1, 100) <= 25:
                            symbol.is_golden = True
                            symbol.display_name += " [GOLD]"

                    if isinstance(symbol, Dice) and has_rigged_dice:
                        if random.randint(1, 100) <= 20:
                            symbol.is_golden = True
                            symbol.display_name += " [GOLD]"

                    if isinstance(symbol, Spinner) and has_golden_spinners:
                        if random.randint(1, 100) <= 30:
                            symbol.is_golden = True
                            symbol.display_name += " [GOLD]"

                    if isinstance(symbol, Card) and has_golden_cards:
                        if random.randint(1, 100) <= 25:
                            symbol.is_golden = True
                            symbol.display_name += " [GOLD]"

                    if isinstance(symbol, Wheel) and has_golden_wheels:
                        if random.randint(1, 100) <= 25:
                            symbol.is_golden = True
                            symbol.display_name += " [GOLD]"

                    self.grid[x][y] = symbol

    # --------------------------------------------------------
    # SPIN
    # --------------------------------------------------------

    def current_spin(self, symbol_classes, weights, owned_charms):
        """
        Perform a new spin:
          - Apply pending bonuses
          - Reset grid
          - Fill grid
        """
        self.apply_pending_bonuses()

        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.fill_cells(symbol_classes, weights, owned_charms)
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
        # Each retrigger charm has a 35% chance to trigger
        # ----------------------------------------------------
        retrigger_count = 0
        for d in owned_charms:
            if d['charm'].kind == "retrigger" and random.randint(1, 100) <= 35:
                retrigger_count += 1
        triggers = 1 + retrigger_count

        if retrigger_count > 0:
            print("I'm Bad At Math activated! Retriggering patterns...")
            sleep(0.75)

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
            # GOLDEN SYMBOLS → QUEUE DELAYED BONUS
            # ------------------------------------------------
            if golden_symbols:
                pending_increases = {}
                for s in golden_symbols:
                    stype = type(s)
                    pending_increases[stype] = pending_increases.get(stype, 0) + s.base_value

                for stype, increase in pending_increases.items():
                    total_increase = increase * triggers
                    self.delayed_bonuses.append({
                        "symbol_type": stype,
                        "increase": total_increase,
                        "delay": 1
                    })
                    print(
                        f"Golden symbol bonus queued! A delayed +{total_increase} bonus for all {stype.__name__}s has been queued for the next spin."
                    )

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

    def __init__(self, name, description, kind, target=None, amount=0, cooldown_rounds=0):
        self.name = name
        self.description = description
        self.kind = kind          # "extra_spin", "weight_active", "modifier", "retrigger"
        self.target = target      # Symbol class (Coin, Dice, etc.)
        self.amount = amount      # numeric effect (weight %, chance %, etc.)
        self.cooldown_rounds = cooldown_rounds

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
    "35% chance to trigger patterns one more time.",
    kind="retrigger"
)

Struck_Gold = Charm(
    "Struck Gold",
    "Activate to increase Coin spawn weight.",
    kind="weight_active",
    target=Coin,
    cooldown_rounds=3
)

Trick_Deck = Charm(
    "Trick Deck",
    "Activate to increase Card spawn weight.",
    kind="weight_active",
    target=Card,
    cooldown_rounds=3
)

ILoveTops = Charm(
    "I Love Tops",
    "Activate to increase Spinner spawn weight.",
    kind="weight_active",
    target=Spinner,
    cooldown_rounds=3
)

Dice_Hard = Charm(
    "Dice Hard",
    "Activate to increase Dice spawn weight.",
    kind="weight_active",
    target=Dice,
    cooldown_rounds=3
)

WheelOfFortune = Charm(
    "Wheel of Fortune",
    "Activate to increase Wheel spawn weight.",
    kind="weight_active",
    target=Wheel,
    cooldown_rounds=3
)

GoldenCoins = Charm(
    "Golden Coins",
    "25% chance for Coins to spawn with the GOLD modifier.",
    kind="modifier",
    target=Coin,
    amount=25
)

Rigged_Dice = Charm(
    "Rigged Dice",
    "20% chance for Dice to spawn with the GOLD modifier.",
    kind="modifier",
    target=Dice,
    amount=20
)

GoldenSpinners = Charm(
    "Golden Spinners",
    "30% chance for Spinners to spawn with the GOLD modifier.",
    kind="modifier",
    target=Spinner,
    amount=30
)

GoldenCards = Charm(
    "Golden Cards",
    "25% chance for Cards to spawn with the GOLD modifier.",
    kind="modifier",
    target=Card,
    amount=25
)

GoldenWheels = Charm(
    "Golden Wheels",
    "25% chance for Wheels to spawn with the GOLD modifier.",
    kind="modifier",
    target=Wheel,
    amount=25
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
    Rigged_Dice,
    GoldenSpinners,
    GoldenCards,
    GoldenWheels
]


# ============================================================
# CHARM HELPERS
# ============================================================

def compute_effective_max_spins(base_max_spins, owned_charms):
    """
    Extra spin charms increase max spins per round.
    """
    extra = sum(1 for d in owned_charms if d['charm'].kind == "extra_spin")
    return base_max_spins + extra


def compute_weight_overrides(symbol_classes, active_bonuses):
    """
    Compute weights with active bonuses, normalized to sum to 100.
    """
    weights = {}
    for cls in symbol_classes:
        if cls in active_bonuses:
            weights[cls] = active_bonuses[cls]
        else:
            base_w = getattr(cls, "weight", 1)
            weights[cls] = base_w

    # Normalize to sum 100
    total = sum(weights.values())
    if total > 0:
        for cls in weights:
            weights[cls] = weights[cls] * 100 / total

    return weights


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
    available = [c for c in ALL_CHARMS if c not in [d['charm'] for d in owned_charms]]

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
    owned_charms.append({'charm': chosen, 'uses': 0, 'cooldown': 0, 'last_increase': 0, 'activations_this_round': 0})

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
        print(f"Enter number of spins (max {max_spins}), 'store' to visit store, 'charm' to activate charms, or 'q' to quit.")
        choice = input("> ").strip().lower()

        if choice == "q":
            return "q"

        if choice == "store":
            return "store"

        if choice == "charm":
            return "charm"

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
# CHARM ACTIVATION PHASE
# ============================================================

def charm_phase(owned_charms, active_bonuses, symbol_classes=None):
    """
    Allow player to activate weight charms that are off cooldown.
    """
    if symbol_classes is None:
        symbol_classes = BASE_SYMBOL_CLASSES
    
    available = [d for d in owned_charms if d['cooldown'] == 0 and d['charm'].kind == "weight_active"]

    if not available:
        print("No weight charms available to activate.")
        return

    print("\nAvailable weight charms to activate:")
    for i, d in enumerate(available):
        charm = d['charm']
        target_name = charm.target.__name__ if charm.target else "Unknown"
        if d['last_increase'] == 0:
            print(f"{i+1}: {charm.name} (adds 20 to {target_name} weight)")
        else:
            next_increase = d['last_increase'] * 0.9
            print(f"{i+1}: {charm.name} (adds {next_increase:.1f} to {target_name} weight)")

    print("Enter the number to activate, or press Enter to skip.")

    choice = input("> ").strip()

    if not choice.isdigit():
        return

    idx = int(choice) - 1

    if 0 <= idx < len(available):
        d = available[idx]
        target_cls = d['charm'].target
        
        if d['activations_this_round'] == 0:
            # First activation this round: add 20 to target symbol
            increase = 20
            active_bonuses[target_cls] = active_bonuses.get(target_cls, getattr(target_cls, "weight", 1)) + increase
            d['last_increase'] = increase
            target_name = target_cls.__name__
            print(f"Activated {d['charm'].name}! {target_name} weight increased by {increase}.")
        else:
            # Subsequent activations this deadline: add 90% of last increase
            increase = d['last_increase'] * 0.9
            active_bonuses[target_cls] = active_bonuses[target_cls] + increase
            d['last_increase'] = increase
            target_name = target_cls.__name__
            print(f"Activated {d['charm'].name}! {target_name} weight increased by {increase:.1f}.")
        
        d['activations_this_round'] += 1
        d['uses'] += 1
        d['cooldown'] = 3


# ============================================================
# DEADLINE SYSTEM
# ============================================================

class DeadlineSystem:
    """
    Manages unlimited payment deadlines.
    Each deadline has 3 rounds:
      - Round 1/3: Can skip
      - Round 2/3: Can skip
      - Round 3/3: MANDATORY - cannot skip
    
    Deadline amounts increase by 300% (4x) each deadline:
      - Deadline 1: $100 per round
      - Deadline 2: $400 per round
      - Deadline 3: $1,600 per round
      - And so on...
    
    Rules:
    - Skip rounds 1 & 2 to accumulate debt
    - Round 3 must be paid or game ends
    - After completing deadline N round 3, move to deadline N+1 round 1
    """
    
    def __init__(self):
        self.current_deadline = 1  # Deadline number (1, 2, 3, ...)
        self.current_round = 1     # Round within deadline (1, 2, or 3)
        self.completed_rounds = []  # List of (deadline, round) tuples
        self.skipped_rounds = []    # List of (deadline, round) tuples
        self.accumulated_debt = 0
    
    def get_deadline_amount(self, deadline_num):
        """Calculate the cost for a given deadline: 100 * 4^(deadline-1)."""
        return int(100 * (4 ** (deadline_num - 1)))
    
    def get_current_deadline_amount(self):
        """Get the amount for the current deadline."""
        return self.get_deadline_amount(self.current_deadline)
    
    def get_current_total(self):
        """Get current amount + accumulated debt."""
        return self.get_current_deadline_amount() + self.accumulated_debt
    
    def get_breakdown(self):
        """Get breakdown of current vs accumulated debt."""
        current = self.get_current_deadline_amount()
        return {"current_round": current, "accumulated_debt": self.accumulated_debt, "total": self.get_current_total()}
    
    def can_skip(self):
        """Can skip if not round 3/3."""
        return self.current_round < 3
    
    def pay_deadline(self):
        """Mark current round as paid and move to next."""
        self.completed_rounds.append((self.current_deadline, self.current_round))
        self.accumulated_debt = 0
        
        if self.current_round == 3:
            # Move to next deadline
            self.current_deadline += 1
            self.current_round = 1
        else:
            # Move to next round in same deadline
            self.current_round += 1
    
    def skip_deadline(self):
        """Skip current round (adds to debt) and move to next."""
        if not self.can_skip():
            return False
        
        self.skipped_rounds.append((self.current_deadline, self.current_round))
        self.accumulated_debt += self.get_current_deadline_amount()
        
        if self.current_round == 3:
            # Move to next deadline
            self.current_deadline += 1
            self.current_round = 1
        else:
            # Move to next round in same deadline
            self.current_round += 1
        
        return True
    
    def display_status(self):
        """Display current deadline status."""
        breakdown = self.get_breakdown()
        cannotskip = " (MANDATORY)" if not self.can_skip() else ""
        
        print(f"\n{'='*50}")
        print(f"DEADLINE {self.current_deadline}, ROUND {self.current_round}/3{cannotskip}")
        print(f"{'='*50}")
        print(f"Current Round Cost:    ${breakdown['current_round']:,}")
        if breakdown['accumulated_debt'] > 0:
            print(f"Accumulated Debt:      ${breakdown['accumulated_debt']:,}")
        print(f"Total Payment Due:     ${breakdown['total']:,}")
        print(f"{'='*50}\n")
    
    def get_progress(self):
        """Get a summary of completed and upcoming deadlines."""
        print("\n" + "="*50)
        print("DEADLINE PROGRESS")
        print("="*50)
        
        # Show completed and skipped rounds
        if self.completed_rounds or self.skipped_rounds:
            all_processed = sorted(self.completed_rounds + self.skipped_rounds)
            for deadline_num, round_num in all_processed:
                amount = self.get_deadline_amount(deadline_num)
                status = ""
                if (deadline_num, round_num) in self.completed_rounds:
                    status = "✓ Completed"
                elif (deadline_num, round_num) in self.skipped_rounds:
                    status = "⏭ Skipped (Owed)"
                print(f"Deadline {deadline_num}, Round {round_num}/3: ${amount:,} - {status}")
        
        # Show current round
        current_amount = self.get_current_deadline_amount()
        print(f"Deadline {self.current_deadline}, Round {self.current_round}/3: ${current_amount:,} - ⏳ Current")
        
        # Calculate total paid
        total_paid = sum(self.get_deadline_amount(d) for d, r in self.completed_rounds)
        print(f"\nTotal Paid: ${total_paid:,}")
        if self.accumulated_debt > 0:
            print(f"Outstanding Debt: ${self.accumulated_debt:,}")
        print("="*50 + "\n")


# ============================================================
# MAIN GAME LOOP
# ============================================================

def main():
    print("Welcome to the Slot Machine Game!")
    sleep(0.75)

    money = 12
    BASE_MAX_SPINS = 8
    owned_charms = []
    active_bonuses = {}
    deadlines = DeadlineSystem()
 
    board = Board(3, 5)
    
    # Display initial deadline
    deadlines.display_status()

    while money > 0:
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

        if choice == "charm":
            charm_phase(owned_charms, active_bonuses, BASE_SYMBOL_CLASSES)
            continue

        spins = choice
        money -= spins

        # Update cooldowns and reset round activation counters at start of round
        for d in owned_charms:
            if d['cooldown'] > 0:
                d['cooldown'] -= 1
            d['activations_this_round'] = 0

        # Weight overrides from active bonuses
        weight_overrides = compute_weight_overrides(BASE_SYMBOL_CLASSES, active_bonuses)

        # Reset grand total for this round
        board.grand_total = 0

        # Perform spins
        for i in range(spins):
            print(f"\n--- SPIN {i+1} ---")
            board.current_spin(BASE_SYMBOL_CLASSES, weight_overrides, owned_charms)
            board.display_total(owned_charms)
            
            # Allow charm activation after each spin
            charm_phase(owned_charms, active_bonuses, BASE_SYMBOL_CLASSES)
            
            # Recalculate weights after charm activation
            weight_overrides = compute_weight_overrides(BASE_SYMBOL_CLASSES, active_bonuses)

        # Round summary
        print("\n==============================")
        print("      FINAL GRAND TOTAL")
        print("==============================")
        print(board.grand_total)
        print()

        # Add winnings
        money += board.grand_total
        print(f"You now have ${money}.\n")
        
        # Check if deadline payment is due
        deadlines.display_status()
        deadline_amount = deadlines.get_current_total()
        breakdown = deadlines.get_breakdown()
        while True:
            if money >= deadline_amount:
                options = []
                options.append("1. Pay deadline")
                
                if deadlines.can_skip():
                    options.append("2. Skip this round (you'll owe it later)")
                else:
                    options.append("(Round 3 is MANDATORY - cannot skip)")
                
                for opt in options:
                    print(opt)
                
                choice = input("> ").strip()
                
                if choice == "1":
                    money -= deadline_amount
                    print(f"Deadline paid! You now have ${money}.")
                    sleep(0.75)
                    deadlines.pay_deadline()
                    # Reset weight bonuses and charm tracking for the new round
                    active_bonuses = {}
                    for d in owned_charms:
                        if d['charm'].kind == "weight_active":
                            d['activations_this_round'] = 0
                            d['last_increase'] = 0
                    deadlines.display_status()
                    break
                elif choice == "2" and deadlines.can_skip():
                    prev_deadline = deadlines.current_deadline
                    prev_round = deadlines.current_round
                    deadlines.skip_deadline()
                    print(f"Skipped Deadline {prev_deadline}, Round {prev_round}/3!")
                    print(f"Debt accumulated. You'll owe ${deadlines.accumulated_debt:,} in future rounds.")
                    sleep(0.75)
                    # Reset weight bonuses and charm tracking for the new round
                    active_bonuses = {}
                    for d in owned_charms:
                        if d['charm'].kind == "weight_active":
                            d['activations_this_round'] = 0
                            d['last_increase'] = 0
                    deadlines.display_status()
                    break
                else:
                    print("Invalid choice. You must pay or skip.")
                    
            else:
                print(f"You don't have enough money to pay (need ${deadline_amount:,}, have ${money})")
                if deadlines.can_skip():
                    print("Would you like to skip this round and owe the debt?")
                    choice = input("Skip? (y/n) > ").strip().lower()
                    if choice == "y":
                        prev_deadline = deadlines.current_deadline
                        prev_round = deadlines.current_round
                        deadlines.skip_deadline()
                        print(f"Skipped Deadline {prev_deadline}, Round {prev_round}/3!")
                        print(f"You now owe ${deadlines.accumulated_debt:,}.")
                        sleep(0.75)
                        # Reset weight bonuses and charm tracking for the new round
                        active_bonuses = {}
                        for d in owned_charms:
                            if d['charm'].kind == "weight_active":
                                d['activations_this_round'] = 0
                                d['last_increase'] = 0
                        deadlines.display_status()
                        break
                    else:
                        print("Game over!")
                        money = 0
                        break
                else:
                    print("Round 3 is MANDATORY and cannot be skipped!")
                    print("Game over!")
                    money = 0
                    break


    # End game
    print("\n" + "="*40)
    if money <= 0:
        print("You lost all your money. Game over.")
        print("="*40)
    else:
        print("Thanks for playing!")
        print("="*40)


# ============================================================
# RUN GAME
# ============================================================

if __name__ == "__main__":
    main()
