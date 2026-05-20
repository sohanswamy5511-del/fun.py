import random
from time import sleep

ANSI_RED = "\033[31m"
ANSI_RESET = "\033[0m"
ANSI_CLEAR_SCREEN = "\033[2J\033[H"

# Phone and Achievement system
PHONE_UPGRADE_LEVEL = 0
ACHIEVEMENTS_UNLOCKED = set()
CURRENT_PHONE_ABILITY = None

PHONE_ABILITY_UNLOCKS = {
    0: ["common", "uncommon", "rare"],
    1: ["uncommon", "rare", "legendary"],
    2: ["rare", "legendary", "exotic"],
    3: ["legendary", "exotic", "transcendent"]
}

ALL_OBTAINABLE_ABILITIES = []

# ============================================================
# PHONE ABILITIES (WITH UPGRADE PROBABILITIES)
# ============================================================
# Rarity probabilities change based on phone upgrades
# Base: Common 50%, Uncommon 30%, Rare 20%,
# Upgrade 1: Common 0%, Uncommon 60%, Rare 35%, Legendary 5%
# Upgrade 2: Common 0%, Uncommon 40%, Rare 50%, Legendary 9%, Exotic 1%
# Upgrade 3: Common 0%, Uncommon 0%, Rare 70%, Legendary 20%, Exotic 9%, Transcendent 1%

PHONE_ABILITIES = [
    # COMMON TIER (50% base, 0% with upgrade 1+)
    {"num": 1, "name": "Increase value of patterns by base value", "rarity": "common", "desc": "All patterns gain their base value"},
    {"num": 2, "name": "Double values of certain symbols", "rarity": "common", "desc": "Randomly double one symbol type"},
    {"num": 3, "name": "Restore charges on cooldown charms", "rarity": "common", "desc": "Reset all charm cooldowns"},
    
    # UNCOMMON TIER (30% base, 60% upgrade 1, 40% upgrade 2, 0% upgrade 3)
    {"num": 4, "name": "+2 manifestation for a symbol", "rarity": "uncommon", "desc": "Average +2 extra of one symbol type for the rest of the deadline"},
    {"num": 5, "name": "Add a random trait to a charm", "rarity": "uncommon", "desc": "Enhance a charm with a trait"},
    {"num": 6, "name": "+1 charm space", "rarity": "uncommon", "desc": "Gain an extra charm slot"},
    
    # RARE TIER (15% base, 35% upgrade 1, 50% upgrade 2, 70% upgrade 3)
    {"num": 7, "name": "Remove mult options of a symbol", "rarity": "rare", "desc": "Simplify a symbol's multipliers"},
    {"num": 8, "name": "Increase Max mult of a symbol by 2", "rarity": "rare", "desc": "Higher multipliers for one symbol"},
    
    # LEGENDARY TIER (5% base, 5% upgrade 1, 9% upgrade 2, 20% upgrade 3)
    {"num": 9, "name": "Double Heads mult of coin", "rarity": "legendary", "desc": "Coin Heads becomes 10x instead of 5x"},
    {"num": 10, "name": "Remove all multipliers except 1 from a symbol", "rarity": "legendary", "desc": "Simplify a symbol's multipliers drastically"},
    {"num": 11, "name": "All cooldown charms take 1 less charge to recharge", "rarity": "legendary", "desc": "Speed up charm cooldowns (minimum 1)"},
    {"num": 12, "name": "+1 charm space", "rarity": "legendary", "desc": "Gain an extra charm slot (cannot be used 3+ times)"},
    {"num": 13, "name": "Increase max mult of all symbols by 10", "rarity": "legendary", "desc": "All symbols roll higher multipliers"},
    {"num": 14, "name": "Debt Decreases by 50%", "rarity": "legendary", "desc": "Next deadline amount reduced (uncopyable)"},
    {"num": 15, "name": "Apply a random trait to all charms", "rarity": "legendary", "desc": "Enhance all active charms (cannot apply eternal)"},
    {"num": 16, "name": "All patterns trigger one more time", "rarity": "legendary", "desc": "Every pattern gets +1 trigger permanently"},
    
    # EXOTIC TIER (1% upgrade 2, 9% upgrade 3)
    {"num": 17, "name": "I CAN LIVE FOREVER", "rarity": "exotic", "desc": "Give eternal trait to a charm (immune to destruction)"},
    {"num": 18, "name": "Spawn exotic charm & reset", "rarity": "exotic", "desc": "Spawn exotic charm, reset deadline, discard non-exotic/eternal charms"},
    {"num": 19, "name": "GODSMOS", "rarity": "exotic", "desc": "ALL charms trigger 1 more time permanently (does not reappear)"},
    {"num": 20, "name": "^1.2 to all patterns and symbols", "rarity": "exotic", "desc": "Multiply all pattern and symbol values permanently"},
    {"num": 21, "name": "^1.15 patterns, ^1.3 symbols, ^1.1 earnings", "rarity": "exotic", "desc": "Separate multipliers to each aspect"},
    {"num": 22, "name": "Gain 10% of deadline each round", "rarity": "exotic", "desc": "Passive income based on deadline (uncopyable, no reappear)"},
    {"num": 23, "name": "Apply trait to all charms & store", "rarity": "exotic", "desc": "All store charms get traits from now on"},
    {"num": 24, "name": "All charms cost 1 less", "rarity": "exotic", "desc": "Store charms now cost 1 less permanently (minimum FREE)"},
    
    # TRANSCENDENT TIER (1% upgrade 3)
    {"num": 25, "name": "Spawn 2 exotic charms", "rarity": "transcendent", "desc": "Add 2 exotic charms without destroying others"},
    {"num": 26, "name": "Spawn essence of the gods", "rarity": "transcendent", "desc": "Mysterious artifact appears (effects unknown)"},
]

