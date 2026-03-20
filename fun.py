import random
class Symbol:
    def __init__(self, name, base_value, current_value):
        self.name = name
        self.base_value = base_value
        self.current_value = current_value
class Dice(Symbol):
    def __init__(self, name = 'Dice', base_value = 3, sidemult = None, current_value = None):
        self.name = name
        self.base_value = base_value
        self.sidemult = sidemult
        self.current_value = current_value if current_value is not None else self.base_value
    def roll(self):
        self.sidemult= random.randint(1, 10)
        self.current_value = self.base_value * self.sidemult if self.current_value is None else self.current_value * self.sidemult
        return self.current_value
    #alow one or two sides to be replaced with a different value if wanted
class Coin(Symbol):
    def __init__(self, name = 'Coin', base_value = 3, current_value = None):
        self.name = name
        self.base_value = base_value
        self.current_value = current_value if current_value is not None else self.base_value
    def flip(self):
        self.current_value = self.current_value * 4 if random.choice(['Heads', 'Tails']) == 'Heads' else self.current_value * 1 if self.current_value is not None else self.base_value * 2 if random.choice(['Heads', 'Tails']) == 'Heads' else self.base_value * 1
        return self.current_value
    #allow coin head flip quadrupling to be increased by 1 eventually, or doubled very late game
class Spinner(Symbol):
    def __init__(self, name = 'Spinner', base_value = 2, current_value = None):
        self.name = name
        self.base_value = base_value
        self.current_value = current_value if current_value is not None else self.base_value
    def spin(self):
        self.current_value = random.randint(1, 10) * self.base_value if self.current_value is None else random.randint(1, 10) * self.current_value
        return self.current_value
    #allow spinner to have more sides eventually
class Card(Symbol):
    def __init__(self, name = 'Card', base_value = 3, current_value = None):
        self.name = name
        self.base_value = base_value
        self.current_value = current_value if current_value is not None else self.base_value
    def draw(self):
        self.current_value = random.randint(1, 13) *self.base_value if self.current_value is None else random.randint(1, 13)* self.current_value
        return self.current_value
    def suit(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        return random.choice(suits)
    #give extra money if same suit or number in pattern soon
class Wheel(Symbol):
    def __init__(self, name = 'Wheel', base_value = 5, current_value = None):
        self.name = name
        self.base_value = base_value
        self.current_value = current_value if current_value is not None else self.base_value
    def spin(self):
        self.current_value = random.randint(1, 7) * self.base_value if self.current_value is None else random.randint(1, 7) * self.current_value
        return self.current_value
    #allow wheel to have more sides based on how many wheels are on the board, which I will implement eventually
class Pattern:
    def __init__(self, name, formations, base_multiplier_value, current_multiplier_value=None):
        self.name = name
        self.formations = formations  # list of lists of coordinate pairs
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = (
            current_multiplier_value if current_multiplier_value is not None
            else base_multiplier_value
        )

    def matches(self, board):
        rows = len(board)
        cols = len(board[0])
        found = []

        for formation in self.formations:
            max_x = max(dx for dx, _ in formation)
            max_y = max(dy for _, dy in formation)

            for start_x in range(rows - max_x):
                for start_y in range(cols - max_y):

                    anchor_symbol = board[start_x][start_y].name
                    match = True

                    for dx, dy in formation:
                        if board[start_x + dx][start_y + dy].name != anchor_symbol:
                            match = False
                            break

                    if match:
                        found.append((start_x, start_y, anchor_symbol))

        return found

    def get_multiplier(self, symbol_value):
        return self.current_multiplier_value * symbol_value
class VerticalLine(Pattern):
    def __init__(self, name = 'Vertical Line', base_multiplier_value = 1, current_multiplier_value = None):
        self.name = name
        self.formations = [[(0, 0), (1, 0), (2, 0)]]
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
class HorizontalLine(Pattern):
    def __init__(self, name = 'Horizontal Line', base_multiplier_value = 1, current_multiplier_value = None):
        self.name = name
        self.formations = [[(0, 0), (0, 1), (0, 2)]]
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
class DiagonalLine(Pattern):
    def __init__(self, name = 'Diagonal Line', base_multiplier_value = 1, current_multiplier_value = None):
        self.name = name
        self.formations = [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
class HorizontalLineLarge(Pattern):
    def __init__(self, name = 'Horizontal Line Large', base_multiplier_value = 2, current_multiplier_value = None):
        self.name = name
        self.formations = [[(0, 0), (0, 1), (0, 2), (0, 3)]]
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
class HorizontalLineXL(Pattern):
    def __init__(self, name = 'Horizontal Line XL', base_multiplier_value = 3, current_multiplier_value = None):
        self.name = name
        self.formations = [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]]
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
class Spoon(Pattern):
    def __init__(self, name = 'Spoon', base_multiplier_value = 5, current_multiplier_value = None):
        self.name = name
        self.formations = [[(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 1), (4, 1)], [(0, 1), (1, 1), (2, 1), (3, 2), (4, 2), (4, 1), (3, 1), (3, 0), (4, 0)]]
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
class Jackpot(Pattern):
    def __init__(self, name = 'Jackpot', base_multiplier_value = 10, current_multiplier_value = None):
        self.name = name
        self.formations = [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]]
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
    def place_symbol(self, x, y, symbol):
        if 0 <= x < self.rows and 0 <= y < self.cols:
            self.grid[x][y] = symbol
    def get_symbol(self, x, y):
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.grid[x][y]
        return None
    def fill_cells(self, symbols):
        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y] is None:
                    self.grid[x][y] = random.choice(symbols)
    def print_board(self):
        print("\n=== BOARD ===")
        for row in self.grid:
            print(" | ".join(f"{symbol.name:6}" if symbol else "Empty " for symbol in row))
        print("=============\n")
    def current_spin(self):
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.fill_cells([Dice(), Coin(), Spinner(), Card(), Wheel()])
        self.print_board()
        
    def display_total(self):
        total = 0
        total_matches = 0
        patterns = [
            VerticalLine(), 
            HorizontalLine(), 
            DiagonalLine(), 
            HorizontalLineLarge(), 
            HorizontalLineXL(), 
            Spoon(), 
            Jackpot()
        ]
        for pattern in patterns:
            matches = pattern.matches(self.grid)
            total_matches += len(matches)
            for x, y, symbol_name in matches:
                symbol_value = self.grid[x][y].current_value
                total += pattern.get_multiplier(symbol_value)
        self.print_board()
        return("Patterns found: " + str(total_matches)) + "\nTotal value: " + str(total)
current_spin = Board(3, 5)

