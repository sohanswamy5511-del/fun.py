#============================================================
#CHARM
#============================================================
from distro import name

class Charm:

    def __init__(
        self,
        name,
        description,
        effects=None,
        rarity="common",
        cooldown_rounds=0,
        weight=None,
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

from enum import Enum, auto

class count_scored:
    def __init__(self, count_stored):
        self.count_stored = count_stored
    def add_count(self):
        start_count_scored = 0
        self.count_scored = start_count_scored


class reset_count:
    ON_SPIN_END = auto()
    ON_ROUND_END = auto()
    ON_DEADLINE_END = auto()

    def reset():
        count_stored = 0