def get_available_phone_abilities():
    """Return phone abilities available at the current phone upgrade level."""
    level = min(max(PHONE_UPGRADE_LEVEL, 0), max(PHONE_ABILITY_UNLOCKS.keys()))
    allowed_rarities = PHONE_ABILITY_UNLOCKS.get(level, ["common", "uncommon", "rare"])
    available = [ability for ability in PHONE_ABILITIES if ability["rarity"] in allowed_rarities]
    return available if available else PHONE_ABILITIES


def get_phone_ability_options():
    """Return a random sample of up to 3 obtainable phone abilities."""
    global ALL_OBTAINABLE_ABILITIES
    obtainable = get_available_phone_abilities()
    sample_size = min(3, len(obtainable))
    ALL_OBTAINABLE_ABILITIES = random.sample(obtainable, sample_size)
    return ALL_OBTAINABLE_ABILITIES


def show_phone_abilities():
    """Display available phone abilities for the player to choose from."""
    global CURRENT_PHONE_ABILITY
    
    available_abilities = get_phone_ability_options()

    print("\n" + "="*50)
    print(f"📞 PHONE ABILITIES - Choose one (Upgrade level {PHONE_UPGRADE_LEVEL}):")
    print("="*50)
    
    for idx, ability in enumerate(available_abilities, start=1):
        print(f"{idx}. {ability['name']} [{ability['rarity'].upper()}]")
        print(f"   {ability['desc']}")
    
    print("\nEnter the number of the ability to select, or 0 to skip:")
    
    while True:
        choice = input("> ").strip()
        
        if choice == "0":
            print("No ability selected.")
            CURRENT_PHONE_ABILITY = None
            break
        
        if not choice.isdigit():
            print("Invalid choice. Please enter a number.")
            continue
        
        choice_num = int(choice)
        
        if choice_num < 0 or choice_num > len(available_abilities):
            print(f"Invalid choice. Please enter 0-{len(available_abilities)}.")
            continue
        
        if choice_num == 0:
            print("No ability selected.")
            CURRENT_PHONE_ABILITY = None
            break
        
        selected = available_abilities[choice_num - 1]
        CURRENT_PHONE_ABILITY = selected
        print(f"✅ Selected: {selected['name']}")
        break
    
    print()

def trigger_button():
    """Activate the current phone ability."""
    if CURRENT_PHONE_ABILITY:
        print(f"📞 PHONE ABILITY TRIGGERED: {CURRENT_PHONE_ABILITY['name']}")
    else:
        print("No phone ability selected.")

def add_achievement(name):
    if name not in ACHIEVEMENTS_UNLOCKED:
        ACHIEVEMENTS_UNLOCKED.add(name)
        print(f"🏆 ACHIEVEMENT UNLOCKED: {name}")

# ============================================================
# ACHIEVEMENTS
# ============================================================
ACHIEVEMENTS_LIST = [
    "Score a Jackpot",
    "True Player: Unlock the World Ender",
    "777: Score your first 777",
    "Phone titan: Have all phone upgrades",
    "Trait master: All charms on table have traits",
    "#: Get into the numbers with hyperions",
    "Exotic master: Get all exotic charms",
    "Unlucky: Score no coins in a round",
    "Even Unluckier: Score no coins in a deadline",
    "I… Lost?: Lose",
    "Button master: Trigger button 5 times before spin",
    "Hey that's ME: Fuse to get Sohan Swamy"
]

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

    def fill_cells(self, symbol_classes, weights, owned_charms, active_bonuses):
        """
        Fill empty cells with symbols, applying:
          - Weight overrides
          - Global bonuses
          - Recharge/repeat modifier effects
          - Golden modifier chance
          - Activation (roll/spin/draw)
        """

        # Build weights list in order
        weights_list = [weights[cls] for cls in symbol_classes]

        # Check charms
        has_golden_coins = any(d['charm'].kind == "modifier" and d['charm'].target is Coin for d in owned_charms)
        has_golden_dice = any(d['charm'].kind == "modifier" and d['charm'].target is Dice for d in owned_charms)
        has_golden_spinners = any(d['charm'].kind == "modifier" and d['charm'].target is Spinner for d in owned_charms)
        has_golden_cards = any(d['charm'].kind == "modifier" and d['charm'].target is Card for d in owned_charms)
        has_golden_wheels = any(d['charm'].kind == "modifier" and d['charm'].target is Wheel for d in owned_charms)
        battery_chance = sum(d['charm'].amount for d in owned_charms if d['charm'].kind == "battery_modifier")
        repetition_chance = sum(d['charm'].amount for d in owned_charms if d['charm'].kind == "repetition_modifier")

        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y] is None:

                    # Choose symbol class
                    symbol_class = random.choices(symbol_classes, weights=weights_list, k=1)[0]
                    symbol = symbol_class()

                    # Apply permanent global bonus
                    bonus = self.global_symbol_bonuses.get(symbol_class, 0)
                    if bonus:
                        symbol.current_value += bonus

                    # Activate (roll/spin/draw)
                    symbol.activate()

                    # Random battery/repeat modifiers from owned charms
                    if battery_chance and random.randint(1, 100) <= battery_chance:
                        symbol.current_value += 1
                        symbol.display_name += " [RECHARGE]"

                    if repetition_chance and random.randint(1, 100) <= repetition_chance:
                        symbol.current_value *= 1.2
                        symbol.display_name += " [REPEAT]"

                    # Golden modifier chance
                    if isinstance(symbol, Coin) and has_golden_coins:
                        if random.randint(1, 100) <= 25:
                            symbol.is_golden = True
                            symbol.display_name += " [GOLD]"

                    if isinstance(symbol, Dice) and has_golden_dice:
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

    def current_spin(self, symbol_classes, weights, owned_charms, active_bonuses, spin_number=None):
        """
        Perform a new spin:
          - Apply pending bonuses
          - Reset grid
          - Fill grid
        """
        self.apply_pending_bonuses()

        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.fill_cells(symbol_classes, weights, owned_charms, active_bonuses)
        self.print_board(spin_number=spin_number)
        sleep(1)

    # --------------------------------------------------------
    # PRINT BOARD
    # --------------------------------------------------------

    def print_board(self, pattern_cells=None, pattern_score=None, spin_number=None):
        print(ANSI_CLEAR_SCREEN, end="")
        sleep(0.25)

        if spin_number is not None:
            print(f"--- SPIN {spin_number} ---")
        print("\n=== BOARD ===")

        highlighted_cells = set()
        score_row = None
        if pattern_cells:
            highlighted_cells = {
                (x, y)
                for _, cells in pattern_cells
                for x, y in cells
            }
            if pattern_score is not None:
                for x, cells in pattern_cells:
                    if cells:
                        score_row = min(x for x, _ in cells)
                        break

        for x, row in enumerate(self.grid):
            row_cells = []
            for y, s in enumerate(row):
                cell_text = f"{s.display_name:14}"
                if (x, y) in highlighted_cells:
                    cell_text = f"{ANSI_RED}{cell_text}{ANSI_RESET}"
                row_cells.append(cell_text)

            line = " | ".join(row_cells)
            if score_row == x and pattern_score is not None:
                line = f"{line}    Score: {pattern_score}"
            print(line)

        print("=============")

        if pattern_cells:
            sleep(1)
        print()

    # --------------------------------------------------------
    # SCORING
    # --------------------------------------------------------

    def display_total(self, owned_charms, spin_number=None):
        """
        Score all patterns:
          - Detect matches
          - Apply golden modifier
          - Apply retrigger logic
          - Add delayed bonuses
        Returns the number of patterns scored this spin (stored as instance variable).
        """
        self.patterns_scored_this_spin = 0  # Initialize counter

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

        # Check for achievements
        if any(pattern.name == "Jackpot" for pattern, _ in all_matches):
            add_achievement("Score a Jackpot")

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

        # Store for print output
        self.last_patterns = chosen

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
        patterns_this_spin = len(chosen)

        has_gold_rush = has_charm(owned_charms, "Gold Rush")

        for pattern, cells in chosen:
            pattern_sum = sum(self.grid[x][y].current_value for x, y in cells)
            pattern_score = pattern.get_multiplier(pattern_sum) * triggers
            self.print_board(pattern_cells=[(pattern.name, cells)], pattern_score=pattern_score, spin_number=spin_number)
            total += pattern_score

            if has_gold_rush:
                golden_symbols = [self.grid[x][y] for x, y in cells if self.grid[x][y].is_golden]
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

            sleep(1.5)

        # ----------------------------------------------------
        # UPDATE DELAYED BONUSES
        # ----------------------------------------------------
        for bonus in self.delayed_bonuses:
            bonus["delay"] -= 1

        # ----------------------------------------------------
        # FINAL OUTPUT
        # ----------------------------------------------------
        total_matches = patterns_this_spin * triggers
        print("\n=========================")
        print(f"Total Matches: {total_matches}")
        print(f"Total Value: {total}")
        print("=========================\n")
        sleep(1)
        self.grand_total += total
        self.patterns_scored_this_spin = total_matches
        return total


