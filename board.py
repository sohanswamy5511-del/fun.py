import random

class Board:

    # ============================================================
    # INIT
    # ============================================================

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols

        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.highlighted_cells = set()

    # ============================================================
    # SPIN
    # ============================================================

    def spin(self, symbol_classes, weights):

        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.fill_board(symbol_classes, weights)
        self.highlighted_cells = set()  # Clear highlights for new spin

    def print_board(self):
        print("\n=== BOARD ===")
        for x, row in enumerate(self.grid):
            line = []
            for y, s in enumerate(row):
                symbol_str = s.display_name if s else "None"
                symbol_str = f"{symbol_str:^14}"

                if (x, y) in self.highlighted_cells:
                    symbol_str = f"\033[91m{symbol_str}\033[0m"

                line.append(symbol_str)
            print(" | ".join(line))

    # ============================================================
    # GRID
    # ============================================================

    def fill_board(self, symbol_classes, weights):

        for x in range(self.rows):
            for y in range(self.cols):

                if self.grid[x][y] is not None:
                    continue

                self.grid[x][y] = random.choices(
                    symbol_classes,
                    weights=weights,
                    k=1
                )[0]()

    # ============================================================
    # BOARD PRINT WITH HIGHLIGHT
    # ============================================================

    def add_highlight(self, cells):
        """Add cells to the highlight set."""
        self.highlighted_cells.update(cells)

    def clear_highlights(self):
        """Clear any highlighted cells."""
        self.highlighted_cells.clear()