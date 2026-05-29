from ast import pattern
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
# EFFECT SYSTEM
# ============================================================

class Effect:

    def __init__(
        self,
        effect_type,
        target=None,
        amount=0,
        chance=None
    ):

        self.type = effect_type
        self.target = target
        self.amount = amount
        self.chance = chance


# ============================================================
# EFFECT CONSTANTS
# ============================================================

LUCK = "LUCK"
EXTRA_SPIN = "EXTRA_SPIN"
WEIGHT_ACTIVE = "WEIGHT_ACTIVE"

ADD_SYMBOL_MULT = "ADD_SYMBOL_MULT"
ADD_PATTERN_MULT = "ADD_PATTERN_MULT"

ADD_REPETITION = "ADD_REPETITION"
ADD_CHAIN = "ADD_CHAIN"
ADD_RECHARGE_TARGET = "ADD_RECHARGE_TARGET"


# ============================================================
# CHARM
# ============================================================

class Charm:

    def __init__(
        self,
        name,
        description,
        effects=None,
        rarity="common",
        cooldown_rounds=0,
        weight=None
    ):

        self.name = name
        self.description = description

        self.effects = effects or []

        self.rarity = rarity
        self.cooldown_rounds = cooldown_rounds
        self.weight = weight

    def __repr__(self):

        return (
            f"{self.name} "
            f"({self.rarity}) - "
            f"{self.description}"
        )


# ============================================================
# RESOLVER
# ============================================================

import random


# ============================================================
# RESOLVER
# ============================================================

class CharmResolver:
    """
    Converts charms into executable effects.
    """

    def resolve(self, charm, context=None):

        resolved = []

        for effect in charm.effects:

            # chance roll
            if effect.chance is not None:

                if random.randint(1, 100) > effect.chance:
                    continue

            resolved.append(effect)

        return resolved


# ============================================================
# EXECUTOR
# ============================================================

class EffectExecutor:

    def execute(self, effect, charm_data, game_state):

        effect_type = effect.type

        # ====================================================
        # LUCK
        # ====================================================

        if effect_type == "LUCK":

            game_state['pending_luck'] += effect.amount

            print(f"  ✓ +{effect.amount} luck")


        # ====================================================
        # EXTRA SPIN
        # ====================================================

        elif effect_type == "EXTRA_SPIN":

            game_state['spins_left'] += effect.amount

            print(f"  ✓ +{effect.amount} spins")


        # ====================================================
        # WEIGHT ACTIVE
        # ====================================================

        elif effect_type == "WEIGHT_ACTIVE":

            target_cls = effect.target
            bonuses = game_state['active_bonuses']

            increase = calculate_weight_increase(target_cls)

            if charm_data['activations_this_round'] == 0:

                bonuses[target_cls] = (
                    bonuses.get(
                        target_cls,
                        getattr(target_cls, "weight", 1)
                    ) + increase
                )

                charm_data['last_increase'] = increase

            else:

                increase = charm_data['last_increase'] * 0.9

                bonuses[target_cls] += increase

                charm_data['last_increase'] = increase

            print(
                f"  ✓ {target_cls.__name__} weight +{increase:.1f}"
            )


        # ====================================================
        # SYMBOL MULT
        # ====================================================

        elif effect_type == "ADD_SYMBOL_MULT":

            game_state['symbols_mult'] += effect.amount

            print(f"  ✓ symbols mult +{effect.amount}")


        # ====================================================
        # PATTERN MULT
        # ====================================================

        elif effect_type == "ADD_PATTERN_MULT":

            game_state['patterns_mult'] += effect.amount

            print(f"  ✓ patterns mult +{effect.amount}")


        # ====================================================
        # REPETITION
        # ====================================================

        elif effect_type == "ADD_REPETITION":

            game_state['repetition_targets'].append(effect.target)

            print("  ✓ repetition modifier added")


        # ====================================================
        # CHAIN
        # ====================================================

        elif effect_type == "ADD_CHAIN":

            game_state['chain_targets'].append(effect.target)

            print("  ✓ chain modifier added")


        # ====================================================
        # RECHARGE
        # ====================================================

        elif effect_type == "ADD_RECHARGE_TARGET":

            game_state['recharge_targets'].append(effect.target)

            print("  ✓ recharge modifier added")


        # ====================================================
        # UNKNOWN
        # ====================================================

        else:

            print(f"  ⚠ Unknown effect: {effect_type}")