# ============================================================
# CHARM SYSTEM
# ============================================================

class Charm:
    """
    A charm modifies gameplay in one of several ways:
      - extra_spin: +1 max spin per round
      - weight_active: increases spawn weight of a symbol type
      - modifier: chance for symbols to spawn golden
      - retrigger: patterns trigger one extra time
      - cooldown: has cooldown-based activation
      - passive: always active
      - trait: applies modifier to other charms
    """

    def __init__(self, name, description, kind, target=None, amount=0, cooldown_rounds=0, rarity="common"):
        self.name = name
        self.description = description
        self.kind = kind
        self.target = target
        self.amount = amount
        self.cooldown_rounds = cooldown_rounds
        self.rarity = rarity

    def __str__(self):
        return f"{self.name}: {self.description}"


# ============================================================
# CHARM DEFINITIONS - COMMON TIER (50% spawn rate base)
# ============================================================

# Luck charms
Tomato = Charm(
    "Tomato",
    "+3 luck for next spin (17.5% trigger chance)",
    kind="luck",
    amount=3,
    rarity="common"
)

Peach = Charm(
    "Peach",
    "+5 luck for next spin (10% trigger chance)",
    kind="luck",
    amount=5,
    rarity="common"
)

# Golden Charms (existing)
GoldenWheels = Charm(
    "Golden Wheels",
    "25% chance for Wheels to spawn with GOLD modifier",
    kind="modifier",
    target=Wheel,
    amount=25,
    rarity="common"
)

GoldenDice = Charm(
    "Golden Dice",
    "20% chance for Dice to spawn with GOLD modifier",
    kind="modifier",
    target=Dice,
    amount=20,
    rarity="common"
)

GoldenCoins = Charm(
    "Golden Coins",
    "25% chance for Coins to spawn with GOLD modifier",
    kind="modifier",
    target=Coin,
    amount=25,
    rarity="common"
)

GoldenSpinners = Charm(
    "Golden Spinners",
    "30% chance for Spinners to spawn with GOLD modifier",
    kind="modifier",
    target=Spinner,
    amount=30,
    rarity="common"
)

GoldenCards = Charm(
    "Golden Cards",
    "25% chance for Cards to spawn with GOLD modifier",
    kind="modifier",
    target=Card,
    amount=25,
    rarity="common"
)

# ============================================================
# CHARM DEFINITIONS - UNCOMMON TIER (30% spawn rate base)
# ============================================================


# Extra spin charm
Spare_Change = Charm(
    "Spare Change",
    "Gain +1 max spin per round",
    kind="extra_spin",
    rarity="uncommon"
)

# Weight-active charms (cooldown based)
Struck_Gold = Charm(
    "Struck Gold",
    "Activate to increase Coin spawn weight",
    kind="weight_active",
    target=Coin,
    cooldown_rounds=3,
    rarity="uncommon"
)

Trick_Deck = Charm(
    "Trick Deck",
    "Activate to increase Card spawn weight",
    kind="weight_active",
    target=Card,
    cooldown_rounds=3,
    rarity="uncommon"
)

