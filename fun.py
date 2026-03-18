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
    def __init__(self, name, formation, base_multiplier_value, current_multiplier_value = None):
        self.name = name
        self.formation = formation
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
    def matches(self, board):
        rows = len(board)
        cols = len(board[0])
        max_x = max(x for x, _ in self.formation)
        max_y = max(y for _, y in self.formation)
        for start_x in range(rows - max_x):
            for start_y in range(cols - max_y):
                first_value = board[start_x][start_y].current_value
                match = True
                for dx, dy in self.formation:
                    if board[start_x + dx][start_y + dy].current_value != first_value:
                        match = False
                        break
                if match:
                    return True
        return False
    def get_multiplier(self):
        return self.current_multiplier_value * self.symbol.current_value if self.current_multiplier_value is not None else self.base_multiplier_value * self.symbol.current_value
class VerticalLine(Pattern):
    def __init__(self, name = 'Vertical Line', base_multiplier_value = 1, current_multiplier_value = None):
        self.name = name
        self.formation = [(0, 0), (1, 0), (2, 0)]
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
class HorizontalLine(Pattern):
    def __init__(self, name = 'Horizontal Line', base_multiplier_value = 1, current_multiplier_value = None):
        self.name = name
        self.formation = [(0, 0), (0, 1), (0, 2)]
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
class DiagonalLine(Pattern):
    def __init__(self, name = 'Diagonal Line', base_multiplier_value = 1, current_multiplier_value = None):
        self.name = name
        self.formation = [(0, 0), (1, 1), (2, 2)] or [(0, 2), (1, 1), (2, 0)]
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
class HorizontalLineLarge(Pattern):
    def __init__(self, name = 'Horizontal Line Large', base_multiplier_value = 2, current_multiplier_value = None):
        self.name = name
        self.formation = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
class HorizontalLineXL(Pattern):
    def __init__(self, name = 'Horizontal Line XL', base_multiplier_value = 3, current_multiplier_value = None):
        self.name = name
        self.formation = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value
class Spoon(Pattern):
    def __init__(self, name = 'Spoon', base_multiplier_value = 5, current_multiplier_value = None):
        self.name = name
        self.formation = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 1), (4, 1)]
        self.base_multiplier_value = base_multiplier_value
        self.current_multiplier_value = current_multiplier_value if current_multiplier_value is not None else base_multiplier_value