# ============================================================
# GLOBAL SYSTEMS
# ============================================================

resolver = CharmResolver()
executor = EffectExecutor()


# ============================================================
# CHARM ACTIVATION (EXECUTION LAYER)
# ============================================================

def activate_charms(owned_charms, game_state):

    available = [
        d for d in owned_charms
        if d['cooldown'] == 0
        and d['charm'].cooldown_rounds > 0
    ]

    if not available:

        print("No cooldown charms available.")
        return

    print("\n🎯 Activating ALL available charms...\n")

    for d in available:

        charm = d['charm']

        print(f"✓ {charm.name} activated!")

        effects = resolver.resolve(charm)

        for effect in effects:

            executor.execute(effect, d, game_state)

        d['uses'] += 1
        d['activations_this_round'] += 1
        d['cooldown'] = charm.cooldown_rounds


# ============================================================
# HELPERS
# ============================================================

def has_available_cooldown_charms(owned_charms):

    return any(
        d['cooldown'] == 0
        and d['charm'].cooldown_rounds > 0
        for d in owned_charms
    )


# ============================================================
# CHARM DEFINITIONS - COMMON TIER (50% spawn rate base) (30% with upgrade)
# ============================================================

# Luck charms
Tomato = Charm(
    "Tomato",
    "+3 luck for next spin (17.5% trigger chance)",
    effects = [
        Effect(LUCK,
                amount = 3
                chance = 17.5
        )
    ]
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
"13% chance for Wheel and Card to have the chain modifier (chain modifier increases the pattern scored's value by its base value)",
kind="chain_modifier",
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
"Gives symbols +base value every time a code charm is used",
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
    return int(1200 * (4 ** (deadline_num - 1)))

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
crafted_recipes = set()

charm_space_max = 6

deadlines = DeadlineSystem()

board = Board(3, 5)

resolver = CharmResolver()

# ============================================================
# CENTRAL GAME STATE
# ============================================================

game_state = {

    # Persistent modifiers
    'active_bonuses': {},

    # Multipliers
    'symbols_mult': 1,
    'patterns_mult': 1,

    # Runtime combat-style effects
    'repetition_targets': [],
    'chain_targets': [],
    'recharge_targets': [],

    # Misc
    'pending_luck': 0,
    'spins_left': 0
}

# ============================================================
# INITIAL DEADLINE DISPLAY
# ============================================================

print(deadlines.get_status_string())
print()

# ============================================================
# MAIN GAME LOOP
# ============================================================

while money > 0:

    # --------------------------------------------------------
    # EFFECTIVE MAX SPINS
    # --------------------------------------------------------

    max_spins = compute_effective_max_spins(
        BASE_MAX_SPINS,
        owned_charms
    )

    # --------------------------------------------------------
    # PLAYER CHOICE
    # --------------------------------------------------------

    choice = get_spin_amount(
        money,
        max_spins,
        owned_charms
    )

    # ========================================================
    # QUIT
    # ========================================================

    if choice == "q":
        print("Thanks for playing!")
        break

    # ========================================================
    # STORE
    # ========================================================

    if choice == "store":

        result = store_phase(
            money,
            owned_charms,
            crafted_recipes
        )

        if result:
            money, owned_charms = result

        continue

    # ========================================================
    # CRAFT
    # ========================================================

    if choice == "craft":

        crafted_recipes = craft_phase(
            owned_charms,
            crafted_recipes
        )

        continue

    # ========================================================
    # MANUAL CHARM ACTIVATION
    # ========================================================

    if choice == "charm":

        activate_charms(
            owned_charms,
            game_state,
            resolver
        )

        continue

    # ========================================================
    # DEADLINE PAYMENT
    # ========================================================

    if choice == "deadline_pay":

        deadline_amount = deadlines.get_current_total()

        if money >= deadline_amount:

            money -= deadline_amount

            print(
                f"Deadline paid! "
                f"You now have ${money}."
            )

            sleep(0.75)

            deadlines.pay_deadline()

            # Reset persistent bonus state
            game_state['active_bonuses'] = {}

            # Reset charm runtime tracking
            for d in owned_charms:

                d['activations_this_round'] = 0
                d['last_increase'] = 0

            reset_manifestation_targets(
                owned_charms
            )

            print(
                deadlines.get_status_string()
            )

        else:

            print(
                f"Insufficient funds. "
                f"Need ${deadline_amount:,}, "
                f"have ${money}."
            )

        continue

    # ========================================================
    # BUTTON
    # ========================================================

    if choice == "button":

        trigger_button()
        continue

    # ========================================================
    # START ROUND
    # ========================================================

    spins = choice
    spins_left = choice

    game_state['spins_left'] = spins_left

    board.start_round()

    money -= spins

    # --------------------------------------------------------
    # COOLDOWNS
    # --------------------------------------------------------

    for d in owned_charms:

        if d['cooldown'] > 0:
            d['cooldown'] -= 1

        d['activations_this_round'] = 0

    # --------------------------------------------------------
    # SPIN LUCK
    # --------------------------------------------------------

    spin_luck = compute_spin_luck(
        owned_charms,
        board
    )

    # --------------------------------------------------------
    # WEIGHT OVERRIDES
    # --------------------------------------------------------

    weight_overrides = compute_weight_overrides(
        BASE_SYMBOL_CLASSES,
        game_state['active_bonuses'],
        owned_charms
    )

    board.grand_total = 0

    patterns_scored_this_round = 0

    # ========================================================
    # SPINS
    # ========================================================

    for i in range(spins):

        # ----------------------------------------------------
        # RESET TEMPORARY EFFECTS EACH SPIN
        # ----------------------------------------------------

        game_state['symbols_mult'] = 1
        game_state['patterns_mult'] = 1

        game_state['repetition_targets'].clear()
        game_state['chain_targets'].clear()
        game_state['recharge_targets'].clear()

        # ----------------------------------------------------
        # RESOLVE PASSIVE CHARMS
        # ----------------------------------------------------

        for d in owned_charms:

            charm = d['charm']

            effects = resolver.resolve(
                charm,
                context=game_state
            )

            for effect in effects:

                if effect.effect_type == "ADD_SYMBOL_MULT":

                    game_state['symbols_mult'] *= (
                        effect.amount
                    )

                elif effect.effect_type == "ADD_PATTERN_MULT":

                    game_state['patterns_mult'] *= (
                        effect.amount
                    )

                elif effect.effect_type == "ADD_REPETITION":

                    game_state[
                        'repetition_targets'
                    ].append(
                        effect.target
                    )

                elif effect.effect_type == "ADD_CHAIN":

                    game_state[
                        'chain_targets'
                    ].append(
                        effect.target
                    )

                elif effect.effect_type == "ADD_RECHARGE_TARGET":

                    game_state[
                        'recharge_targets'
                    ].append(
                        effect.target
                    )

        # ----------------------------------------------------
        # CURRENT SPIN
        # ----------------------------------------------------

        board.current_spin(
            BASE_SYMBOL_CLASSES,
            weight_overrides,
            owned_charms,
            game_state['active_bonuses'],
            spin_luck,
            spin_number=i + 1,

            # NEW EFFECT STATE
            game_state=game_state
        )

        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

        board.display_total(
            owned_charms,
            spin_number=i + 1
        )

        patterns_scored_this_round += (
            board.patterns_scored_this_spin
        )

        # ====================================================
        # MID-ROUND CHARM ACTIVATION
        # ====================================================

        if (
            spins_left != 0
            and has_available_cooldown_charms(
                owned_charms
            )
        ):

            print(
                "\n📜 Activate charms?"
            )

            print(
                "(type 'charm' or press Enter)"
            )

            charm_input = (
                input("> ")
                .strip()
                .lower()
            )

            if charm_input == "charm":

                game_state['spins_left'] = (
                    spins_left
                )

                activate_charms(
                    owned_charms,
                    game_state,
                    resolver
                )

                spins_left = (
                    game_state['spins_left']
                )

                # Recompute weights
                weight_overrides = (
                    compute_weight_overrides(
                        BASE_SYMBOL_CLASSES,
                        game_state[
                            'active_bonuses'
                        ],
                        owned_charms
                    )
                )

        # ----------------------------------------------------
        # NEXT SPIN
        # ----------------------------------------------------

        if i + 1 < spins:

            input(
                "Press Enter to spin again..."
            )

            spins_left -= 1

            game_state['spins_left'] = (
                spins_left
            )

    # ========================================================
    # END ROUND
    # ========================================================

    deadlines.decrement_round()

    # --------------------------------------------------------
    # FINAL TOTAL
    # --------------------------------------------------------

    print("\n==============================")
    print("      FINAL GRAND TOTAL")
    print("==============================")

    print(board.grand_total)
    print()

    money += board.grand_total

    print(
        f"You now have ${money}.\n"
    )

    # ========================================================
    # WIN CONDITION
    # ========================================================

    if money >= 1000000:

        print(
            "WIN: You have reached "
            "$1,000,000!"
        )

        add_achievement(
            "Reach 1 Million"
        )

    # ========================================================
    # DEADLINE STATUS
    # ========================================================

    print(
        deadlines.get_status_string()
    )

    # ========================================================
    # MANDATORY DEADLINE PAYMENT
    # ========================================================

    if deadlines.must_pay():

        deadline_amount = (
            deadlines.get_current_total()
        )

        # ----------------------------------------------------
        # GAME OVER
        # ----------------------------------------------------

        if money < deadline_amount:

            print(
                f"\n💀 GAME OVER!"
            )

            print(
                f"You don't have enough "
                f"money to pay "
                f"${deadline_amount:,}."
            )

            print(
                f"You only have ${money}."
            )

            break

        # ----------------------------------------------------
        # FORCE PAYMENT
        # ----------------------------------------------------

        print(
            f"\n⚠️ DEADLINE REACHED!"
        )

        print(
            f"You must pay "
            f"${deadline_amount:,} "
            f"to proceed."
        )

        while True:

            choice = (
                input(
                    "Enter "
                    "'deadline_pay' "
                    "or '1' to pay: "
                )
                .strip()
                .lower()
            )

            if (
                choice == "deadline_pay"
                or choice == "1"
            ):

                money -= deadline_amount

                print(
                    f"💰 Deadline paid!"
                )

                print(
                    f"You now have ${money}."
                )

                sleep(0.75)

                deadlines.pay_deadline()

                # Reset persistent bonuses
                game_state[
                    'active_bonuses'
                ] = {}

                # Reset charm runtime tracking
                for d in owned_charms:

                    d[
                        'activations_this_round'
                    ] = 0

                    d[
                        'last_increase'
                    ] = 0

                reset_manifestation_targets(
                    owned_charms
                )

                print(
                    "\nNew deadline: "
                    + deadlines.get_status_string()
                )

                # Phone abilities
                if deadlines.can_choose_phone_ability():

                    show_phone_abilities()

                break

            else:

                print(
                    "Invalid input."
                )

    print()

# ============================================================
# GAME END
# ============================================================

print("\n" + "=" * 40)

if money <= 0:

    print(
        "You lost all your money."
    )

    print("Game over.")

else:

    print("Thanks for playing!")

print("=" * 40)