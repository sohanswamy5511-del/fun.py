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
    {"num": 4, "name": "+1 manifestation for a symbol", "rarity": "uncommon", "desc": "Average +1 extra of one symbol type, permanently"},
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
        self.round_symbol_bonuses = {}   # {SymbolClass: int}

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

        if to_apply:
            print("Applying delayed bonuses for this spin...")

        for bonus in to_apply:
            stype = bonus["symbol_type"]
            inc = bonus["increase"]

            self.global_symbol_bonuses[stype] = (
                self.global_symbol_bonuses.get(stype, 0) + inc
            )

            print(f"Delayed bonus applied! All {stype.__name__}s gain +{inc} permanently.")
            sleep(.3)

        # Remove applied bonuses
        self.delayed_bonuses = [b for b in self.delayed_bonuses if b["delay"] > 0]

    # --------------------------------------------------------
    # START ROUND
    # --------------------------------------------------------

    def start_round(self):
        """Reset round-scoped fusion modifier effects."""
        self.round_symbol_bonuses = {}
        for pattern in PATTERNS:
            pattern.current_multiplier_value = pattern.base_multiplier_value

    def get_modifier_rarity_rank(self, modifiers):
        """Return a rarity rank for a set of modifiers."""
        rank_map = {
            "gold": 5,
            "recharge": 4,
            "repetition": 3,
            "pattern_mult": 2,
            "symbol_mult": 1,
            "mimic": 0
        }
        return max((rank_map.get(mod, 0) for mod in modifiers), default=0)

    def apply_mimic_modifier(self, symbol, x, y):
        """Copy the nearest modifier from an existing symbol on the board."""
        best_source = None
        best_distance = None
        best_rank = -1

        for i in range(self.rows):
            for j in range(self.cols):
                candidate = self.grid[i][j]
                if candidate is None or candidate is symbol:
                    continue
                candidate_mods = [m for m in candidate.modifiers if m != "mimic"]
                if not candidate_mods:
                    continue

                distance = abs(x - i) + abs(y - j)
                rank = self.get_modifier_rarity_rank(candidate_mods)

                if best_source is None or distance < best_distance or (distance == best_distance and rank > best_rank):
                    best_source = candidate
                    best_distance = distance
                    best_rank = rank

        if best_source:
            copied_mods = [m for m in best_source.modifiers if m != "mimic"]
            symbol.modifiers.extend(copied_mods)
            if copied_mods:
                symbol.display_name += " [MIMIC:" + ",".join(copied_mods) + "]"

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

        # Check charms: detect any charm whose kind mentions 'gold' for GOLD modifiers
        has_golden_coins = any('gold' in str(d['charm'].kind) and d['charm'].target is Coin for d in owned_charms)
        has_golden_dice = any('gold' in str(d['charm'].kind) and d['charm'].target is Dice for d in owned_charms)
        has_golden_spinners = any('gold' in str(d['charm'].kind) and d['charm'].target is Spinner for d in owned_charms)
        has_golden_cards = any('gold' in str(d['charm'].kind) and d['charm'].target is Card for d in owned_charms)
        has_golden_wheels = any('gold' in str(d['charm'].kind) and d['charm'].target is Wheel for d in owned_charms)
        battery_chance = sum(d['charm'].amount for d in owned_charms if d['charm'].kind == "battery_modifier")
        repetition_chance = sum(d['charm'].amount for d in owned_charms if d['charm'].kind == "repetition_modifier")
        symbol_modifier_chance = sum(d['charm'].amount for d in owned_charms if d['charm'].kind == "symbol_modifier_chance")
        chain_modifier_chance = sum(d['charm'].amount for d in owned_charms if d['charm'].kind == "chain_modifier_chance")
        pattern_modifier_chance = sum(d['charm'].amount for d in owned_charms if d['charm'].kind == "pattern_modifier_chance")
        mimic_modifier_chance = sum(d['charm'].amount for d in owned_charms if d['charm'].kind == "mimic_modifier_chance")
        fusion_amplifier_bonus = sum(d['charm'].amount for d in owned_charms if d['charm'].kind == "fusion_amplifier")
        modifier_chance_bonus = get_modifier_chance_bonus(owned_charms)

        symbol_modifier_chance += modifier_chance_bonus + fusion_amplifier_bonus
        pattern_modifier_chance += modifier_chance_bonus + fusion_amplifier_bonus
        mimic_modifier_chance += max(0, modifier_chance_bonus // 2) + fusion_amplifier_bonus // 2

        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y] is None:

                    # Choose symbol class
                    symbol_class = random.choices(symbol_classes, weights=weights_list, k=1)[0]
                    symbol = symbol_class()

                    # Apply permanent and round-scoped global bonuses
                    bonus = self.global_symbol_bonuses.get(symbol_class, 0) + self.round_symbol_bonuses.get(symbol_class, 0)
                    if bonus:
                        symbol.current_value += bonus

                    # Activate (roll/spin/draw)
                    symbol.activate()

                    # Fusion modifiers can attach to symbols
                    if symbol_modifier_chance and random.randint(1, 100) <= symbol_modifier_chance:
                        symbol.modifiers.append("symbol_mult")
                        symbol.current_value += symbol.base_value
                        symbol.display_name += " [SYMBOL]"

                    if pattern_modifier_chance and random.randint(1, 100) <= pattern_modifier_chance:
                        symbol.modifiers.append("pattern_mult")
                        # Pattern multiplier modifiers will be applied during pattern scoring
                        symbol.display_name += " [PATTERN]"   

                    if mimic_modifier_chance and random.randint(1, 100) <= mimic_modifier_chance:
                        symbol.modifiers.append("mimic")
                        self.apply_mimic_modifier(symbol, x, y)

                    # Random battery/repeat modifiers from owned charms
                    if battery_chance and random.randint(1, 100) <= battery_chance:
                        if any(d['charm'].amount for d in owned_charms if d['charm'].kind == "battery_modifier"):
                            symbol.modifiers.append("recharge")
                        symbol.display_name += " [RECHARGE]"
                    
                    
                    if chain_modifier_chance and random.randint(1, 100) <= chain_modifier_chance:
                        symbol.modifiers.append("chain")
                        symbol.display_name += " [CHAIN]"

                    if repetition_chance and random.randint(1, 100) <= repetition_chance:
                        if any(d['charm'].amount for d in owned_charms if d['charm'].kind == "repetition_modifier"):
                            if isinstance(symbol, Coin, Spinner) and has_AGAINGAGAINAGAIN:
                                pattern.is_repeated = True
                                symbol.display_name += " [REPEAT]"
                        else:
                            pattern.is_repeated = True
                            symbol.display_name += " [REPEAT]"
                    else:
                        pattern.is_repeated = False
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

    def current_spin(self, symbol_classes, weights, owned_charms, active_bonuses, spin_luck, spin_number=None):
        """
        Perform a new spin:
          - Apply pending bonuses
          - Reset grid
          - Fill grid
        """
        self.apply_pending_bonuses()

        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.fill_cells(symbol_classes, weights, owned_charms, active_bonuses)
        self.apply_luck_manifestation(spin_luck)
        self.print_board(spin_number=spin_number)
        sleep(0.1)

    def apply_luck_manifestation(self, luck_amount):
        """Ensure the board contains at least luck_amount of one symbol type."""
        if luck_amount <= 1:
            return

        desired = min(luck_amount, self.rows * self.cols)
        counts = {}
        for x in range(self.rows):
            for y in range(self.cols):
                symbol = self.grid[x][y]
                symbol_type = type(symbol)
                counts[symbol_type] = counts.get(symbol_type, 0) + 1

        if not counts:
            return

        target_type = max(counts.keys(), key=lambda t: (counts[t], t().base_value))
        current_count = counts[target_type]

        if current_count >= desired:
            return

        needed = desired - current_count
        candidates = [
            (x, y) for x in range(self.rows) for y in range(self.cols)
            if type(self.grid[x][y]) != target_type
        ]
        random.shuffle(candidates)

        for x, y in candidates[:needed]:
            symbol = target_type()
            bonus = self.global_symbol_bonuses.get(target_type, 0) + self.round_symbol_bonuses.get(target_type, 0)
            if bonus:
                symbol.current_value += bonus
            symbol.activate()
            self.grid[x][y] = symbol

        print(f"Luck forced {desired}x {target_type.__name__} on board (luck={luck_amount}).")

    # --------------------------------------------------------
    # PRINT BOARD
    # --------------------------------------------------------

    def print_board(self, pattern_cells=None, pattern_score=None, spin_number=None):
        print(ANSI_CLEAR_SCREEN, end="")
        sleep(0.05)

        if spin_number is not None:
            print()
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
        sleep(.3)
        if pattern_cells:
            sleep(.3)
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
        # Multiple charm types can trigger pattern retriggering
        # Each charm has its own activation conditions
        # ----------------------------------------------------
        retrigger_count = 0
        retrigger_sources = []
        
        # I'm Bad at Math: 35% chance to trigger
        for d in owned_charms:
            if d['charm'].kind == "retrigger" and d['charm'].name != "Pattern Pulse" and d['charm'].name != "Lucky Coin Math" and random.randint(1, 100) <= 35:
                retrigger_count += 1
                retrigger_sources.append("I'm Bad at Math")
        
        # NOCHANGE: Patterns with non-Coin symbols trigger once more (cooldown 4)
        for d in owned_charms:
            if d['charm'].name == "NOCHANGE" and d['cooldown'] == 0:
                # Check if any pattern has non-Coin symbols
                for pattern, cells in chosen:
                    has_non_coin = any(not isinstance(self.grid[x][y], Coin) for x, y in cells)
                    if has_non_coin:
                        retrigger_count += 1
                        retrigger_sources.append("NOCHANGE")
                        d['cooldown'] = d['charm'].cooldown_rounds
                        break
        
        # Coin Rush: Patterns with only Coins trigger two more times (cooldown 5)
        for d in owned_charms:
            if d['charm'].name == "Coin Rush" and d['cooldown'] == 0:
                # Check if any pattern has only Coin symbols
                for pattern, cells in chosen:
                    all_coins = all(isinstance(self.grid[x][y], Coin) for x, y in cells)
                    if all_coins:
                        retrigger_count += 2
                        retrigger_sources.append("Coin Rush")
                        d['cooldown'] = d['charm'].cooldown_rounds
                        break
        
        # Pattern Pulse: 70% chance to trigger once more if 10+ patterns this spin
        if len(chosen) >= 10:
            for d in owned_charms:
                if d['charm'].name == "Pattern Pulse" and random.randint(1, 100) <= 70:
                    retrigger_count += 1
                    retrigger_sources.append("Pattern Pulse")
                    break
        
        # Lucky Coin Math: 30% chance to trigger once more if pattern contains a Coin
        for d in owned_charms:
            if d['charm'].name == "Lucky Coin Math":
                for pattern, cells in chosen:
                    has_coin = any(isinstance(self.grid[x][y], Coin) for x, y in cells)
                    if has_coin and random.randint(1, 100) <= 30:
                        retrigger_count += 1
                        retrigger_sources.append("Lucky Coin Math")
                        break
        
        triggers = 1 + retrigger_count

        if retrigger_count > 0:
            sources_str = ", ".join(dict.fromkeys(retrigger_sources))  # Remove duplicates while preserving order
            print(f"✨ {sources_str} activated! Retriggering patterns {retrigger_count} more time(s)...")
            sleep(0.75)

        # ----------------------------------------------------
        # SCORE EACH PATTERN
        # ----------------------------------------------------
        patterns_this_spin = len(chosen)

        has_gold_rush = has_charm(owned_charms, "Gold Rush")

        processed_patterns = []

        for pattern, cells in chosen:
            pattern_sum = sum(self.grid[x][y].current_value for x, y in cells)

            # Fusion modifiers: symbol modifiers and pattern modifiers carry through the round.
            scored_symbols = [self.grid[x][y] for x, y in cells]
            scored_symbol_types = set(type(s) for s in scored_symbols)

            for sym in scored_symbols:
                if "symbol_mult" in sym.modifiers:
                    self.round_symbol_bonuses[type(sym)] = self.round_symbol_bonuses.get(type(sym), 0) + 1
                    print(f"Symbol modifier triggered: all {type(sym).__name__}s gain +1 multiplier until end of round.")
                    sleep(0.2)

            if any("pattern_mult" in sym.modifiers for sym in scored_symbols):
                pattern.current_multiplier_value += 1
                print(f"Pattern modifier triggered: {pattern.name} multiplier +1 until end of round.")
                sleep(0.2)

            pattern_score = pattern.get_multiplier(pattern_sum) * triggers
            self.print_board(pattern_cells=[(pattern.name, cells)], pattern_score=pattern_score, spin_number=spin_number)
            total += pattern_score
            # ------------------------------------------------
            # GOLDEN MODIFIER: base behavior (without Gold Rush charm)
            # For every GOLD symbol in the scored pattern, queue a delayed
            # permanent bonus of +base_value for that symbol type. Multiple
            # GOLD symbols stack; retriggers multiply the total queued amount.
            # The queued bonuses are applied at the start of the next spin.
            # ------------------------------------------------
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
                        f"Golden modifier queued! A delayed +{total_increase} bonus for all {stype.__name__}s has been queued for the next spin."
                    )
                    sleep(0.5)

            # Append this scored pattern to processed list and handle Gold Rush
            processed_patterns.append((pattern, cells))

            # Gold Rush special: once at least 10 patterns have been scored in
            # this spin, each subsequent scored pattern causes the aggregated
            # GOLD base_values from the previous ten scored patterns to be
            # immediately applied permanently to their symbol types. This
            # happens for every pattern after the tenth (inclusive).
            if has_gold_rush and len(processed_patterns) >= 10:
                # Use the first ten scored patterns of this spin for aggregation
                first_ten = processed_patterns[:10]
                agg = {}
                for _, pcells in first_ten:
                    for x, y in pcells:
                        s = self.grid[x][y]
                        if s.is_golden:
                            stype = type(s)
                            agg[stype] = agg.get(stype, 0) + s.base_value

                if agg:
                    print("Gold Rush active: applying aggregated bonuses from the first 10 patterns immediately:")
                    for stype, inc in agg.items():
                        self.global_symbol_bonuses[stype] = self.global_symbol_bonuses.get(stype, 0) + inc
                        print(f"  +{inc} permanently applied to all {stype.__name__}s")

            sleep(0.25)

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
        sleep(.3)
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
      - symbol_modifier_chance: chance for symbols to spawn with +1 symbol mult until end round
      - pattern_modifier_chance: chance for symbols to spawn with +1 pattern mult until end round
      - mimic_modifier_chance: chance for symbols to spawn with a mimic modifier that copies the nearest modifier
      - fusion_amplifier: increases fusion modifier chances
      - retrigger: patterns trigger one extra time
      - cooldown: has cooldown-based activation
      - passive: always active
      - trait: applies modifier to other charms
    """

    def __init__(self, name, description, kind, target=None, amount=0, cooldown_rounds=0, rarity="common", chance=None, spins=1, max_amount=None):
        self.name = name
        self.description = description
        self.kind = kind  # can be a comma-separated string like 'luck,extra_spin'
        self.target = target
        self.amount = amount
        self.cooldown_rounds = cooldown_rounds
        self.rarity = rarity
        # Optional: activation chance (percentage) for chance-based charms
        self.chance = chance
        # Optional: number of spins this charm's luck effect should last when triggered
        self.spins = spins
        # Optional: maximum amount (used by some charms)
        self.max_amount = max_amount

    def __str__(self):
        return f"{self.name}: {self.description}"


# ============================================================
# CHARM DEFINITIONS - COMMON TIER (50% spawn rate base) (30% with upgrade)
# ============================================================

# Luck charms
Tomato = Charm(
    "Tomato",
    "+3 luck for next spin (17.5% trigger chance)",
    kind="luck",
    amount=3,
    chance=17.5,
    rarity="common"
)

Peach = Charm(
    "Peach",
    "+5 luck for next spin (10% trigger chance)",
    kind="luck",
    amount=5,
    chance=10,
    rarity="common"
)

# Golden Charms (existing)
GoldenWheels = Charm(
    "Golden Wheels",
    "25% chance for Wheels to spawn with GOLD modifier",
    kind="gold_modifier",
    target=Wheel,
    amount=25,
    rarity="common"
)

GoldenDice = Charm(
    "Golden Dice",
    "20% chance for Dice to spawn with GOLD modifier",
    kind="gold_modifier",
    target=Dice,
    amount=20,
    rarity="common"
)

GoldenCoins = Charm(
    "Golden Coins",
    "25% chance for Coins to spawn with GOLD modifier",
    kind="gold_modifier",
    target=Coin,
    amount=25,
    rarity="common"
)

GoldenSpinners = Charm(
    "Golden Spinners",
    "30% chance for Spinners to spawn with GOLD modifier",
    kind="gold_modifier",
    target=Spinner,
    amount=30,
    rarity="common"
)

GoldenCards = Charm(
    "Golden Cards",
    "25% chance for Cards to spawn with GOLD modifier",
    kind="gold_modifier",
    target=Card,
    amount=25,
    rarity="common"
)

Altered_Coin = Charm(
    "Altered Coin",
    "+1 spins_left, +3 luck (cooldown 1) 15% chance for destruction after the fifth use",
    kind="luck,extra_spin",
    amount=3,
    cooldown_rounds=1,
    rarity="common"
)

Spoons = Charm(
    "Spoons",
    "Whenever you see 3 spins with no patterns of 4+ symbols, the next spin will have one of the spoon patterns",
    kind="guaranteed_pattern",
    rarity="common"
)

X = Charm(
    "X",
    "Whenever you don’t see a pattern for 5 spins, the next spin will have an x pattern",
    kind="guaranteed_pattern",
    rarity="common"
)

N = Charm(
    "N",
    "Whenever you don’t see a pattern for 4 spins, the next spin will have an N pattern",
    kind="guaranteed_pattern",
    rarity="common"
)

LuckyPenny = Charm(
    "Lucky Penny",
    "+5 luck for next spin (12% trigger chance)",
    kind="luck",
    amount=5,
    chance=12,
    rarity="common"
)

FortuneCookie = Charm(
    "Fortune Cookie",
    "+3 luck for the next two spins (10% trigger chance)",
    kind="luck",
    amount=3,
    chance=10,
    spins=2,
    rarity="common"
)

JadeRabbit = Charm(
    "Jade Rabbit",
    "+1 spin_left, +4 luck (16% trigger chance)",
    kind="extra_spin,luck",
    amount=4,
    chance=16,
    rarity="common"
)

Cornerstone = Charm(
    "Cornerstone",
    "+7 luck for the first spin after buying a charm",
    kind="luck",
    amount=7,
    rarity="common"
)

NotGreedy = Charm(
    "Not Greedy",
    "5% chance for any symbol to spawn with GOLD modifier. Raises by 3% for every round skipped when paying a deadline early",
    kind="gold_modifier",
    amount=5,
    max_amount=25,
    rarity="common"
)

LuckyStar = Charm(
    "Lucky Star",
    "After scoring 1 pattern in 3 consecutive spins, next spin gains +5 luck",
    kind="luck",
    amount=5,
    rarity="common"
)

Wishbone = Charm(
    "Wishbone",
    "+2 luck next spin; if no patterns appear, gain +5 luck on the following spin",
    kind="luck",
    amount=2,
    rarity="common"
)

Sunflower = Charm(
    "Sunflower",
    "Guarantee a Horizontal Line XL pattern if no pattern appears for 2 spins",
    kind="guaranteed_pattern",
    rarity="common"
)

CatWink = Charm(
    "Cat Wink",
    "Guarantee a Vertical Line pattern after 1 scoreless spins",
    kind="guaranteed_pattern",
    rarity="common"
)

Smile = Charm(
    "Smile",
    "+3 luck for next spin (cooldown 1)",
    kind="luck",
    amount=3,
    cooldown_rounds=1,
    rarity="common"
)

FourLeaf = Charm(
    "Four Leaf",
    "+9 luck for next spin (5% trigger chance)",
    kind="luck",
    amount=9,
    chance=5,
    rarity="common"
)

OneMoreSpin = Charm(
    "One More Spin",
    "+1 max_spins next round (cooldown 3)",
    kind="extra_spin",
    cooldown_rounds=2,
    rarity="common"
)

PocketRabbit = Charm(
    "Pocket Rabbit",
    "+1 luck for every charm bought this deadline, applied next spin",
    kind="luck",
    amount=1,
    rarity="common"
)

BrokenMirror = Charm(
    "Broken Mirror",
    "If you fail to score, next spin gains +4 luck",
    kind="luck",
    amount=4,
    rarity="common"
)

# ============================================================
# CHARM DEFINITIONS - UNCOMMON TIER (30% spawn rate base) (33% with upgrade)
# ============================================================


# Extra spin charm
Spare_Change = Charm(
    "Spare Change",
    "+2 max spins",
    kind="max_spins+",
    rarity="uncommon"
)

# Weight-active charms (cooldown based)
Struck_Gold = Charm(
    "Struck Gold",
    "+2 avg coin manifestation for the rest of the deadline",
    kind="weight_active",
    target=Coin,
    cooldown_rounds=3,
    rarity="uncommon"
)

Trick_Deck = Charm(
    "Trick Deck",
    "+2 avg card manifestation for the rest of the deadline",
    kind="weight_active",
    target=Card,
    cooldown_rounds=3,
    rarity="uncommon"
)

ILoveTops = Charm(
    "I Love Tops",
    "+2 avg spinner manifestation for the rest of the deadline",
    kind="weight_active",
    target=Spinner,
    cooldown_rounds=3,
    rarity="uncommon"
)

Dice_Hard = Charm(
    "Dice Hard",
    "+2 avg dice manifestation for the rest of the deadline",
    kind="weight_active",
    target=Dice,
    cooldown_rounds=3,
    rarity="uncommon"
)

WheelOfFortune = Charm(
    "Wheel of Fortune",
    "+2 avg wheel manifestation for the rest of the deadline",
    kind="weight_active",
    target=Wheel,
    cooldown_rounds=3,
    rarity="uncommon"
)

SymbolBoost = Charm(
    "Symbol Boost",
    "Increase a chosen symbol's xmult by +1",
    kind="symbol_xmult",
    amount=1,
    rarity="uncommon"
)

SymbolSurge = Charm(
    "Symbol Surge",
    "Increase a chosen symbol's xmult by +2",
    kind="symbol_xmult",
    amount=2,
    rarity="uncommon"
)

CharmPocket = Charm(
    "Charm Pocket",
    "+1 charm space (doesn't take space)",
    kind="charm_space",
    amount=1,
    rarity="uncommon"
)

CharmHouse = Charm(
    "Charm House",
    "+2 charm space",
    kind="charm_space",
    amount=2,
    rarity="uncommon"
)

Blueprint = Charm(
    "Blueprint",
    "Gain the same effect as the last bought charm",
    kind="copy_purchased",
    rarity="uncommon"
)

LeftWing = Charm(
    "Left Wing",
    "Reuse the effect of the first charm you sold",
    kind="copy_sold",
    rarity="uncommon"
)

PhoneReuse = Charm(
    "Phone Reuse",
    "When a phone ability is selected, stop it from reappearing. When this charm is thrown away, allow it to be reseen and reuse the phone ability",
    kind="phone_reuse",
    rarity="uncommon"
)

CharmReappear = Charm(
    "Charm Reappear",
    "When a charm is thrown away, store it inside this charm. When this charm is thrown away, respawn the thrown away charm on the table",
    kind="charm_reappear",
    rarity="uncommon"
)

TakeSpace = Charm(
    "Take Space",
    "When a charm that doesn’t take space is bought, store it inside this charm. Throwing away this charm reuses the charm in question immediately",
    kind="take_space",
    rarity="uncommon"
)

I_cant_stop_winning = Charm(
    "I can't stop winning",
    "13% chance for Wheel and Card to have the blue modifier (blue modifier increases the pattern scored's value by its base value)",
    kind="blue_modifier",
    target=(Wheel, Card),
    amount=13,
    rarity="uncommon"
)

ReRetrigger = Charm(
    "Re-Retrigger",
    "5% chance for Dice to have the recharge modifier (recharge gives +1 charge on a random cooldown charm)",
    kind="recharge_modifier",
    target=Dice,
    amount=5,
    rarity="uncommon"
)

AGAINAGAINAGAIN = Charm(
    "AGAINAGAINAGAIN",
    "15% chance for Coin and Spinner to have the repetition modifier (gives +1 trigger of the pattern with the modifier scored) and does it multiple times every time there is one in a pattern",
    kind="repetition_modifier",
    target=(Coin, Spinner),
    amount=15,
    rarity="uncommon"
)

LuckyReroll = Charm(
    "Lucky Reroll",
    "+1 max spins and +3 luck for first spin of next round",
    kind="max_spins+",
    amount=1,
    rarity="uncommon"
)

SymbolBlast = Charm(
    "Symbol Blast",
    "Increase a chosen symbol's xmult by +3",
    kind="symbol_xmult",
    amount=3,
    rarity="uncommon"
)

# ============================================================
# CHARM DEFINITIONS - RARE TIER (20% spawn rate base) (22% with upgrade)
# ============================================================

ImBadAtMath = Charm(
    "I'm Bad At Math",
    "35% chance to trigger patterns one more time",
    kind="retrigger",
    rarity="rare"
)

Ramen = Charm(
    "Ramen",
    "Whenever you score 5 patterns, double the value of all symbols until the end of the round",
    kind="value_doubling",
    rarity="rare"
)

BeefBrisket = Charm(
    "Beef Brisket",
    "Whenever you score no patterns in a round, double all symbol mults, pattern mults, and 1.5 * earnings mult",
    kind="value_boost_on_drought",
    rarity="rare"
)

FreeEarnings = Charm(
    "Free Earnings",
    "Earnings mult +1 permanently (doesn't take space)",
    kind="earnings_mult",
    rarity="rare"
)

Bell = Charm(
    "Bell",
    "Symbols mult +1 permanently (cooldown 2)",
    kind="symbols_mult",
    cooldown_rounds=2,
    rarity="rare"
)

EverythingInExcess = Charm(
    "Everything in Excess",
    "Patterns mult +1 permanently for every time you earn 1.5x the required deadline's amount",
    kind="patterns_mult",
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

PatternPulse = Charm(
    "Pattern Pulse",
    "70% chance to trigger patterns one more time for the rest of the spin when there are 10 pattern triggers in a spin",
    kind="retrigger",
    rarity="rare"
)

BigScore = Charm(
    "Big Score",
    "Whenever you score at least 8 patterns, triple all symbol values for the rest of the round",
    kind="value_doubling",
    rarity="rare"
)

DrySpellBoost = Charm(
    "Dry Spell",
    "Whenever you score no patterns in a round, increase all symbol and pattern values by 90% permanently",
    kind="value_boost_on_drought",
    rarity="rare"
)

PatternSurge = Charm(
    "Pattern Surge",
    "Patterns mult +2 permanently after scoring 10 patterns in a round",
    kind="patterns_mult",
    rarity="rare"
)

LuckyCoinMath = Charm(
    "Lucky Coin Math",
    "30% chance to trigger patterns one more time when a pattern contains a Coin",
    kind="retrigger",
    rarity="rare"
)

SymbolFrenzy = Charm(
    "Symbol Frenzy",
    "Symbols mult +2 permanently after scoring 5 jackpots in a round",
    kind="symbols_mult",
    rarity="rare"
)

PatternWave = Charm(
    "Pattern Wave",
    "Patterns mult +2 permanently after scoring 7 patterns in one spin",
    kind="patterns_mult",
    rarity="rare"
)

EarningsRush = Charm(
    "Earnings Rush",
    "Earnings mult +3 permanently (doesn't take space)",
    kind="earnings_mult",
    rarity="rare"
)

SymbolRitual = Charm(
    "Symbol Ritual",
    "Symbols mult +3 permanently after scoring 5+ different patterns in one spin",
    kind="symbols_mult",
    rarity="rare"
)

PatternChain = Charm(
    "Pattern Chain",
    "Patterns mult +1 permanently every time you score 5 patterns after a scoreless spin",
    kind="patterns_mult",
    rarity="rare"
)

DoubleCoinValues = Charm(
    "Double Coin Values",
    "Double all Coin values for the rest of the round after scoring 5 Coin patterns",
    kind="value_doubling",
    rarity="rare"
)

DoubleDiceValues = Charm(
    "Double Dice Values",
    "Double all Dice values for the rest of the round after scoring 5 Dice patterns",
    kind="value_doubling",
    rarity="rare"
)

DoubleSpinnerValues = Charm(
    "Double Spinner Values",
    "Double all Spinner values for the rest of the round after scoring 5 Spinner patterns",
    kind="value_doubling",
    rarity="rare"
)

DoubleCardValues = Charm(
    "Double Card Values",
    "Double all Card values for the rest of the round after scoring 5 Card patterns",
    kind="value_doubling",
    rarity="rare"
)

DoubleWheelValues = Charm(
    "Double Wheel Values",
    "Double all Wheel values for the rest of the round after scoring 5 Wheel patterns",
    kind="value_doubling",
    rarity="rare"
)

DoubleAllPatterns = Charm(
    "Double All Patterns",
    "Double all pattern values for the rest of the round after scoring 7+ patterns in one spin",
    kind="value_doubling",
    rarity="rare"
)

EarningsWave = Charm(
    "Earnings Wave",
    "Double earnings mult for the rest of the round after scoring 18+ patterns in one spin",
    kind="earnings_mult",
    rarity="rare"
)

SymbolEcho = Charm(
    "Symbol Echo",
    "Symbols mult +1 permanently after scoring 3 different symbol patterns in one spin",
    kind="symbols_mult",
    rarity="rare"
)

PatternEcho = Charm(
    "Pattern Echo",
    "Patterns mult +1 permanently after scoring 5 different patterns in one spin",
    kind="patterns_mult",
    rarity="rare"
)

EarningsEcho = Charm(
    "Earnings Echo",
    "Earnings mult +1 permanently after scoring 4 consecutive spins with no patterns",
    kind="earnings_mult",
    rarity="rare"
)

SymbolRally = Charm(
    "Symbol Rally",
    "Symbols mult +1 permanently after scoring 6+ same_symbol patterns in one deadline",
    kind="symbols_mult",
    rarity="rare"
)

PatternRally = Charm(
    "Pattern Rally",
    "Patterns mult +1 permanently after scoring 8+ patterns across two spins",
    kind="patterns_mult",
    rarity="rare"
)

EarningsRally = Charm(
    "Earnings Rally",
    "Earnings mult +2 permanently after scoring the same pattern 5 spins in a row",
    kind="earnings_mult",
    rarity="rare"
)

ValueSpill = Charm(
    "Value Spill",
    "Increase all symbol values by their current value after 10+ pattern triggers in one deadline",
    kind="symbol_value",
    rarity="rare"
)

PatternReverb = Charm(
    "Pattern Reverb",
    "Increase all pattern values by their current value, permanently after scoring 10 patterns in a spin without a Jackpot",
    kind="pattern_value",
    rarity="rare"
)

SymbolCascade = Charm(
    "Symbol Cascade",
    "Symbols mult +1 permanently after scoring a pattern with 4+ symbols",
    kind="symbols_mult",
    rarity="rare"
)

PatternCascade = Charm(
    "Pattern Cascade",
    "Patterns mult +1 permanently after scoring a pattern with 5+ symbols",
    kind="patterns_mult",
    rarity="rare"
)

#===========================================================
# CHARM DEFINITIONS - EPIC TIER (5% spawn rate base) (10% with upgrade)
#===========================================================

Commit = Charm(
    "Commit",
    "Gain a new charm with rarity of last bought charm, destroy a random charm with rarity of last bought charm. Destroys after use",
    kind="code_commit",
    rarity="epic"
)

PatternAurora = Charm(
    "Pattern Aurora",
    "Double all pattern values for the rest of the deadline when you score 10+ patterns in a spin",
    kind="value_doubling",
    rarity="epic"
)

TripleAllSymbols = Charm(
    "Triple All Symbols",
    "Triple all symbol values for the rest of the deadline after scoring 18+ patterns in one spin",
    kind="value_doubling",
    rarity="epic"
)

TripleAllPatterns = Charm(
    "Triple All Patterns",
    "Triple all pattern values for the rest of the deadline after scoring 20+ patterns in one spin",
    kind="value_doubling",
    rarity="epic"
)

TripleEarningsMult = Charm(
    "Triple Earnings Mult",
    "Triple earnings mult permanently after ending a deadline at 500% of requirement",
    kind="earnings_mult",
    rarity="epic"
)

QuadAllSymbols = Charm(
    "Quad All Symbols",
    "Quadruple all symbol values for the rest of the round after scoring 30+ patterns in one spin",
    kind="value_doubling",
    rarity="epic"
)

QuadAllPatterns = Charm(
    "Quad All Patterns",
    "Quadruple all pattern values for the rest of the round after scoring 25 same_symbol patterns in one spin",
    kind="value_doubling",
    rarity="epic"
)

QuadEarningsMult = Charm(
    "Quad Earnings Mult",
    "Quadruple earnings mult permanently after scoring 100+ patterns in a deadline",
    kind="earnings_mult",
    rarity="epic"
)

SymbolTriumph = Charm(
    "Symbol Triumph",
    "Symbols mult +3 permanently after scoring 30+ jackpots in a single round",
    kind="symbols_mult",
    rarity="epic"
)

PatternTriumph = Charm(
    "Pattern Triumph",
    "Patterns mult +3 permanently after scoring 12+ jackpots in one spin",
    kind="patterns_mult",
    rarity="epic"
)

EarningsTriumph = Charm(
    "Earnings Triumph",
    "Earnings mult +4 permanently after scoring 20+ patterns in one spin",
    kind="earnings_mult",
    rarity="epic"
)

SymbolOverdrive = Charm(
    "Symbol Overdrive",
    "Symbols mult +5 permanently after scoring 7 different patterns in one spin",
    kind="symbols_mult",
    rarity="epic"
)

PatternOverdrive = Charm(
    "Pattern Overdrive",
    "Patterns mult +5 permanently after scoring 10 of the same pattern type in a row",
    kind="patterns_mult",
    rarity="epic"
)

EarningsOverdrive = Charm(
    "Earnings Overdrive",
    "Earnings mult +5 permanently (cooldown 7)",
    kind="earnings_mult",
    rarity="epic"
)

QuadThunder = Charm(
    "Quad Thunder",
    "Quadruple all symbols and pattern values when you score only one pattern in a spin and it has exactly 9 symbols",
    kind="value_doubling",
    rarity="epic",
)

Stage = Charm(
    "Stage",
    "All changes to a charm will be permanent. Destroys after use",
    kind="code_stage",
    rarity="epic"
)

Sync = Charm(
    "Sync",
    "All changes to game values will be permanent. Usable between spins. Destroys after use",
    kind="code_sync",
    rarity="epic"
)

New_Variable = Charm(
    "New Variable",
    "Add a new xmult option to a symbol of maximum of 25. Destroys after use",
    kind="code_new_variable",
    rarity="epic"
)

Make_True = Charm(
    "Make True",
    "A phone call will now have your ability of choice WITHIN UPGRADE LIMITS. Destroys after use",
    kind="code_make_true",
    rarity="epic"
)

More_Coding = Charm(
    "More Coding",
    "Gives a charm with '//' in its name every deadline if player has enough space",
    kind="code_more_coding",
    rarity="epic"
)

Python = Charm(
    "Python",
    "Gives symbols +base value every time an epic or legendary charm is used",
    kind="code_python",
    rarity="epic"
)

HTML = Charm(
    "HTML",
    "Gives patterns +base value every time an epic or legendary charm is used",
    kind="code_html",
    rarity="epic"
)

I_WANT_IT_NOW = Charm(
    "I WANT IT NOW",
    "Choose a charm to get (non exotic +). Destroys after use",
    kind="code_want_it_now",
    rarity="epic"
)

FusionReactor = Charm(
    "Fusion Reactor",
    """Boost all fusion modifier chances by 10%
    Mimics now go after the rarest modifier to copy following same logic.
    Symbol modifier now gives +2 for trigger, pattern mult modifier now requires only one pattern to do its effect.
    Creates a new modifier called earnings; scoring 3 patterns with it increases your earnings bonus by 2 for the rest of the round.""",
    kind="fusion_amplifier",
    amount=8,
    rarity="epic"
)

Resurrection = Charm(
    "Resurrection",
    "When you are about to die you gain two extra rounds. Then destroys itself",
    kind="revive",
    rarity="epic"
)

# ============================================================
# CHARM DEFINITIONS - LEGENDARY TIER (5% spawn rate with upgrade)
# ============================================================

CCHARM = Charm(
    "CCHARM",
    "All cooldown charms trigger one more time",
    kind="cooldown_charm_retrigger",
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
    kind="value_doubling",
    rarity="legendary"
)

GiantPeach = Charm(
    "Giant Peach",
    "Score 30+ patterns in a spin = double patterns and symbols (resets end of deadline)",
    kind="value_doubling",
    rarity="legendary"
)

LargestTomato = Charm(
    "The Largest Tomato Ever",
    "Score 50+ patterns = double value, then triple, then quad, etc. (resets end of deadline)",
    kind="value_exponential",
    rarity="legendary"
)

MoneyMakingMachine = Charm(
    "Money Making Machine",
    "Charms giving patterns multiplier + 1 and symbols multiplier + 1 now give patterns multiplier +10 and symbols multiplier x1.5",
    kind="mult_converter",
    rarity="legendary"
)

Flowers = Charm(
    "Flowers",
    "Increase value of all symbols by their base value every other pattern (resets end of deadline)",
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
    """Gold Rush: If a spin contains >=10 scored patterns, the aggregated GOLD modifiers
