#============================================================
#RESOLVER
#============================================================

import random

class CharmResolver:
    """
    Converts charms into executable effects.
    """

    def resolve(self, charm, context=None):

        resolved = []

        for effect in charm.effects:

            # ------------------------------------------------
            # CHANCE CHECK
            # ------------------------------------------------

            if effect.chance is not None:

                if random.random() > effect.chance / 100:
                    continue

            resolved.append(effect)

        return resolved