ILoveTops = Charm(
    "I Love Tops",
    "Activate to increase Spinner spawn weight",
    kind="weight_active",
    target=Spinner,
    cooldown_rounds=3,
    rarity="uncommon"
)

Dice_Hard = Charm(
    "Dice Hard",
    "Activate to increase Dice spawn weight",
    kind="weight_active",
    target=Dice,
    cooldown_rounds=3,
    rarity="uncommon"
)

WheelOfFortune = Charm(
    "Wheel of Fortune",
    "Activate to increase Wheel spawn weight",
    kind="weight_active",
    target=Wheel,
    cooldown_rounds=3,
    rarity="uncommon"
)

# ============================================================
# CHARM DEFINITIONS - RARE TIER (20% spawn rate base)
# ============================================================

ImBadAtMath = Charm(
    "I'm Bad At Math",
    "35% chance to trigger patterns one more time",
    kind="retrigger",
    rarity="rare"
)

Score5Patterns = Charm(
    "Pattern Doubler",
    "When you score 5 patterns, double all symbol values until end of round",
    kind="conditional_mult",
    rarity="rare"
)

NoPatternBoost = Charm(
    "Clutch Play",
    "When you score no patterns, double symbol/pattern mults and 1.5x earnings",
    kind="conditional_mult",
    rarity="rare"
)

EarningsMultUp = Charm(
    "Earnings Boost",
    "Earnings mult +1 (doesn't take space)",
    kind="earnings_mult",
    rarity="rare"
)

SymbolsMultUp = Charm(
    "Symbol Power",
    "Symbols mult +1 permanently (cooldown 2)",
    kind="symbols_mult",
    cooldown_rounds=2,
    rarity="rare"
)

PatternsMultScaling = Charm(
    "Pattern Scaling",
    "Patterns mult +1 for every 1.5x deadline earned",
    kind="patterns_mult_scaling",
    rarity="rare"
)

NO_CHANGE = Charm(
    "NOCHANGE",
    "Patterns containing symbols other than Coin trigger one more time (cooldown 4)",
    kind="pattern_retrigger_non_coin",
    cooldown_rounds=4,
    rarity="rare"
)

CoinExtraTrigger = Charm(
    "Coin Rush",
    "Patterns containing only Coins trigger two more times (cooldown 5)",
    kind="pattern_retrigger_coin",
    cooldown_rounds=5,
    rarity="rare"
)

# ============================================================
# CHARM DEFINITIONS - LEGENDARY TIER (5% spawn rate base)
# ============================================================

CCHARM = Charm(
    "CCHARM",
    "All cooldown charms trigger one more time",
    kind="cooldown_retrigger",
    rarity="legendary"
)

ProtestingCall = Charm(
    "Protesting Call",
    "All phone abilities trigger one more time",
    kind="phone_retrigger",
    rarity="legendary"
)

WorldRecordPepper = Charm(
    "World Record Pepper",
    "Score 15+ patterns in a spin = double all symbol values (resets end of deadline)",
    kind="conditional_mult_15",
    rarity="legendary"
)

GiantPeach = Charm(
    "Giant Peach",
    "Score 30+ patterns in a spin = double patterns and symbols (resets end of deadline)",
    kind="conditional_mult_30",
    rarity="legendary"
)

LargestTomato = Charm(
    "The Largest Tomato Ever",
    "Score 50+ patterns = double value, then triple, then quad, etc. (resets end of deadline)",
    kind="conditional_mult_exponential",
    rarity="legendary"
)

PSA15 = Charm(
    "PSA 15",
    "Charms giving +1 to mult now give +10 to patterns, x1.5 to symbols",
    kind="mult_boost",
    rarity="legendary"
)

Flowers = Charm(
    "Flowers",
    "Increase value of all symbols every other pattern (resets end of deadline)",
    kind="alternating_boost",
    rarity="legendary"
)

INeedToStopWinning = Charm(
    "I NEED TO STOP WINNING",
    "Jackpots don't occur - one random cell changes symbol instead (requires 6 charges)",
    kind="jackpot_prevention",
    cooldown_rounds=6,
    rarity="legendary"
)

GoldRush = Charm(
    "Gold Rush",
    "If >=1 symbol has GOLD modifier, increase its value by base value per trigger, permanently",
    kind="gold_amplifier",
    rarity="legendary"
)

# ============================================================
# CHARM DEFINITIONS - EXOTIC TIER (SPAWNED FROM PHONE ABILITIES ONLY)
# ============================================================

QuantProfessor = Charm(
    "Quant Professor",
    "Earnings mult doubles every time you score a jackpot with all symbols mult=1",
    kind="exotic_earnings",
    rarity="exotic"
)

IsThisBroken = Charm(
    "Is this broken?",
    "Symbols and patterns mult triple every jackpot with all symbols mult=1",
    kind="exotic_triple",
    rarity="exotic"
)

TenXMult = Charm(
    "+10xmult",
    "Jackpot of all symbols with mult=1 converts to +10 xmult per symbol",
    kind="exotic_xmult",
    rarity="exotic"
)

CoinTailsBoost = Charm(
    "^^1.1",
    "+1 then ^1.7 coin tails mult every jackpot of all tails (resets end of round)",
    kind="exotic_tails",
    rarity="exotic"
)

ExponentialMult = Charm(
    "^^^2",
    "^1.5 any symbol xmult every jackpot of least value xmult (resets end of round)",
    kind="exotic_exponential",
    rarity="exotic"
)

ExponentialGrowth = Charm(
    "Exponential Mult is broken",
    "^1 base, gains ^0.01 for every jackpot pattern trigger",
    kind="exotic_growth",
    rarity="exotic"
)

AlwaysOn = Charm(
    "Always On",
    "50% chance for button to not consume charges when pressed",
    kind="button_preservation",
    rarity="exotic"
)

TheSeraphim = Charm(
    "The Seraphim",
    "When you score all patterns except Jackpot, ^3 to symbols and patterns (resets end of round)",
    kind="exotic_seraphim",
    rarity="exotic"
)

