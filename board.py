import random

class Board:

    # ============================================================
    # INIT
    # ============================================================

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols

        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    # ============================================================
    # SPIN
    # ============================================================

    def spin(self, symbol_classes, weights):

        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.fill_board(symbol_classes, weights)

        print("\n=== BOARD ===")
        for row in self.grid:
            print(" | ".join(s.display_name for s in row))

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
                )[0]

    # ============================================================
    # BOARD PRINT WITH HIGHLIGHT
    # ============================================================

    def print_board(self, highlight_cells=None, pattern_score=None):

        print("\n=== BOARD ===")

        highlight = set(highlight_cells or [])

        for x, row in enumerate(self.grid):
            line = []
            for y, s in enumerate(row):

                text = f"{s.display_name:14}"

                if (x, y) in highlight:
                    text = f"[{text}]"

                line.append(text)

            print(" | ".join(line))

        if pattern_score is not None:
            print(f"\nScore: {pattern_score}")