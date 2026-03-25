import random
from time import sleep

# ---------------- SYMBOLS ---------------- #

class Symbol:
    def __init__(self, name, base_value, current_value=None):
        self.name = name
        self.base_value = base_value
        self.current_value = current_value if current_value is not None else base_value
        self.display_name = name


class Coin(Symbol):
    weight = 30

    def __init__(self, name='Coin', base_value=3, current_value=None):
        super().__init__(name, base_value, current_value)

    def flip(self):
        result = random.choice(['Heads', 'Tails'])
        mult = 5 if result == 'Heads' else 1
        self.current_value = self.base_value * mult
        self.display_name = f"{self.name} ({result})"
        return self.current_value


class Spinner(Symbol):
    weight = 25

    def __init__(self, name='Spinner', base_value=2, current_value=None):
        super().__init__(name, base_value, current_value)

    def spin(self):
        mult = random.randint(1, 12)
        self.current_value = self.base_value * mult
        self.display_name = f"{self.name} (x{mult})"
        return self.current_value


class Dice(Symbol):
    weight = 20

    def __init__(self, name='Dice', base_value=5, sidemult=None, current_value=None):
        super().__init__(name, base_value, current_value)
        self.sidemult = sidemult

    def roll(self):
        self.sidemult = random.randint(1, 6)
        self.current_value = self.base_value * self.sidemult
        self.display_name = f"{self.name} (x{self.sidemult})"
        return self.current_value


class Card(Symbol):
    weight = 15

    def __init__(self, name='Card', base_value=3, current_value=None):
        super().__init__(name, base_value, current_value)

    def draw(self):
        value = random.randint(1, 13)
        self.current_value = self.base_value * value
        self.display_name = f"{self.name} (x{value})"
        return self.current_value


class Wheel(Symbol):
    weight = 10

    def __init__(self, name='Wheel', base_value=5, current_value=None):
        super().__init__(name, base_value, current_value)

    def spin(self):
        mult = random.randint(1, 10)
        self.current_value = self.base_value * mult
        self.display_name = f"{self.name} (x{mult})"
        return self.current_value


BASE_SYMBOL_CLASSES = [Dice, Coin, Spinner, Card, Wheel]


# ---------------- PATTERNS ---------------- #

class Pattern:
    def __init__(self, name, formations, base_multiplier_value, current_multiplier_value=None):
        self.name = name
        self.formations = formations
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = (
            current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
        )

    def matches(self, board):
        rows = len(board)
        cols = len(board[0])
        found = []

        for formation in self.formations:
            for start_x in range(rows):
                for start_y in range(cols):

                    anchor_symbol = board[start_x][start_y].name
                    match = True

                    for dx, dy in formation:
                        x = start_x + dx
                        y = start_y + dy

                        if not (0 <= x < rows and 0 <= y < cols):
                            match = False
                            break

                        if board[x][y].name != anchor_symbol:
                            match = False
                            break

                    if match:
                        found.append((start_x, start_y, anchor_symbol))

        return found

    def get_multiplier(self, symbol_value):
        return self.current_multiplier_value * symbol_value


class VerticalLine(Pattern):
    def __init__(self):
        super().__init__("Vertical Line", [[(0, 0), (1, 0), (2, 0)]], 1)


class HorizontalLine(Pattern):
    def __init__(self):
        super().__init__("Horizontal Line", [[(0, 0), (0, 1), (0, 2)]], 1)


class DiagonalLine(Pattern):
    def __init__(self):
        super().__init__(
            "Diagonal Line",
            [
                [(0, 0), (1, 1), (2, 2)],
                [(0, 2), (1, 1), (2, 0)]
            ],
            1
        )


class HorizontalLineLarge(Pattern):
    def __init__(self):
        super().__init__(
            "Horizontal Line Large",
            [[(0, 0), (0, 1), (0, 2), (0, 3)]],
            2
        )


class HorizontalLineXL(Pattern):
    def __init__(self):
        super().__init__(
            "Horizontal Line XL",
            [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]],
            3
        )


class Spoon(Pattern):
    def __init__(self):
        super().__init__(
            "Spoon",
            [
                [(0, 0), (0, 1), (1, 0), (1, 1),
                 (2, 0), (2, 1), (3, 1), (4, 1)],
                [(0, 1), (1, 1), (2, 1), (3, 2),
                 (4, 2), (4, 1), (3, 1), (3, 0), (4, 0)]
            ],
            5
        )