Blood = Charm(
    "Blood",
    "+5% chance for symbols to have any symbol modifier",
    kind="modifier_chance",
    amount=5,
    rarity="exotic"
)

Soul = Charm(
    "Soul",
    "+5% chance for symbols to have battery modifier",
    kind="battery_modifier",
    amount=5,
    rarity="exotic"
)

Body = Charm(
    "Body",
    "+5% chance for symbols to have repetition modifier",
    kind="repetition_modifier",
    amount=5,
    rarity="exotic"
)

SevenDeadlySins = Charm(
    "7 Deadly Sins",
    "5% chance to get three 7s on board (1,1)(1,2)(1,3). Reward ^^2 coins earned this round",
    kind="seven_multiplier",
    rarity="exotic"
)

InfiniteStorage = Charm(
    "Infinite Storage",
    "+1 charm space for every 5+ jackpots in spin, +1 for each jackpot after 10th",
    kind="space_scaling",
    rarity="exotic"
)

RELOADING = Charm(
    "RELOADING",
    "All symbols gain 1/9 of current value every shop restock. Restock costs /2",
    kind="shop_scaling",
    rarity="exotic"
)

# ============================================================
# CHARM DEFINITIONS - TRANSCENDENCE (THE END OF THE UNIVERSE)
# ============================================================

THEWORLDENDER = Charm(
    "THE WORLD ENDER",
    "20% symbol modifier chance (apply 2x). All xmults treated as x1. +4 luck. Activate: all values gain [x]x, 777 gain [x^2]x. X increases by 1 per 5 jackpots. Spawn 777 next spin. +1 charm space permanently",
    kind="world_ender",
    cooldown_rounds=3,
    rarity="transcendent"
)

EssenceOfGods = Charm(
    "Essence of the Gods",
    "Seems like it doesn't do anything…yet",
    kind="mystery",
    rarity="transcendent"
)

# ============================================================
# CRAFTABLE CHARMS (RECIPES)
# ============================================================

CRAFTABLE_CHARMS = {
    "Phone Upgrade": {
        "name": "Phone Upgrade",
        "description": "Common calls 0% chance, legendary calls 5% chance",
        "requires": ["Protesting Call", "CCHARM", "Gold Rush"],
        "rarity": "craftable"
    },
    "Phone Upgrade MKII": {
        "name": "Phone Upgrade MKII",
        "description": "Exotic phone calls 1% spawn chance",
        "requires": ["Protesting Call", "CCHARM", "PSA 15", "Flowers"],
        "rarity": "craftable"
    },
    "Phone Upgrade MKIII": {
        "name": "Phone Upgrade MKIII",
        "description": "Transcendent calls 1% spawn, common 0%",
        "requires": ["CCHARM", "Protesting Call", "I NEED TO STOP WINNING", "Sohan Swamy", "Flowers", "Gold Rush"],
        "rarity": "craftable"
    },
    "Charm Upgrade": {
        "name": "Charm Upgrade",
        "description": "Legendary charms can spawn in store",
        "requires": ["I'm Bad At Math", "CCHARM"],  # Two retrigger charms
        "rarity": "craftable"
    },
    "//Symbol": {
        "name": "Symbol Upgrade",
        "description": "15% chance for any symbol to have any symbol modifier",
        "requires": ["I can't stop winning", "Re-Retrigger", "AGAINAGAINAGAIN"],
        "rarity": "craftable"
    },
    "Human": {
        "name": "Human Upgrade",
        "description": "+20% chance for symbols to have any modifier. Modifiers trigger twice. Max 4 per symbol",
        "requires": ["Soul", "Body", "Blood"],
        "rarity": "craftable_exotic"
    },
    "777": {
        "name": "777 Upgrade",
        "description": "Button triggers give 100% chance for 777. 777 value +^^0.01 per jackpot",
        "requires": ["7 Deadly Sins", "Giant Peach", "The Largest Tomato Ever"],
        "rarity": "craftable_exotic"
    },
    "Sohan Swamy": {
        "name": "Sohan Swamy",
        "description": "+1 value on all symbols",
        "requires": ["All Exotic Charms"],  # Requires all exotic charms
        "rarity": "craftable_exotic"
    },
    "THE WORLD ENDER": {
        "name": "THE WORLD ENDER",
        "description": "20% symbol modifier chance (apply 2x). All xmults treated as x1. +4 luck. Activate: all values gain [x]x, 777 gain [x^2]x. X increases by 1 per 5 jackpots. Spawn 777 next spin. +1 charm space permanently",
        "requires": ["Sohan Swamy", "EssenceOfGods x 3"],
        "rarity": "craftable_transcendent"
    }
}

# ============================================================
# ALL CHARMS LIST
# ============================================================

ALL_CHARMS = [
    # Common
    Tomato, Peach,
    GoldenWheels, GoldenDice, GoldenCoins, GoldenSpinners, GoldenCards,
    
    # Uncommon
    Spare_Change,
    Struck_Gold, Trick_Deck, ILoveTops, Dice_Hard, WheelOfFortune,
    
    # Rare
    ImBadAtMath,
    Score5Patterns, NoPatternBoost,
    EarningsMultUp, SymbolsMultUp, PatternsMultScaling,
    NO_CHANGE, CoinExtraTrigger,
    
    # Legendary
    CCHARM, ProtestingCall,
    WorldRecordPepper, GiantPeach, LargestTomato,
    PSA15, Flowers,
    INeedToStopWinning, GoldRush,
    
    # Exotic
    QuantProfessor, IsThisBroken, TenXMult,
    CoinTailsBoost, ExponentialMult, ExponentialGrowth,
    AlwaysOn, TheSeraphim, Blood, Soul, Body,
    SevenDeadlySins, InfiniteStorage, RELOADING,
    
    
    # Transcendency
    THEWORLDENDER, EssenceOfGods,
]