from the previous ten patterns are immediately added to their symbol types for every pattern
after 10. Additionally, GOLD modifiers still queue their normal delayed bonuses for the next spin. 
This makes GOLD modifiers far more powerful when many patterns are scored in a single spin.""",
    kind="gold_amplifier",
    rarity="legendary"
)

CooldownChoir = Charm(
    "Cooldown Choir",
    "All cooldown charms trigger one more time",
    kind="cooldown_charm_retrigger",
    rarity="legendary"
)

PhoneEncore = Charm(
    "Phone Encore",
    "All phone abilities trigger one more time",
    kind="phone_retrigger",
    rarity="legendary"
)

Blossom = Charm(
    "Blossom",
    "Increase value of all symbols and patterns by their base value every fourth pattern (resets end of deadline)",
    kind="alternating_boost",
    rarity="legendary"
)

JackpotShield = Charm(
    "Jackpot Shield",
    "Jackpots don't occur - one random cell changes symbol instead (requires 6 charges)",
    kind="jackpot_prevention",
    cooldown_rounds=6,
    rarity="legendary"
)

GoldStandard = Charm(
    "Gold Standard",
    "If a spin contains >=8 scored patterns, all GOLD modifiers double their effect for the round",
    kind="gold_amplifier",
    rarity="legendary"
)

SymbolFusion = Charm(
    "Symbol Fusion",
    "+20% chance for your most valuable symbol to have the symbol modifier. Scoring a pattern with this modifier increases your symbol multiplier by one until the end of the round",
    kind="symbol_modifier",
    rarity="legendary_craftable",
)

PatternFusion = Charm(
    "Pattern Fusion",
    "+15% chance for your most valuable symbol to have the pattern mult modifier. Scoring two patterns with this modifier increases your patterns multiplier by one until the end of the round",
    kind="pattern_mult_modifier",
    rarity="legendary_craftable",
)

Mimic = Charm(
    "Mimic",
    "+25% chance for all symbols to have the mimic modifier. Mimic becomes the modifier of the closest symbol with a modifier's modifier",
    kind="mimic_modifier",
    rarity="legendary_craftable",
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
    kind="conditional_nonJackpot",
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
    kind="three7s",
    rarity="exotic"
)

InfiniteStorage = Charm(
    "Infinite Storage",
    "+1 charm space for every 5+ jackpots in spin, +1 for each jackpot after 10th",
    kind="charm_space_scaling",
    rarity="exotic"
)

RELOADING = Charm(
    "RELOADING",
    "All symbols gain 1/9 of current value every shop restock. Restock costs /2",
    kind="shop_scaling",
    rarity="exotic"
)

Polynomial = Charm(
    "Polynomial",
    "All charms that scale now scale by a degree 2 polynomial.",
    kind="scale_scaling",
    rarity="exotic"
)

Fusion_Reactor = Charm(
    "Fusion Reactor",
    """Increases chances of all symbols to have mimic, symbol, or pattern_mult modifiers by 20%
    Symbol now gives +2 symbol mult, Pattern now only requires one pattern, Mimic copies rarest modifier instead of most common one
    Creates a new modifier called earnings that increases your earnings mult by 2 for every 3 patterns scored with the modifier""",
    kind="new_modifiers",
    rarity="exotic_craftable",
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
    "HelloSymbol": {
        "name": "HelloSymbol",
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
    "Symbol Fusion": {
        "name": "Symbol Fusion",
        "description": "Craft the Symbol Fusion charm, which grants symbol modifier spawning with end-of-round symbol bonus effects.",
        "requires": ["Golden Coins", "Golden Dice", "Golden Wheels"],
        "rarity": "craftable_rare"
    },
    "Pattern Fusion": {
        "name": "Pattern Fusion",
        "description": "Craft the Pattern Fusion charm, which grants pattern modifier spawning with end-of-round pattern bonus effects.",
        "requires": ["Golden Spinners", "Golden Cards", "Golden Dice"],
        "rarity": "craftable_rare"
    },
    "Mimic": {
        "name": "Mimic",
        "description": "Craft the Mimic Fusion charm, which grants mimic modifier spawning to copy nearby modifiers.",
        "requires": ["Golden Wheels", "Golden Cards", "Golden Coins"],
        "rarity": "craftable_rare"
    },
    "Fusion Reactor": {
        "name": "Fusion Reactor",
        "description": "Craft the Fusion Reactor charm, increasing fusion modifier chances and mimic power.",
        "requires": ["NOCHANGE", "CCHARM", "NotGreedy"],
        "rarity": "craftable_epic"
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
    Altered_Coin, Spoons, X, N,
    LuckyPenny, FortuneCookie, JadeRabbit, Cornerstone, LuckyStar, Wishbone,
    Sunflower, CatWink, Smile, FourLeaf,
    OneMoreSpin, PocketRabbit, BrokenMirror,
    
    # Uncommon
    Spare_Change,
    Struck_Gold, Trick_Deck, ILoveTops, Dice_Hard, WheelOfFortune,
    SymbolBoost, SymbolSurge,
    CharmPocket, CharmHouse, Blueprint, LeftWing,
    PhoneReuse, CharmReappear, TakeSpace,
    I_cant_stop_winning, ReRetrigger, AGAINAGAINAGAIN,
    LuckyReroll,
    
    # Rare
    ImBadAtMath,
    Ramen, BeefBrisket,
    FreeEarnings, Bell, EverythingInExcess,
    NO_CHANGE, CoinExtraTrigger, PatternPulse, BigScore,
    DrySpellBoost, PatternSurge,
    PatternAurora, SymbolFrenzy, PatternWave, EarningsRush,
    SymbolRitual, PatternCascade, SymbolCascade,
    DoubleCoinValues, DoubleDiceValues, DoubleSpinnerValues,
    DoubleCardValues, DoubleWheelValues,
    DoubleAllPatterns, EarningsWave,
    SymbolEcho, PatternEcho, EarningsEcho,
    SymbolRally, PatternRally, EarningsRally,
    ValueSpill, PatternReverb,

    # Epic
    Commit, Stage, Sync, New_Variable, Make_True, More_Coding, Python, HTML, I_WANT_IT_NOW, FusionReactor, Resurrection,
    TripleAllSymbols, TripleAllPatterns, TripleEarningsMult,
    QuadAllSymbols, QuadAllPatterns, QuadEarningsMult,
    SymbolTriumph, PatternTriumph, EarningsTriumph,
    SymbolOverdrive, PatternOverdrive, EarningsOverdrive,
    QuadThunder,

    # Legendary
    CCHARM, ProtestingCall,
    WorldRecordPepper, GiantPeach, LargestTomato,
    MoneyMakingMachine, Flowers,
    INeedToStopWinning, GoldRush,
    CooldownChoir, PhoneEncore, 
    JackpotShield, GoldStandard,
    SymbolFusion, PatternFusion, Mimic,
    
    # Exotic
    QuantProfessor, IsThisBroken, TenXMult,
    CoinTailsBoost, ExponentialMult, ExponentialGrowth,
    AlwaysOn, TheSeraphim, Blood, Soul, Body,
    SevenDeadlySins, InfiniteStorage, RELOADING, Polynomial,
    
    # Transcendency
    THEWORLDENDER, EssenceOfGods,
]

ALL_OBTAINABLE_CHARMS_LIST = [
    # Common
    Tomato, Peach,
    GoldenWheels, GoldenDice, GoldenCoins, GoldenSpinners, GoldenCards,
    Altered_Coin, Spoons, X, N,
    LuckyPenny, FortuneCookie, JadeRabbit, Cornerstone, LuckyStar, Wishbone,
    Sunflower, CatWink, Smile, FourLeaf,
    OneMoreSpin, PocketRabbit, BrokenMirror,
    
    # Uncommon
    Spare_Change,
    Struck_Gold, Trick_Deck, ILoveTops, Dice_Hard, WheelOfFortune,
    SymbolBoost, SymbolSurge,
    CharmPocket, CharmHouse, Blueprint, LeftWing,
    PhoneReuse, CharmReappear, TakeSpace,
    I_cant_stop_winning, ReRetrigger, AGAINAGAINAGAIN,
    LuckyReroll,
    
    # Rare
    ImBadAtMath,
    Ramen, BeefBrisket,
    FreeEarnings, Bell, EverythingInExcess,
    NO_CHANGE, CoinExtraTrigger, PatternPulse, BigScore,
    DrySpellBoost, PatternSurge,
    PatternAurora, SymbolFrenzy, PatternWave, EarningsRush,
    SymbolRitual, PatternCascade, SymbolCascade,
    DoubleCoinValues, DoubleDiceValues, DoubleSpinnerValues,
    DoubleCardValues, DoubleWheelValues,
    DoubleAllPatterns, EarningsWave,
    SymbolEcho, PatternEcho, EarningsEcho,
    SymbolRally, PatternRally, EarningsRally,
    ValueSpill, PatternReverb,
    
    # Epic
    Commit, Stage, Sync, New_Variable, Make_True, More_Coding, Python, HTML, I_WANT_IT_NOW,
    Resurrection,
]

ALL_OBTAINABLE_LOCKED = [
    CCHARM, ProtestingCall,
    WorldRecordPepper, GiantPeach, LargestTomato,
    MoneyMakingMachine, Flowers,
    INeedToStopWinning, GoldRush,
    CooldownChoir, PhoneEncore, JackpotShield, GoldStandard,
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
    # support charms that list multiple kinds in a comma-separated string
    extra = sum(1 for d in owned_charms if "extra_spin" in str(d['charm'].kind))
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


def compute_spin_luck(owned_charms, board):
    """Compute effective luck for the upcoming spin.

    Without luck charms, luck is a random value from 1 to 4. Luck charms
    increase this initial value by their amount. Passive luck bonuses from
    other effects are also applied.
    """
    effects = apply_charm_effects(owned_charms, board)
    initial_luck = random.randint(1, 4)
    bonus_luck = int(effects.get('luck_bonus', 0))

    for d in owned_charms:
        charm = d['charm']

        # handle persistent multi-spin luck from previous triggers
        if d.get('temp_luck_spins', 0) > 0 and "luck" in str(charm.kind):
            bonus_luck += charm.amount
            d['temp_luck_spins'] -= 1
            continue

        # charms can declare multiple kinds separated by commas
        if "luck" in str(charm.kind):
            # if charm has a chance, roll to see if it activates
            if getattr(charm, 'chance', None) is not None:
                if random.random() * 100 <= charm.chance:
                    bonus_luck += charm.amount
                    # if the charm lasts multiple spins, mark temp counter
                    if getattr(charm, 'spins', 1) > 1:
                        d['temp_luck_spins'] = charm.spins - 1
            else:
                bonus_luck += charm.amount

    total_luck = max(1, initial_luck + bonus_luck)
    return total_luck


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
# WEIGHT CHARM HELPERS
# ============================================================

def calculate_weight_increase(target_symbol_class):
    """
    Calculate the weight increase needed to add approximately +2 average symbols per spin.
    
    On a 3x5 (15-cell) board, we solve for X where:
    (base_weight + X) / (base_total_weight + X) * 15 = (base_weight / base_total_weight * 15) + 2
    
    This ensures that the target symbol type appears 2 more times per spin on average.
    """
    base_weight = getattr(target_symbol_class, "weight", 1)
    # With default symbols: Coin=30, Spinner=25, Dice=20, Card=15, Wheel=10, Seven=0 (total=100)
    base_total_weight = 100
    
    # Current average count of this symbol on a 15-cell board
    current_avg = (base_weight / base_total_weight) * 15
    target_avg = current_avg + 2
    
    # Solve: (base_weight + X) / (base_total_weight + X) * 15 = target_avg
    # base_weight * 15 + X * 15 = target_avg * (base_total_weight + X)
    # X * (15 - target_avg) = target_avg * base_total_weight - base_weight * 15
    
    numerator = target_avg * base_total_weight - base_weight * 15
    denominator = 15 - target_avg
    
    if denominator > 0:
        increase = numerator / denominator
        return max(1, int(round(increase)))
    return 2  # fallback


# ============================================================
# AUTO‑ACTIVATE‑ALL CHARM PHASE (UPDATED)
# ============================================================

def charm_phase(owned_charms, active_bonuses, symbol_classes=None, deadlines=None):
    """
    UPDATED BEHAVIOR:
    When the player types 'charm', ALL cooldown-based charms that are off cooldown
    automatically activate, in order, with no menu.
    
    This includes:
      - weight_active charms (Struck Gold, Trick Deck, etc.) - applies weight increase for +2 avg symbols
      - Any other charm with cooldown_rounds > 0 and currently available
    
    Weight increases PERSIST across spins within a deadline and accumulate with each trigger.
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

            # Calculate increase based on target symbol's base weight
            increase = calculate_weight_increase(target_cls)

            # First activation this round
            if d['activations_this_round'] == 0:
                active_bonuses[target_cls] = active_bonuses.get(target_cls, getattr(target_cls, "weight", 1)) + increase
                d['last_increase'] = increase
                current_avg = (active_bonuses[target_cls] / (100 + increase)) * 15
                print(f"  ✓ {charm.name}: {target_name} weight +{increase} (~+2 avg symbols)")

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
        board.start_round()
        money -= spins

        # Update cooldowns and reset round activation counters
        for d in owned_charms:
            if d['cooldown'] > 0:
                d['cooldown'] -= 1
            d['activations_this_round'] = 0

        # Compute spin luck and use it during board creation
        spin_luck = compute_spin_luck(owned_charms, board)
        # NOTE: DO NOT reset active_bonuses here - weight increases persist across spins within a deadline
        weight_overrides = compute_weight_overrides(BASE_SYMBOL_CLASSES, active_bonuses, owned_charms)
        board.grand_total = 0
        patterns_scored_this_round = 0  # Track total patterns for conditional charms

        # Perform spins
        for i in range(spins):
            board.current_spin(BASE_SYMBOL_CLASSES, weight_overrides, owned_charms, active_bonuses, spin_luck, spin_number=i+1)
            board.display_total(owned_charms, spin_number=i+1)
            patterns_scored_this_round += board.patterns_scored_this_spin

            if spins != 0 and has_available_cooldown_charms(owned_charms):
                print("\n📜 Activate charms? (type 'charm' to activate, or press Enter to skip)")
                charm_input = input("> ").strip().lower()
                if charm_input == "charm":
                    charm_phase(owned_charms, active_bonuses, BASE_SYMBOL_CLASSES)
                    # Recalculate weights after charm activation so changes take effect on next spin
                    weight_overrides = compute_weight_overrides(BASE_SYMBOL_CLASSES, active_bonuses, owned_charms)
            
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

            if i + 1 < spins:
                input("Press Enter to spin again...")

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