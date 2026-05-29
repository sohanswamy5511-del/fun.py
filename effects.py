#============================================================
#EFFECT TYPES
#============================================================

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any
from conditions import Condition

class EffectType(Enum):

    LUCK = auto()
    EXTRA_SPIN = auto()
    WEIGHT_ACTIVE = auto()

    ADD_SYMBOL_MULT = auto()
    ADD_PATTERN_MULT = auto()

    ADD_REPETITION = auto()
    ADD_CHAIN = auto()
    ADD_RECHARGE_TARGET = auto()
#============================================================
#EFFECT
#============================================================

class Trigger(Enum):

    ON_SPIN_END = auto()
    ON_PATTERN_MATCH = auto()
    ON_PATTERN_FAIL = auto()

@dataclass
class Effect:

    type: EffectType
    target: Any = None
    amount: float = 0
    chance: float | None = None
    trigger: Trigger | None = None
    condition: Condition | None = None