ALL_OBTAINABLE_CHARMS_LIST = [
    # Common
    Tomato, Peach,
    GoldenWheels, GoldenDice, GoldenCoins, GoldenSpinners, GoldenCards,
    
    # Uncommon
    Spare_Change,
    Struck_Gold, Trick_Deck, ILoveTops, Dice_Hard, WheelOfFortune,
    
    # Rare
    ImBadAtMath,
    Score5Patterns, NoPatternBoost,
    EarningsMultUp, SymbolsMultUp, PatternsMultScaling,
    NO_CHANGE, CoinExtraTrigger,
]

ALL_OBTAINABLE_LOCKED = [
    CCHARM, ProtestingCall,
    WorldRecordPepper, GiantPeach, LargestTomato,
    PSA15, Flowers,
    INeedToStopWinning, GoldRush,
]


def get_all_obtainable_charms(crafted_recipes=None):
    """Return the charms that can appear in the store.

    Legendary charms are only available after crafting Charm Upgrade.
    Exotic and transcendent charms are never available in the store.
    """
    obtainable = list(ALL_OBTAINABLE_CHARMS_LIST)
    if crafted_recipes and "Charm Upgrade" in crafted_recipes:
        obtainable += list(ALL_OBTAINABLE_LOCKED)
    return obtainable

# ============================================================
# CHARM HELPERS
# ============================================================

def compute_effective_max_spins(base_max_spins, owned_charms):
    """
    Extra spin charms increase max spins per round.
    """
    extra = sum(1 for d in owned_charms if d['charm'].kind == "extra_spin")
    return base_max_spins + extra


def compute_weight_overrides(symbol_classes, active_bonuses, owned_charms=None):
    """
    Compute weights with active bonuses and manifestation charms,
    then normalize to sum to 100.
    """
    weights = {}
    for cls in symbol_classes:
        if cls in active_bonuses:
            weights[cls] = active_bonuses[cls]
        else:
            base_w = getattr(cls, "weight", 1)
            weights[cls] = base_w

    if owned_charms:
        for d in owned_charms:
            if d['charm'].kind == "manifestation":
                if d.get('manifestation_target') is None:
                    d['manifestation_target'] = random.choice(symbol_classes)
                target_cls = d['manifestation_target']
                weights[target_cls] = weights.get(target_cls, getattr(target_cls, "weight", 1)) + 13.333

    # Normalize to sum 100
    total = sum(weights.values())
    if total > 0:
        for cls in weights:
            weights[cls] = weights[cls] * 100 / total

    return weights


def has_available_cooldown_charms(owned_charms):
    return any(d['cooldown'] == 0 and d['charm'].cooldown_rounds > 0 for d in owned_charms)




def requirements_met(owned_charms, requirement):
    if requirement == "All Exotic Charms":
        exotic_total = sum(1 for c in ALL_CHARMS if c.rarity == "exotic")
        return sum(1 for d in owned_charms if d['charm'].rarity == "exotic") >= exotic_total

    if " x " in requirement:
        name, count_str = requirement.rsplit(" x ", 1)
        if count_str.isdigit():
            return sum(1 for d in owned_charms if d['charm'].name == name) >= int(count_str)

    return any(d['charm'].name == requirement for d in owned_charms)


def get_available_craftables(owned_charms, crafted_recipes):
    available = []
    for recipe_name, recipe in CRAFTABLE_CHARMS.items():
        if recipe_name in crafted_recipes:
            continue
        if all(requirements_met(owned_charms, req) for req in recipe['requires']):
            available.append(recipe)
    return available


def craft_phase(owned_charms, crafted_recipes):
    global PHONE_UPGRADE_LEVEL
    available = get_available_craftables(owned_charms, crafted_recipes)
    if not available:
        print("No craftable recipes are available right now.")
        return crafted_recipes

    print("\n🛠️  Craftable recipes:")
    for idx, recipe in enumerate(available, start=1):
        print(f"{idx}. {recipe['name']} - {recipe['description']}")
    print("Enter the number of the recipe to craft, or press Enter to skip:")

    choice = input("> ").strip()
    if choice == "":
        print("No recipe crafted.")
        return crafted_recipes

    if not choice.isdigit():
        print("Invalid input. Crafting skipped.")
        return crafted_recipes

    idx = int(choice) - 1
    if idx < 0 or idx >= len(available):
        print("Invalid choice. Crafting skipped.")
        return crafted_recipes

    recipe = available[idx]
    recipe_name = recipe['name']
    crafted_recipes.add(recipe_name)

    if recipe_name == "Charm Upgrade":
        print("Charm Upgrade crafted! Legendary charms are now available in the store.")
    elif recipe_name == "Phone Upgrade":
        PHONE_UPGRADE_LEVEL = max(PHONE_UPGRADE_LEVEL, 1)
        print("Phone Upgrade crafted! Phone ability progression has advanced.")
    elif recipe_name == "Phone Upgrade MKII":
        PHONE_UPGRADE_LEVEL = max(PHONE_UPGRADE_LEVEL, 2)
        print("Phone Upgrade MKII crafted! Phone ability progression has advanced.")
    elif recipe_name == "Phone Upgrade MKIII":
        PHONE_UPGRADE_LEVEL = max(PHONE_UPGRADE_LEVEL, 3)
        print("Phone Upgrade MKIII crafted! Phone ability progression has advanced.")
    else:
        print(f"{recipe_name} crafted!")

    return crafted_recipes


def reset_manifestation_targets(owned_charms):
    """Reset manifestation targets when a new deadline begins."""
    for d in owned_charms:
        if d['charm'].kind == "manifestation":
            d['manifestation_target'] = None

# ============================================================
# STORE SYSTEM
# ============================================================

def store_phase(money, owned_charms, crafted_recipes):
    """
    Store logic:
      - Shows 4 random charms not yet owned
      - Charms cost $5
      - Player may buy one charm per visit
      - Exotic charms and THE WORLD ENDER are not available in shop
      - Legendary charms are only available after crafting Charm Upgrade
    """

    print("\nWelcome to the store.")
    print(f"You have ${money}. Charms cost $5 each.")

    # Filter out charms already owned.
    # Legendary charms become available only after crafting Charm Upgrade.
    available_chars = get_all_obtainable_charms(crafted_recipes)
    available = [
        c for c in available_chars
        if c not in [d['charm'] for d in owned_charms]
        and c.name != "THE WORLD ENDER"
    ]

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