class Jackpot(Pattern):
    def __init__(self):
        super().__init__(
            "Jackpot",
            [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
              (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
              (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]],
            10
        )


PATTERNS = [
    VerticalLine(),
    HorizontalLine(),
    DiagonalLine(),
    HorizontalLineLarge(),
    HorizontalLineXL(),
    Spoon(),
    Jackpot()
]


# ---------------- BOARD ---------------- #

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.grand_total = 0

    def fill_cells(self, symbol_classes, weights_override=None):
        if weights_override is None:
            weights_override = {}

        weights = []
        for cls in symbol_classes:
            base_w = getattr(cls, "weight", 1)
            w = weights_override.get(cls, base_w)
            weights.append(w)

        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y] is None:
                    symbol_class = random.choices(symbol_classes, weights=weights, k=1)[0]
                    symbol = symbol_class()

                    if isinstance(symbol, Dice):
                        symbol.roll()
                    elif isinstance(symbol, Coin):
                        symbol.flip()
                    elif isinstance(symbol, Spinner):
                        symbol.spin()
                    elif isinstance(symbol, Card):
                        symbol.draw()
                    elif isinstance(symbol, Wheel):
                        symbol.spin()

                    self.grid[x][y] = symbol

    def print_board(self):
        print("\n=== BOARD ===")
        for row in self.grid:
            print(" | ".join(f"{symbol.display_name:12}" if symbol else "Empty" for symbol in row))
        print("=============\n")

    def current_spin(self, symbol_classes, weights_override=None):
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.fill_cells(symbol_classes, weights_override)
        self.print_board()

    def display_total(self, owned_charms):
        total = 0
        all_matches = []

        for pattern in PATTERNS:
            raw_matches = pattern.matches(self.grid)

            for (x, y, symbol_name) in raw_matches:
                for formation in pattern.formations:
                    cells = {(x + dx, y + dy) for (dx, dy) in formation}

                    if all(0 <= cx < self.rows and 0 <= cy < self.cols for (cx, cy) in cells):
                        all_matches.append((pattern, cells))
                        break

        def sort_key(item):
            pattern, cells = item

        all_matches.sort(key=sort_key)

        chosen = []
        used_cells = set()
        for pattern, cells in all_matches:
            
            if pattern.name == "Jackpot":
                chosen.append(pattern, cells)
                continue

            if any(cells.issubset(existing_cells)
                    for (p, existing_cells) in chosen
                    if p.name != "Jackpot"):
                        continue

            chosen.append((pattern, cells))
            used_cells |= cells
            
        retrigger_count = sum(1 for c in owned_charms if c.kind == "retrigger")
        triggers = 1 + retrigger_count
        sleep(1)
        print("\n=== PATTERN BREAKDOWN ===")
        for pattern, cells in chosen:
            symbol_values = [self.grid[x][y].current_value for (x, y) in cells]
            pattern_sum = sum(symbol_values)
            pattern_score = pattern.get_multiplier(pattern_sum)

            print(f"\nPattern: {pattern.name}")
            print(f"Cells: {sorted(list(cells))}")
            print("Symbols:")
            for (x, y) in sorted(list(cells)):
                s = self.grid[x][y]
                print(f"  ({x},{y}) -> {s.display_name} = {s.current_value}")

            print(f"Base Sum: {pattern_sum}")
            print(f"Multiplier: x{pattern.current_multiplier_value}")
            print(f"Triggers: {triggers}")
            print(f"Contribution: {pattern_score * triggers}")

            total += pattern_score * triggers

        print("\n=========================")
        print(f"Total Matches: {len(chosen)}")
        if all_matches != []:
            if Jackpot == True:
                print("Jackpot!!!")
            if retrigger_count > 0 and retrigger_count != 1:
                print(f"All patterns matched {retrigger_count} more times!")
            elif retrigger_count == 1:
                print(f'All patterns matched {retrigger_count} more time!')
            else:
                return None
        print(f"Total Value: {total}") 
        print("=========================\n")

        self.grand_total += total
        return total

# ---------------- CHARMS & STORE ---------------- #

class Charm:
    def __init__(self, name, description, kind, target=None, amount=0):
        """
        kind: 'extra_spin' or 'weight'
        target: symbol class for weight charms
        amount: delta to apply
        """
        self.name = name
        self.description = description
        self.kind = kind
        self.target = target
        self.amount = amount

    def __str__(self):
        return f"{self.name}: {self.description}"


