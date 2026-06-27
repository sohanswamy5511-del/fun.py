from os import name
import random

from charms import Charm, reset_count
from gamestate import last_bought_charm, game_state
from effects import Effect, EffectType, Trigger, Duration
from symbol import Coin, Spinner, Wheel, Dice, Card
from conditions import FirstSpinAfterCharmBought, PatternScored, SameSymbolCount, ScorelessRound, EarningsThreshold, UniquePatternCount, ScorelessSpinFollowup, UniqueSymbolCount, CharmBoughtThisDeadline, SamePatternScored
from pattern import Pattern, VerticalLine, HorizontalLine, DiagonalLine, HorizontalLineLarge, HorizontalLineXL, SpoonA, SpoonB, NPatternA, NPatternB, XPattern, Jackpot
# ============================================================
# CHARM DEFINITIONS - COMMON TIER (50% spawn rate base) (30% with upgrade)
# ============================================================


# Luck charms
Tomato = Charm(
    name="Tomato",
    description="+3 luck for next spin (17.5% trigger chance)",
    effects=[
        Effect(
            type=EffectType.LUCK,
            amount=3,
            chance=17.5,
            trigger=Trigger.ON_SPIN_START,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="common"
)

Peach = Charm(
    name="Peach",
    description="+5 luck for next spin (10% trigger chance)",
    effects=[
        Effect(
            type=EffectType.LUCK,
            amount=5,
            chance=10,
            trigger=Trigger.ON_SPIN_START,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="common"
)

GoldenWheels = Charm(
    name="Golden Wheels",
    description="25% chance for Wheels to spawn with GOLD modifier",
    effects=[
        Effect(
            type=EffectType.GOLD_MODIFIER,
            amount=25,
            chance=25,
            target=Wheel,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="common"
)

GoldenDice = Charm(
    name="Golden Dice",
    description="20% chance for Dice to spawn with GOLD modifier",
    effects=[
        Effect(
            type=EffectType.GOLD_MODIFIER,
            amount=20,
            chance=20,
            target=Dice,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="common"
)

GoldenCoins = Charm(
    name="Golden Coins",
    description="25% chance for Coins to spawn with GOLD modifier",
    effects=[
        Effect(
            type=EffectType.GOLD_MODIFIER,
            amount=25,
            chance=25,
            target=Coin,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="common"
)

GoldenSpinners = Charm(
    name="Golden Spinners",
    description="30% chance for Spinners to spawn with GOLD modifier",
    effects=[
        Effect(
            type=EffectType.GOLD_MODIFIER,
            amount=30,
            chance=30,
            target=Spinner,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="common"
)

GoldenCards = Charm(
    name="Golden Cards",
    description="25% chance for Cards to spawn with GOLD modifier",
    effects=[
        Effect(
            type=EffectType.GOLD_MODIFIER,
            amount=25,
            chance=25,
            target=Card,
            trigger=Trigger.PERMANENT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="common"
)

Altered_Coin = Charm(
    name="Altered Coin",
    description="+1 spins_left, +3 luck (cooldown 1). 15% chance of destruction after 5th use",
    effects=[
        Effect(
            type=EffectType.LUCK,
            amount=3,
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            duration=Duration.SPINS(1)
        ),
        Effect(
            type=EffectType.SPINS_LEFT,
            amount=1,
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            duration=Duration.ROUNDS(1)       
        )
    ],
    rarity="common",
    cooldown_rounds=1,
    charm_life=random.randint(1, 100) if Duration.USES() > 5 else None
)

Spoons = Charm(
    name="Spoons",
    description=(
        "Whenever you see 3 spins with no patterns of 5+ symbols, the next spin will have "
        "one of the spoon patterns"
    ),
    effects=[
        Effect(
            type=EffectType.GUARANTEE_PATTERN,
            target=random.choice([SpoonA, SpoonB]),
            trigger=Trigger.PRE_SCORE,
            condition=PatternScored(0, 3, None, None, 5),
            duration=Duration.SPINS(1)
        )
    ],
    rarity="common"
)

X = Charm(
    name="X",
    description=(
        "Whenever you don’t see a pattern for 5 spins, "
        "the next spin will have an X pattern"
    ),
    effects=[
        Effect(
            type=EffectType.GUARANTEE_PATTERN,
            target=XPattern,
            trigger=Trigger.PRE_SCORE,
            condition=PatternScored(0, 5, None, None, None),
            duration=Duration.SPINS(1)
        )
    ],
    rarity="common"
)

N = Charm(
    name="N",
    description=(
        "Whenever you don’t see a pattern for 4 spins, "
        "the next spin will have an N pattern"
    ),
    effects=[
        Effect(
            type=EffectType.GUARANTEE_PATTERN,
            target=random.choice([NPatternA, NPatternB]),
            trigger=Trigger.PRE_SCORE,
            condition=PatternScored(0, 4, None, None, None),
            duration=Duration.SPINS(1)
        )
    ],

    rarity="common"
)

LuckyPenny = Charm(
    name="Lucky Penny",
    description="+5 luck for next spin (12% trigger chance)",
    effects=[
        Effect(
            EffectType.LUCK,
            amount=5,
            chance=12,
            trigger=Trigger.ON_SPIN_START,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="common"
)

FortuneCookie = Charm(
    name="Fortune Cookie",
    description="+3 luck for the next two spins (10% trigger chance)",
    effects=[
        Effect(
            EffectType.LUCK,
            amount=3,
            chance=10,
            trigger=Trigger.ON_SPIN_START,
            duration=Duration.SPINS(2)
        )
    ],
    rarity="common"
)

JadeRabbit = Charm(
    name="Jade Rabbit",
    description="+1 spin_left, +4 luck (16% trigger chance)",
    effects=[
        Effect(
            EffectType.LUCK,
            amount=4,
            chance=16,
            trigger=Trigger.ON_SPIN_START,
            duration=Duration.SPINS(1)
        ),
        Effect(
            EffectType.SPINS_LEFT,
            amount=1,
            chance=100,
            trigger=Trigger.ON_SPIN_START,
            duration=Duration.ROUNDS(1)
        )
    ],
    rarity="common"
)

Cornerstone = Charm(
    name="Cornerstone",
    description="+7 luck for the first spin after buying a charm",
    effects=[
        Effect(
            EffectType.LUCK,
            amount=7,
            chance=100,
            condition=FirstSpinAfterCharmBought(),
            trigger=Trigger.ON_SPIN_START,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="common"
)

NotGreedy = Charm(
    name="Not Greedy",
    description="5% base chance for any symbol to spawn with GOLD modifier. Raises by 3% for every round skipped this deadline (up to 35%)",
    effects=[
        Effect(
            type=EffectType.DYNAMIC_GOLD_CHANCE,
            amount=5 + (lambda gs: gs.get('rounds_skipped_this_deadline', 0) * 3),
            calculate_fn=lambda gs: 5 + (gs.get('rounds_skipped_this_deadline', 0) * 3),
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="common"
)

LuckyStar = Charm(
    name="Lucky Star",
    description="After scoring 1 pattern in 3 consecutive spins, next spin gains +5 luck",
    effects=[
        Effect(
            EffectType.LUCK,
            amount=5,
            chance=100,
            condition=PatternScored(1, 3, None, None, None),
            trigger=Trigger.ON_SPIN_START,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="common"
)

Wishbone = Charm(
    name="Wishbone",
    description="+2 luck next spin after 2 failed spins; gain +5 luck on followup for every spin after without a pattern",
    effects=[
        Effect(
            EffectType.LUCK,
            amount=2,
            chance=100,
            condition=PatternScored(0, 2, None, None, None),
            trigger=Trigger.ON_SPIN_START,
            duration=Duration.SPINS(1)
        ),
        Effect(
            EffectType.LUCK,
            amount=2 + (5 * (lambda gs: gs.get('consecutive_scoreless_spins', 0) - 2)),
            chance=100,
            condition=PatternScored(0, 1, None, None, None),
            trigger=Trigger.ON_SPIN_START,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="common"
)

Sunflower = Charm(
    name="Sunflower",
    description="Guarantee a Horizontal Line XL pattern if no pattern appears for 2 spins",
    effects=[
        Effect(
            type=EffectType.GUARANTEE_PATTERN,
            target=HorizontalLineXL,
            chance=100,
            condition=PatternScored(0, 2, None, None, None),
            trigger=Trigger.PRE_SCORE,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="common"
)

CatWink = Charm(
    name="Cat Wink",
    description="Guarantee a Vertical Line pattern after 1 scoreless spin",
    effects=[
        Effect(
            type=EffectType.GUARANTEE_PATTERN,
            target=VerticalLine,
            chance=100,
            condition=PatternScored(0, 1, None, None, None),
            trigger=Trigger.PRE_SCORE,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="common"
)

Smile = Charm(
    name="Smile",
    description="+3 luck for next spin (cooldown 1)",
    effects=[
        Effect(
            type=EffectType.LUCK,
            amount=3,
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="common",
    cooldown_rounds=1
)

FourLeaf = Charm(
    name="Four Leaf",
    description="+9 luck for next spin (5% trigger chance)",
    effects=[
        Effect(
            type=EffectType.LUCK,
            amount=9,
            chance=5,
            trigger=Trigger.ON_SPIN_START,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="common"
)

OneMoreSpin = Charm(
    name="One More Spin",
    description="+1 max_spins next round (cooldown 3)",
    effects=[
        Effect(
            type=EffectType.MAX_SPINS,
            amount=1,
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            delay=Duration.ROUNDS(1),
            duration=Duration.ROUNDS(1)
        )
    ],
    rarity="common",
    cooldown_rounds=3
)

PocketRabbit = Charm(
    name="Pocket Rabbit",
    description="+1 luck for every charm bought this deadline, applied next spin. Throws itself away after triggering",
    effects=[
        Effect(
            type=EffectType.LUCK,
            amount=1 + (lambda gs: gs.get('charms_bought_this_deadline', 0)),
            chance=100,
            trigger=Trigger.ON_SPIN_START,
            condition=CharmBoughtThisDeadline(),
            calculate_fn=lambda gs: gs.get('charms_bought_this_deadline', 0),
            duration=Duration.SPINS(1),
            charm_life=Duration.SPINS(1)
        )
    ],
    rarity="common"
)

BrokenMirror = Charm(
    name="Broken Mirror",
    description="If you fail to score, next spin gains +4 luck",
    effects=[
        Effect(
            type=EffectType.LUCK,
            amount=4,
            chance=100,
            condition=PatternScored(0, 1, None, None, None),
            trigger=Trigger.ON_SPIN_START,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="common"
)

# ============================================================
# CHARM DEFINITIONS - UNCOMMON TIER (30% spawn rate base) (33% with upgrade)
# ============================================================

# Extra spin charm
Spare_Change = Charm(
    name="Spare Change",
    description="+2 max spins",
    effects=[
        Effect(
            type=EffectType.MAX_SPINS,
            amount=2,
            chance=100,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT
        )
    ],
    rarity="uncommon"
)

# Weight-active charms (cooldown based)
Struck_Gold = Charm(
    name="Struck Gold",
    description="+2 avg coin manifestation for the rest of the deadline",
    effects=[
        Effect(
            type=EffectType.WEIGHT_ACTIVE,
            target=Coin,
            amount=2,
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            duration=Duration.DEADLINE(1)
        )
    ],
    rarity="uncommon",
    cooldown_rounds=3
)

Trick_Deck = Charm(
    name="Trick Deck",
    description="+2 avg card manifestation for the rest of the deadline",
    effects=[
        Effect(
            type=EffectType.WEIGHT_ACTIVE,
            target=Card,
            amount=2,
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            duration=Duration.DEADLINE(1)
        )
    ],
    rarity="uncommon",
    cooldown_rounds=3
)

ILoveTops = Charm(
    name="I Love Tops",
    description="+2 avg spinner manifestation for the rest of the deadline",
    effects=[
        Effect(
            type=EffectType.WEIGHT_ACTIVE,
            target=Spinner,
            amount=2,
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            duration=Duration.DEADLINE(1)
        )
    ],
    rarity="uncommon",
    cooldown_rounds=3
)

Dice_Hard = Charm(
    name="Dice Hard",
    description="+2 avg dice manifestation for the rest of the deadline",
    effects=[
        Effect(
            type=EffectType.WEIGHT_ACTIVE,
            target=Dice,
            amount=2,
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            duration=Duration.DEADLINE(1)
        )
    ],
    rarity="uncommon",
    cooldown_rounds=3
)

WheelOfFortune = Charm(
    name="Wheel of Fortune",
    description="+2 avg wheel manifestation for the rest of the deadline",
    effects=[
        Effect(
            type=EffectType.WEIGHT_ACTIVE,
            target=Wheel,
            amount=2,
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            duration=Duration.DEADLINE(1)
        )
    ],
    rarity="uncommon",
    cooldown_rounds=3
)

SymbolBoost = Charm(
    name="Symbol Boost",
    description="Increase a chosen symbol's xmult by +1",
    effects=[
        Effect(
            type=EffectType.INCREASE_SYMBOL_MULTIPLIER,
            amount=1,
            chance=100,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="uncommon"
)

SymbolSurge = Charm(
    name="Symbol Surge",
    description="Increase a chosen symbol's xmult by +2",
    effects=[
        Effect(
            type=EffectType.INCREASE_SYMBOL_MULTIPLIER,
            amount=2,
            chance=100,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="uncommon"
)

CharmPocket = Charm(
    name="Charm Pocket",
    description="+1 charm space (doesn't take space)",
    effects=[
        Effect(
            type=EffectType.ADD_CHARM_SPACE,
            amount=1,
            chance=100,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="uncommon"
)

CharmHouse = Charm(
    name="Charm House",
    description="+2 charm space",
    effects=[
        Effect(
            type=EffectType.ADD_CHARM_SPACE,
            amount=2,
            chance=100,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="uncommon"
)

Blueprint = Charm(
    name="Blueprint",
    description="Gain the same effect as the last bought charm (while equipped)",
    effects=[
        Effect(
            type=EffectType.COPY_LAST_NON_BLUEPRINT_CHARM,
            chance=100,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="uncommon"
)

LeftWing = Charm(
    name="Left Wing",
    description="Reuse the effect of the first charm you sold",
    effects=[
        Effect(
            type=EffectType.COPY_FIRST_SOLD_CHARM,
            chance=100,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="uncommon"
)

PhoneReuse = Charm(
    name="Phone Reuse",
    description="When a phone ability is selected, stop it from reappearing. When this charm is thrown away, allow it to be reseen and reuse the phone ability",
    effects=[
        Effect(
            type=EffectType.PHONE_STORAGE,
            chance=100,
            trigger=Trigger.ON_THROWN_AWAY,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="uncommon"
)

CharmReappear = Charm(
    name="Charm Reappear",
    description="When a charm is thrown away, store it inside this charm. When this charm is thrown away, respawn the thrown away charm on the table",
    effects=[
        Effect(
            type=EffectType.CHARM_STORAGE,
            chance=100,
            trigger=Trigger.ON_THROWN_AWAY,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="uncommon"
)

TakeSpace = Charm(
    name="Take Space",
    description="When a charm that doesn’t take space is bought, store it inside this charm. Throwing away this charm reuses the charm in question immediately",
    effects=[
        Effect(
            type=EffectType.CHARM_STORAGE_NON_TAKE_SPACE,
            chance=100,
            trigger=Trigger.ON_THROWN_AWAY,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="uncommon"
)

I_cant_stop_winning = Charm(
    name="I can't stop winning",
    description="13% chance for Wheel and Card to have the chain modifier",
    effects=[
        Effect(
            type=EffectType.ADD_CHAIN,
            target=(Wheel, Card),
            amount=1,
            chance=13,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="uncommon"
)

ReRetrigger = Charm(
    name="Re-Retrigger",
    description="5% chance for Dice to have the recharge modifier",
    effects=[
        Effect(
            type=EffectType.ADD_RECHARGE_TARGET,
            target=Dice,
            amount=1,
            chance=5,
            trigger=Trigger.WHEN_BOUGHT,        
            duration=Duration.PERMANENT()
        )
    ],
    rarity="uncommon"
)

AGAINAGAINAGAIN = Charm(
    name="AGAINAGAINAGAIN",
    description="15% chance for Coin and Spinner to have the repetition modifier",
    effects=[
        Effect(
            type=EffectType.ADD_REPETITION,
            target=(Coin, Spinner),
            amount=1,
            chance=15,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT
        )
    ],
    rarity="uncommon"
)

LuckyReroll = Charm(
    name="Lucky Reroll",
    description="+1 max spins and +3 luck for first spin of next round",
    effects=[
        Effect(
            type=EffectType.MAX_SPINS,
            amount=1,
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            duration=Duration.ROUNDS(1)

        ),
        Effect(
            type=EffectType.LUCK,
            amount=3,
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="uncommon"
)

SymbolBlast = Charm(
    name="Symbol Blast",
    description="Increase a chosen symbol's xmult by +3",
    effects=[
        Effect(
            type=EffectType.INCREASE_SYMBOL_MULTIPLIER,
            amount=3,
            chance=100,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="uncommon"
)

# ============================================================
# CHARM DEFINITIONS - RARE TIER (20% spawn rate base) (22% with upgrade)
# ============================================================

ImBadAtMath = Charm(
name="I'm Bad At Math",
    description="35% chance to trigger patterns one more time",
    effects=[
        Effect(
            type=EffectType.RETRIGGER_PATTERN,
            chance=35,
            trigger=Trigger.ON_SPIN_START,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="rare"
)

Ramen = Charm(
    name="Ramen",
    description="Whenever you score 5 patterns, double the value of all symbols until the end of the round",
    effects=[
        Effect(
            type=EffectType.VALUE_DOUBLING,
            chance=100,
            condition=PatternScored(5, 1, None, None, None),
            duration=Duration.DEADLINES(1)
        )
    ],
    rarity="rare"
)

BeefBrisket = Charm(
    name="Beef Brisket",
    description="Whenever you score no money in a round, double all symbol mults, pattern mults, and 1.5 * earnings mult",
    effects=[
        Effect(
            type=EffectType.VALUE_BOOST_DROUGHT,
            chance=100,
            condition=ScorelessRound(),
            trigger=Trigger.ON_ROUND_END,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

FreeEarnings = Charm(
    name="Free Earnings",
    description="Earnings mult +1 permanently (doesn't take space)",
    effects=[
        Effect(
            type=EffectType.INCREASE_EARNINGS_MULTIPLIER,
            amount=1,
            chance=100,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

Bell = Charm(
    name="Bell",
    description="Symbols mult +1 permanently (cooldown 2)",
    effects=[
        Effect(
            type=EffectType.INCREASE_SYMBOL_MULTIPLIER,
            amount=1,
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare",
    cooldown=2
)

EverythingInExcess = Charm(
    name="Everything in Excess",
    description="Patterns mult +1 permanently for every time you earn 1.5x the required deadline's amount in a spin or round",
    effects=[
        Effect(
            type=EffectType.INCREASE_PATTERNS_MULTIPLIER,
            amount=1,
            chance=100,
            condition=EarningsThreshold(1.5),
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

NO_CHANGE = Charm(
    name="NO CHANGE",
    description="Patterns containing symbols other than Coin trigger one more time (cooldown 4)",
    effects=[
        Effect(
            type=EffectType.RETRIGGER_PATTERN,
            target=lambda pattern: not all(symbol == Coin for symbol in pattern.symbols),
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            duration=Duration.ROUNDS(1)
        )
    ],
    rarity="rare",
    cooldown=4
)

CoinExtraTrigger = Charm(
    name="Coin Rush",
    description="Patterns containing only Coins trigger two more times (cooldown 5)",
    effects=[
        Effect(
            type=EffectType.RETRIGGER_PATTERN(2),
            target=lambda pattern: all(symbol == Coin for symbol in pattern.symbols),
            chance=100,
            trigger=Trigger.ON_ACTIVATION,
            duration=Duration.ROUNDS(1)
        )
    ],
    rarity="rare",
    cooldown=5
)

PatternPulse = Charm(
    name="Pattern Pulse",
    description="70% chance to trigger patterns one more time for the rest of the spin when there are 10 pattern triggers in a spin",
    effects=[
        Effect(
            type=EffectType.RETRIGGER_PATTERN,
            chance=70,
            condition=PatternScored(10, 1, None, None, None),
            trigger=Trigger.PRE_SCORE,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="rare"
)

BigScore = Charm(
    name="Big Score",
    description="Whenever you score at least 8 patterns, triple all symbol values for the rest of the round",
    effects=[
        Effect(
            type=EffectType.VALUE_DOUBLING,
            chance=100,
            condition=PatternScored(8, 1, None, None, None),
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.ROUNDS(1)
        )
    ],
    rarity="rare"
)

DrySpellBoost = Charm(
    name="Dry Spell",
    description="Whenever you score no patterns or money in a round, increase all symbol and pattern values by 200% permanently",
    effects=[
        Effect(
            type=EffectType.VALUE_BOOST_DROUGHT,
            chance=100,
            condition=ScorelessRound(),
            trigger=Trigger.ON_ROUND_END,
            duration=Duration.PERMANENT
        )
    ],
    rarity="rare"
)

PatternSurge = Charm(
name="Pattern Surge",
    description="Patterns mult +2 permanently after scoring 10 patterns in a round",
    effects=[
        Effect(
            type=EffectType.INCREASE_PATTERNS_MULTIPLIER,
            amount=2,
            chance=100,
            condition=PatternScored(10, None, None, None, None),
            trigger=Trigger.ON_ROUND_END if PatternScored >= 10 and game_state.SPINS_LEFT == 0 else Trigger.ON_SPIN_END,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

LuckyCoinMath = Charm(
    name="Lucky Coin Math",
    description="30% chance to trigger all patterns one more  time if a coin pattern appears",
    effects=[
        Effect(
            type=EffectType.RETRIGGER_PATTERN,
            chance=30,
            condition=lambda pattern: any(symbol == Coin for symbol in pattern.symbols),
            trigger=Trigger.PRE_SCORE,
            duration=Duration.SPINS(1)
        )
    ],
    rarity="rare"
)

SymbolFrenzy = Charm(
    name="Symbol Frenzy",
    description="Symbols mult +2 permanently after scoring 5 jackpots in a round",
    effects=[
        Effect(
            type=EffectType.INCREASE_SYMBOLS_MULTIPLIER,
            amount=2,
            chance=100,
            condition=PatternScored(5, None, None, None, 15),
            trigger=Trigger.ON_ROUND_END if PatternScored >= 10 and game_state.SPINS_LEFT == 0 else Trigger.ON_SPIN_END,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

PatternWave = Charm(
    name="Pattern Wave",
    description="Patterns mult +2 permanently after scoring 7 patterns in one spin",
    effects=[
        Effect(
            type=EffectType.INCREASE_PATTERNS_MULTIPLIER,
            amount=2,
            chance=100,
            condition=PatternScored(7, 1, None, None, None),
            trigger=Trigger.ON_SPIN_END(),
            duration=Duration.PERMANENT()        
        )
    ],
    rarity="rare"
)

EarningsRush = Charm(
    name="Earnings Rush",
    description="Earnings mult +3 permanently (doesn't take space)",
    effects=[
        Effect(
            type=EffectType.INCREASE_EARNINGS_MULTIPLIER,
            amount=3,
            chance=100,
            trigger=Trigger.WHEN_BOUGHT,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

SymbolRitual = Charm(
    name="Symbol Ritual",
    description="Symbols mult +3 permanently after scoring 5+ different patterns in one spin",
    effects=[
        Effect(
            type=EffectType.INCREASE_SYMBOLS_MULTIPLIER,
            amount=3,
            chance=100,
            condition=UniquePatternCount(5, 1),
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

PatternChain = Charm(
    name="Pattern Chain",
    description="Patterns mult +1 permanently every time you score 5 patterns after a scoreless spin",
    effects=[
        Effect(
            type=EffectType.INCREASE_PATTERNS_MULTIPLIER,
            amount=1,
            chance=100,
            condition=ScorelessSpinFollowup(5),
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

DoubleCoinValues = Charm(
    name="Double Coin Values",
    description="Double all Coin values for the rest of the round after scoring 2+ Coin patterns in a spin",
    effects=[
        Effect(
            type=EffectType.VALUE_DOUBLING,
            chance=100,
            condition=PatternScored(2, 1, None, None, None) if all(symbol == Coin for symbol in Pattern.symbols) else None,
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.ROUNDS(1)
        )
    ],
    rarity="rare"
)

DoubleDiceValues = Charm(
    name="Double Dice Values",
    description="Double all Dice values for the rest of the round after scoring 2+ Dice patterns in a spin",
    effects=[
        Effect(
            type=EffectType.VALUE_DOUBLING,
            chance=100,
            condition=PatternScored(2, 1, None, None, None) if all(symbol == Dice for symbol in Pattern.symbols) else None,
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.ROUNDS(1)
        )
    ],
    rarity="rare"
)

DoubleSpinnerValues = Charm(
    name="Double Spinner Values",
    description="Double all Spinner values for the rest of the round after scoring 2+ Spinner patterns in a spin",
    effects=[
        Effect(
            type=EffectType.VALUE_DOUBLING,
            chance=100,
            condition=PatternScored(2, 1, None, None, None) if all(symbol == Spinner for symbol in Pattern.symbols) else None,
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.ROUNDS(1)
        )
    ],
    rarity="rare"
)

DoubleCardValues = Charm(
    name="Double Card Values",
    description="Double all Card values for the rest of the round after scoring 2+ Card patterns in a spin",
    effects=[
        Effect(
            type=EffectType.VALUE_DOUBLING,
            chance=100,
            condition=PatternScored(2, 1, None, None, None) if all(symbol == Card for symbol in Pattern.symbols) else None,
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.ROUNDS(1)
        )
    ],
    rarity="rare"
)

DoubleWheelValues = Charm(
    name="Double Wheel Values",
    description="Double all Wheel values for the rest of the round after scoring 2+ Wheel patterns in a spin",
    effects=[
        Effect(
            type=EffectType.VALUE_DOUBLING,
            chance=100,
            condition=PatternScored(2, 1, None, None) if all(symbol == Wheel for symbol in Pattern.symbols) else None,
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.ROUNDS(1)
        )
    ],
    rarity="rare"
)

DoubleAllPatterns = Charm(
    name="Double All Patterns",
    description="Double all pattern values for the rest of the round after scoring 7+ patterns in one spin",
    effects=[
        Effect(
            type=EffectType.VALUE_DOUBLING,
            chance=100,
            condition=PatternScored(7, 1, None, None, None),
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.ROUNDS(1)
        )
    ],
    rarity="rare"
)

EarningsWave = Charm(
    name="Earnings Wave",
    description="Double earnings mult for the rest of the round after scoring 18+ patterns in one spin",
    effects=[
        Effect(
            type=EffectType.INCREASE_EARNINGS_MULTIPLIER,
            chance=100,
            condition=PatternScored(18, 1, None, None, None),
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.ROUNDS(1)
        )
    ],
    rarity="rare"
)

SymbolEcho = Charm(
    name="Symbol Echo",
    description="Symbols mult +1 permanently after scoring 3 different symbol patterns in one spin",
    effects=[
        Effect(
            type=EffectType.INCREASE_SYMBOLS_MULTIPLIER,
            amount=1,
            chance=100,
            condition=UniqueSymbolCount(3, 1),
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

PatternEcho = Charm(
name="Pattern Echo",
    description="Patterns mult +1 permanently after scoring 5 different patterns in one spin",
    effects=[
        Effect(
            type=EffectType.INCREASE_PATTERNS_MULTIPLIER,
            amount=1,
            chance=100,
            condition=UniquePatternCount(5, 1),
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

EarningsEcho = Charm(
    name="Earnings Echo",
    description="Earnings mult +1 permanently after scoring 4 consecutive spins with no patterns",
    effects=[
        Effect(
            type=EffectType.INCREASE_EARNINGS_MULTIPLIER,
            amount=1,
            chance=100,
            condition=PatternScored(0, 4, None, None, None),
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

SymbolRally = Charm(
    name="Symbol Rally",
    description="Symbols mult +1 permanently after scoring 6+ same_symbol patterns in one deadline",
    effects=[
        Effect(
            type=EffectType.INCREASE_SYMBOLS_MULTIPLIER,
            amount=1,
            chance=100,
            condition=SameSymbolCount(6),
            trigger=Trigger.ON_ROUND_END if SameSymbolCount >= 6 and game_state.SPINS_LEFT == 0 else Trigger.ON_SPIN_END,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

PatternRally = Charm(
    name="Pattern Rally",
    description="Patterns mult +1 permanently after scoring 8+ patterns across two spins",
    effects=[
        Effect(
            type=EffectType.INCREASE_PATTERNS_MULTIPLIER,
            amount=1,
            chance=100,
            condition=PatternScored(8, None, 2, None, None),
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

EarningsRally = Charm(
    name="Earnings Rally",
    description="Earnings mult +2 permanently after scoring the same pattern 5 spins in a row",
    effects= [
        Effect(
            type=EffectType.INCREASE_EARNINGS_MULTIPLIER,
            amount=2,
            chance=100,
            condition=SamePatternScored(1, 5),
            trigger=Trigger.ON_ROUND_END if game_state.SPINS_LEFT == 0 else Trigger.ON_SPIN_END,
            duration=Duration.PERMANENT()
        )
    ],
    rarity="rare"
)

ValueSpill = Charm(
    name="Value Spill",
    description="Increase all symbol values by their current value/25 for the deadline after 10+ pattern triggers in one deadline",
    effects=[
        Effect(
            type=EffectType.SYMBOL_VALUE_INCREASE,
            chance=100,
            condition=PatternScored(10, None, None, None, None),
            trigger=Trigger.ON_ROUND_END if game_state.SPINS_LEFT == 0 else Trigger.ON_SPIN_END,
            duration=Duration.DEADLINES(1)
        )
    ],
    rarity="rare"
)

PatternReverb = Charm(
    name="Pattern Reverb",
    description="Double all pattern values, permanently after scoring 10 patterns in a spin without a Jackpot",
    effects=[
        Effect(
            type=EffectType.PATTERN_VALUE_DOUBLE,
            chance=100,
            condition=PatternScored(10, 1, None, 14, None),
            trigger=Trigger.ON_SPIN_END,
            duration=Duration.PERMANENT
        )
    ],
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
"20% symbol modifier chance (apply 2x). All xmults treated as x1. +4 luck. Activate: all values gain [x]x. x increases by 1 per 5 jackpots. +1 charm space permanently",
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
    "description": "20% symbol modifier chance (apply 2x). All xmults treated as x1. +4 luck. Activate: all values gain [x]x. x increases by 1 every 5 jackpots. +1 charm space permanently",
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
InfiniteStorage, RELOADING, Polynomial,

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