def get_spin_amount(money, max_spins, owned_charms):
    """
    Ask the player how many spins they want.
    Options:
      - Enter a number (1 to max_spins)
      - Enter 'store' to visit the store
      - Enter 'craft' to craft recipes
      - Enter 'charm' to activate charms
      - Enter 'deadline_pay' to pay the deadline early
      - Enter 'q' to quit
    """

    while True:
        print(f"You have ${money}. Each spin costs $1.")
        options = [f"number of spins (max {max_spins})", "'store' to visit store", "'craft' to craft recipes", "'charm' to activate charms", "'deadline_pay' to pay the deadline early", "'q' to quit"]
        print("Enter " + ", ".join(options))
        choice = input("> ").strip().lower()

        if choice == "q":
            return "q"

        if choice == "store":
            return "store"

        if choice == "craft":
            return "craft"

        if choice == "charm":
            return "charm"

        if choice == "deadline_pay":
            return "deadline_pay"

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
# AUTO‑ACTIVATE‑ALL CHARM PHASE (UPDATED)
# ============================================================

def charm_phase(owned_charms, active_bonuses, symbol_classes=None):
    """
    UPDATED BEHAVIOR:
    When the player types 'charm', ALL cooldown-based charms that are off cooldown
    automatically activate, in order, with no menu.
    
    This includes:
      - weight_active charms (Struck Gold, Trick Deck, etc.)
      - Any other charm with cooldown_rounds > 0 and currently available
    
    Each charm keeps its own diminishing-return chain.
    """

    if symbol_classes is None:
        symbol_classes = BASE_SYMBOL_CLASSES

    # All charms with cooldowns that are currently available
    available = [d for d in owned_charms if d['cooldown'] == 0 and d['charm'].cooldown_rounds > 0]

    if not available:
        print("No cooldown charms available to activate.")
        return

    print("\n🎯 Activating ALL available cooldown charms...")

    for d in available:
        charm = d['charm']
        
        # Handle weight_active charms
        if charm.kind == "weight_active":
            target_cls = charm.target
            target_name = target_cls.__name__

            # First activation this round
            if d['activations_this_round'] == 0:
                increase = 20
                active_bonuses[target_cls] = active_bonuses.get(target_cls, getattr(target_cls, "weight", 1)) + increase
                d['last_increase'] = increase
                print(f"  ✓ {charm.name}: {target_name} weight +{increase}")

            else:
                # Subsequent activations: 90% of last increase (diminishing returns)
                increase = d['last_increase'] * 0.9
                active_bonuses[target_cls] = active_bonuses[target_cls] + increase
                d['last_increase'] = increase
                print(f"  ✓ {charm.name} (again): {target_name} weight +{increase:.1f}")

        # Handle other cooldown charms
        else:
            print(f"  ✓ {charm.name} activated!")

        d['activations_this_round'] += 1
        d['uses'] += 1
        d['cooldown'] = charm.cooldown_rounds
    
    print()


# ============================================================
# CHARM EFFECT HELPERS
# ============================================================

def get_charm_space_used(owned_charms):
    """Calculate how many charm slots are currently used."""
    return len(owned_charms)

def get_modifier_chance_bonus(owned_charms):
    """Calculate total % bonus to symbol modifier chance from charms."""
    bonus = 0
    for d in owned_charms:
        charm = d['charm']
        if charm.kind == "modifier_chance":
            bonus += charm.amount
    return bonus

def apply_charm_effects(owned_charms, board, patterns_scored=0):
    """
    Apply passive charm effects:
    - modifier_chance: increase symbol modifier spawn chances
    - Infinite Storage: increase charm space if 5+ jackpots
    - World Ender effects: passive +4 luck, modifier doubling, etc.
    """
    effects = {
        'modifier_chance_bonus': 0,
        'luck_bonus': 0,
        'earnings_mult': 1.0,
        'symbols_mult': 1.0,
        'patterns_mult': 1.0
    }
    
    for d in owned_charms:
        charm = d['charm']
        
        if charm.kind == "modifier_chance":
            effects['modifier_chance_bonus'] += charm.amount
        elif charm.kind == "world_ender":
            effects['luck_bonus'] += 4
    
    return effects

def has_charm(owned_charms, charm_name):
    """Check if player has a specific charm."""
    return any(d['charm'].name == charm_name for d in owned_charms)

def count_charm_by_rarity(owned_charms, rarity):
    """Count how many charms of a specific rarity the player has."""
    return sum(1 for d in owned_charms if d['charm'].rarity == rarity)


# ============================================================
# DEADLINE SYSTEM
# ============================================================

