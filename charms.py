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