# ============================================================
# SYMBOL BASE CLASS
# ============================================================
import random

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
        super().__init__("Seven", base_value=None)

    def activate(self):
        pass


# ============================================================
# LIST OF ALL SYMBOL TYPES
# ============================================================

BASE_SYMBOL_CLASSES = [Dice, Coin, Spinner, Card, Wheel, Seven]