class DeadlineSystem:
    """
    Deadline system with 3-round progression per deadline.
    
    - Each deadline lasts 3 rounds
    - Display "X rounds left" (starting at 3)
    - After each set of spins, rounds decrement
    - When rounds reach 0 rounds left, payment is MANDATORY
    - After payment, reset to 3 rounds left for next deadline
    - Deadline amounts increase by 300% (4x) each payment
    """

    def __init__(self):
        self.current_deadline = 1
        self.rounds_left = 3
        self.payments_made = 0

    def get_deadline_amount(self, deadline_num):
        """Calculate deadline amount based on deadline number."""
        return int(100 * (4 ** (deadline_num - 1)))

    def get_current_total(self):
        """Return the current amount owed."""
        return self.get_deadline_amount(self.current_deadline)

    def get_status_string(self):
        """Return display string for rounds and deadline."""
        return f"💀 DEADLINE {self.current_deadline} | {self.rounds_left} rounds left | ${self.get_current_total():,}"

    def decrement_round(self):
        """Decrement rounds after a set of spins is completed."""
        self.rounds_left -= 1

    def must_pay(self):
        """Check if payment is mandatory (rounds reached 0)."""
        return self.rounds_left == 0

    def pay_deadline(self):
        """Pay the deadline and advance to next one."""
        self.current_deadline += 1
        self.rounds_left = 3
        self.payments_made += 1
    
    def can_choose_phone_ability(self):
        """Check if the player can choose a phone ability (deadline 2 or higher)."""
        return self.current_deadline >= 2


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
    crafted_recipes = set()
    charm_space_max = 6  # Start with 6 max charm slots
    deadlines = DeadlineSystem()

    board = Board(3, 5)

    # Display initial deadline info
    print(deadlines.get_status_string())
    print()

    while money > 0:
        max_spins = compute_effective_max_spins(BASE_MAX_SPINS, owned_charms)
        choice = get_spin_amount(money, max_spins, owned_charms)

        if choice == "q":
            print("Thanks for playing!")
            break

        if choice == "store":
            result = store_phase(money, owned_charms, crafted_recipes)
            if result:
                money, owned_charms = result
            continue

        if choice == "craft":
            crafted_recipes = craft_phase(owned_charms, crafted_recipes)
            continue


        if choice == "charm":
            charm_phase(owned_charms, active_bonuses, BASE_SYMBOL_CLASSES)
            continue

        if choice == "deadline_pay":
            # Handle mandatory deadline payment
            deadline_amount = deadlines.get_current_total()
            if money >= deadline_amount:
                money -= deadline_amount
                print(f"Deadline paid! You now have ${money}.")
                sleep(0.75)
                deadlines.pay_deadline()
                active_bonuses = {}
                for d in owned_charms:
                    if d['charm'].kind == "weight_active":
                        d['activations_this_round'] = 0
                        d['last_increase'] = 0
                reset_manifestation_targets(owned_charms)
                print(deadlines.get_status_string())
            else:
                print(f"Insufficient funds. Need ${deadline_amount:,}, have ${money}.")
            continue

        if choice == "button":
            trigger_button()
            continue

        spins = choice
        money -= spins

        # Update cooldowns and reset round activation counters
        for d in owned_charms:
            if d['cooldown'] > 0:
                d['cooldown'] -= 1
            d['activations_this_round'] = 0

        weight_overrides = compute_weight_overrides(BASE_SYMBOL_CLASSES, active_bonuses, owned_charms)
        board.grand_total = 0
        patterns_scored_this_round = 0  # Track total patterns for conditional charms

        # Perform spins
        for i in range(spins):
            board.current_spin(BASE_SYMBOL_CLASSES, weight_overrides, owned_charms, active_bonuses, spin_number=i+1)
            board.display_total(owned_charms, spin_number=i+1)
            patterns_scored_this_round += board.patterns_scored_this_spin

            if spins != 0 and has_available_cooldown_charms(owned_charms):
                print("\n📜 Activate charms? (type 'charm' to activate, or press Enter to skip)")
                charm_input = input("> ").strip().lower()
                if charm_input == "charm":
                    charm_phase(owned_charms, active_bonuses, BASE_SYMBOL_CLASSES)
            
            # Check and trigger conditional charms based on patterns this spin
            patterns_this_spin = board.patterns_scored_this_spin
            
            # WorldRecordPepper: 15+ patterns = double symbol values
            if patterns_this_spin >= 15 and has_charm(owned_charms, "World Record Pepper"):
                print("🌶️ WORLD RECORD PEPPER TRIGGERED! All symbols doubled until end of round!")
            
            # GiantPeach: 30+ patterns = double patterns and symbols
            if patterns_this_spin >= 30 and has_charm(owned_charms, "Giant Peach"):
                print("🍑 GIANT PEACH TRIGGERED! All patterns and symbols doubled until end of round!")
            
            # LargestTomato: 50+ patterns = exponential doubling
            if patterns_this_spin >= 50 and has_charm(owned_charms, "The Largest Tomato Ever"):
                print("🍅 THE LARGEST TOMATO EVER TRIGGERED! Values multiplying exponentially!")

        # Decrement round after all spins are completed
        deadlines.decrement_round()

        # Round summary
        print("\n==============================")
        print("      FINAL GRAND TOTAL")
        print("==============================")
        print(board.grand_total)
        print()

        money += board.grand_total
        print(f"You now have ${money}.\n")

        # Win condition
        if money >= 1000000:
            print("WIN: You have reached $1,000,000! You can now craft the Grabber charm to continue playing.")
            add_achievement("Reach 1 Million")

        # Deadline display and check
        print(deadlines.get_status_string())
        
        if deadlines.must_pay():
            # Mandatory payment - rounds reached 0
            deadline_amount = deadlines.get_current_total()
            
            if money < deadline_amount:
                # Not enough money - GAME OVER
                print(f"\n💀 GAME OVER! You don't have enough money to pay ${deadline_amount:,}.")
                print(f"You only have ${money}. Unable to pay deadline.")
                break
            
            # Player has enough money - force payment
            print(f"\n⚠️  DEADLINE REACHED! You must pay ${deadline_amount:,} to proceed.")
            
            while True:
                choice = input("Enter 'deadline_pay' or '1' to pay: ").strip().lower()
                
                if choice == "deadline_pay" or choice == "1":
                    money -= deadline_amount
                    print(f"💰 Deadline paid! You now have ${money}.")
                    sleep(0.75)
                    deadlines.pay_deadline()
                    active_bonuses = {}
                    for d in owned_charms:
                        if d['charm'].kind == "weight_active":
                            d['activations_this_round'] = 0
                            d['last_increase'] = 0
                    reset_manifestation_targets(owned_charms)
                    print(f"\nNew deadline: {deadlines.get_status_string()}")
                    
                    # Show phone ability selection for deadline 2 and onwards
                    if deadlines.can_choose_phone_ability():
                        show_phone_abilities()
                    
                    break
                else:
                    print("Invalid input. Type 'deadline_pay' or '1' to pay the deadline.")
        
        print()

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