# Charm definitions
Spare_Change = Charm(
    "Spare Change",
    "Gain +1 max spin per round.",
    kind="extra_spin"
)

ImBadAtMath = Charm(
    "I'm Bad At Math",
    "Patterns Trigger one more time",
    kind="retrigger",
    target=None,
    amount=1
)

Struck_Gold = Charm(
    "Struck Gold",
    "Coins appear more often (+5 weight).",
    kind="weight",
    target=Coin,
    amount=5
)

Trick_Deck = Charm(
    "Trick Deck",
    "Cards appear more often (+5 weight).",
    kind="weight",
    target=Card,
    amount=5
)

ILoveTops = Charm(
    "I Love Tops",
    "Spinners appear more often (+5 weight).",
    kind="weight",
    target=Spinner,
    amount=5
)

Dice_Hard = Charm(
    "Dice Hard",
    "Dice appear more often (+5 weight).",
    kind="weight",
    target=Dice,
    amount=5
)

WheelOfFortune = Charm(
    "Wheel of Fortune",
    "Wheels appear more often (+5 weight).",
    kind="weight",
    target=Wheel,
    amount=5
)

#more charms coming soon

ALL_CHARMS = [
    Spare_Change,
    Struck_Gold,
    Trick_Deck,
    ILoveTops,
    Dice_Hard,
    WheelOfFortune,
    ImBadAtMath
]


def compute_effective_max_spins(base_max_spins, owned_charms):
    extra = sum(1 for c in owned_charms if c.kind == "extra_spin")
    return base_max_spins + extra

def compute_weight_overrides(owned_charms):
    overrides = {}
    for c in owned_charms:
        if c.kind == "weight" and c.target is not None:
            base = overrides.get(c.target, getattr(c.target, "weight", 1))
            overrides[c.target] = base + c.amount
    return overrides


def store_phase(money, owned_charms):
    print("\nWelcome to the store.")
    print(f"You have ${money}. Charms cost $5 each.")
    stock_size = min(4, len(ALL_CHARMS))
    stock = random.sample(ALL_CHARMS, stock_size)

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

    idx = int(choice)-1
    if idx < 0 or idx >= len(stock):
        print("Invalid index. Leaving the store.")
        return money, owned_charms

    if money < 5:
        print("Not enough money to buy a charm.")
        return money, owned_charms

    chosen_charm = stock[idx]
    owned_charms.append(chosen_charm)
    money -= 5
    print(f"You bought: {chosen_charm.name}")

    return money, owned_charms


# ---------------- INPUT HELPERS ---------------- #

def get_spin_amount(money, max_spins):
    while True:
        spins = input(
            f"You have {money} dollars. Each spin costs 1 dollar.\n"
            f"Enter number of spins (max {max_spins}), press q to quit, or enter store to go to the store: "
        ).strip()

        if spins.lower() == "q":
            return "q"

        if spins.lower() == "store":
            return "store"

        if not spins.isdigit():
            print("Invalid input. Please enter a number.")
            continue

        spins = int(spins)

        if spins < 1:
            print("You must spin at least once.")
            continue

        if spins > max_spins:
            print(f"Maximum spins is {max_spins}. Please enter a valid number.")
            continue

        if spins > money:
            print(f"Not enough money for {spins} spins. You have {money} dollars.")
            continue

        return spins


# ---------------- GAME LOOP ---------------- #

def main():
    print("Welcome to the Slot Machine Game!")
    money = 16
    BASE_MAX_SPINS = 8
    owned_charms = []

    while money > 0:
        board = Board(3, 5)

        effective_max_spins = compute_effective_max_spins(BASE_MAX_SPINS, owned_charms)
        spins = get_spin_amount(money, effective_max_spins)

        if spins == "q":
            print("Thanks for playing!")
            break

        if spins == "store":
            money, owned_charms = store_phase(money, owned_charms)
            continue

        money -= spins

        weight_overrides = compute_weight_overrides(owned_charms)

        for i in range(spins):
            print(f"\n--- SPIN {i + 1} ---")
            board.current_spin(BASE_SYMBOL_CLASSES, weight_overrides)
            board.display_total(owned_charms)
            sleep(1)

        print("\n==============================")
        print("      FINAL GRAND TOTAL")
        print("==============================")
        print(board.grand_total)

        money += board.grand_total
        print(f"You now have ${money}.\n")
    print("You lost all your money. You lose")
    quit()
if __name__ == "__main__":
    main()