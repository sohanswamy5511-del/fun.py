#============================================================
#EFFECT TYPES
#============================================================

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any
from conditions import Condition

class EffectType(Enum):

    # Core effects
    LUCK = auto()
    SPINS_LEFT = auto()
    MAX_SPINS = auto()
    EXTRA_SPIN = auto()
    
    # Modifiers
    GOLD_MODIFIER = auto()
    WEIGHT_ACTIVE = auto()
    INCREASE_SYMBOL_MULT = auto()
    INCREASE_PATTERN_MULT = auto()
    
    # Pattern effects
    ADD_REPETITION = auto()
    ADD_CHAIN = auto()
    ADD_RECHARGE_TARGET = auto()
    GUARANTEE_PATTERN = auto()
    
    # Dynamic effects
    DYNAMIC_GOLD_CHANCE = auto()
    
    # Charm system effects - Storage
    ADD_CHARM_SPACE = auto()
    CHARM_STORAGE = auto()
    CHARM_STORAGE_NON_TAKE_SPACE = auto()
    PHONE_STORAGE = auto()
    
    # Charm system effects - Copying
    COPY_LAST_NON_BLUEPRINT_CHARM = auto()
    COPY_FIRST_SOLD_CHARM = auto()
    
    # Multiplier effects
    EARNINGS_MULT = auto()
    SYMBOLS_MULT = auto()
    PATTERNS_MULT = auto()
    
    # Special triggers
    RETRIGGER_PATTERN = auto()
    SYMBOL_VALUE_DOUBLE = auto()
    VALUE_BOOST_DROUGHT = auto()
#============================================================
#EFFECT
#============================================================

class Trigger(Enum):

    ON_SPIN_START = auto()
    PRE_SCORE = auto()
    ON_SPIN_END = auto()
    ON_ACTIVATION = auto() # When the charm is activated (cooldown)
    ON_PATTERN_MATCH = auto()
    ON_PATTERN_FAIL = auto()
    WHEN_BOUGHT = auto() #when charm is bought (permanent basically)
    ON_THROWN_AWAY = auto()
    ON_ROUND_END = auto()

@dataclass
class Effect:

    type: EffectType
    target: Any = None
    amount: float = 0
    chance: float | None = None
    trigger: Trigger | None = None
    condition: Condition | None = None
    calculate_fn: Any = None 

# Duration
class Duration(Enum):
    
    PERMANENT = auto() # Lasts indefinitely while the charm is held
    SPINS = auto() # Lasts for a certain number of spins
    ROUNDS = auto() # Lasts for a certain number of rounds
    DEADLINES = auto() # Lasts for a certain amount of real time (not implemented yet