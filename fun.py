import random
from time import sleep

class Symbol:
    def __init__(self, name, base_value, current_value):
        self.name = name
        self.base_value = base_value
        self.current_value = current_value


# ---------------- SYMBOL TYPES ---------------- #

class Dice(Symbol):
    weight = 20  # manifestation chance

    def __init__(self, name='Dice', base_value=3, sidemult=None, current_value=None):
        super().__init__(name, base_value, current_value if current_value is not None else base_value)
        self.sidemult = sidemult
        self.display_name = name

    def roll(self):
        self.sidemult = random.randint(1, 10)
        self.current_value = self.base_value * self.sidemult
        self.display_name = f"{self.name} (x{self.sidemult})"
        return self.current_value


class Coin(Symbol):
    weight = 25

    def __init__(self, name='Coin', base_value=3, current_value=None):
        super().__init__(name, base_value, current_value if current_value is not None else base_value)
        self.display_name = name

    def flip(self):
        result = random.choice(['Heads', 'Tails'])
        self.current_value = self.base_value * (4 if result == 'Heads' else 1)
        self.display_name = f"{self.name} ({result})"
        return self.current_value


class Spinner(Symbol):
    weight = 30

    def __init__(self, name='Spinner', base_value=2, current_value=None):
        super().__init__(name, base_value, current_value if current_value is not None else base_value)
        self.display_name = name

    def spin(self):
        mult = random.randint(1, 10)
        self.current_value = self.base_value * mult
        self.display_name = f"{self.name} (x{mult})"
        return self.current_value


class Card(Symbol):
    weight = 15

    def __init__(self, name='Card', base_value=3, current_value=None):
        super().__init__(name, base_value, current_value if current_value is not None else base_value)
        self.display_name = name

    def draw(self):
        value = random.randint(1, 13)
        self.current_value = self.base_value * value
        self.display_name = f"{self.name} (x{value})"
        return self.current_value


class Wheel(Symbol):
    weight = 10

    def __init__(self, name='Wheel', base_value=5, current_value=None):
        super().__init__(name, base_value, current_value if current_value is not None else base_value)
        self.display_name = name

    def spin(self):
        mult = random.randint(1, 7)
        self.current_value = self.base_value * mult
        self.display_name = f"{self.name} (x{mult})"
        return self.current_value


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
        super().__init__("Diagonal Line",
            [
                [(0, 0), (1, 1), (2, 2)],   # main diagonal
                [(0, 2), (1, 1), (2, 0)]    # reverse diagonal (correct)
            ],
            1
        )


class HorizontalLineLarge(Pattern):
    def __init__(self):
        super().__init__("Horizontal Line Large",
                         [[(0, 0), (0, 1), (0, 2), (0, 3)]],
                         2)


class HorizontalLineXL(Pattern):
    def __init__(self):
        super().__init__("Horizontal Line XL",
                         [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]],
                         3)


class Spoon(Pattern):
    def __init__(self):
        super().__init__("Spoon",
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
        super().__init__("Jackpot",
            [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
              (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
              (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]],
            10
        )


# ---------------- BOARD ---------------- #

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.grand_total = 0

    def fill_cells(self, symbols):
        weights = [s.weight for s in symbols]

        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y] is None:

                    symbol_class = random.choices(symbols, weights=weights, k=1)[0]
                    symbol = symbol_class.__class__()

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

    def current_spin(self):
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.fill_cells([Dice(), Coin(), Spinner(), Card(), Wheel()])
        self.print_board()

    def display_total(self):
        total = 0

        patterns = [
            VerticalLine(),
            HorizontalLine(),
            DiagonalLine(),
            HorizontalLineLarge(),
            HorizontalLineXL(),
            Spoon(),
            Jackpot()
        ]

        all_matches = []

        for pattern in patterns:
            raw_matches = pattern.matches(self.grid)

            for (x, y, symbol_name) in raw_matches:
                for formation in pattern.formations:
                    cells = {(x + dx, y + dy) for (dx, dy) in formation}

                    if all(0 <= cx < self.rows and 0 <= cy < self.cols for (cx, cy) in cells):
                        all_matches.append((pattern, cells))
                        break

        def sort_key(item):
            pattern, cells = item
            is_jackpot = (pattern.name == "Jackpot")
            return (
                0 if is_jackpot else 1,
                -len(cells)
            )

        all_matches.sort(key=sort_key)

        used_cells = set()
        chosen = []

        for pattern, cells in all_matches:

            if pattern.name == "Jackpot":
                chosen.append((pattern, cells))
                continue

            if cells & used_cells:
                continue

            chosen.append((pattern, cells))
            used_cells |= cells

        total_matches = len(chosen)

        for pattern, cells in chosen:
            cx, cy = next(iter(cells))
            symbol_value = self.grid[cx][cy].current_value
            total += pattern.get_multiplier(symbol_value)

        print(f"Total Matches: {total_matches}")
        print(f"Total Value: {total}")

        self.grand_total += total
        return total


print("Welcome to the Slot Machine Game!")
money = 16

while True:
    board = Board(3, 5)
    spins = input(f'You have {money} dollars. Each spin costs 1 dollar. You can spin however many times you like: ')
    sleep(1)
    spins = int(spins)
    number = int(spins)
    sleep(2)

    while spins == number and money < number:
        print(f"Not enough money for {number} spins. Please enter a valid number of spins.")
        spins = input("Enter number of spins or press q to quit: ")
        if spins == "q":
            break
        while not spins.isdigit():
            spins = input("Invalid input. Please enter a valid number of spins.")
        spins = int(spins)

    money -= int(spins)

    for i in range(spins):
        print(f"\n--- SPIN {i+1} ---")
        board.current_spin()
        board.display_total()
        sleep(1)

    print("\n==============================")
    print("      FINAL GRAND TOTAL")
    print("==============================")
    print(board.grand_total)

    money += board.grand_total