# main.py

from board import Board
from gamestate import game_state

from pattern import PATTERNS
from scoreengine import ScoreEngine

from eventsystem import (
    activate_charms,
    event_bus,
    CharmResolver
)

from symbol import BASE_SYMBOL_CLASSES


def find_matches(board):

    matches = []

    for pattern in PATTERNS:

        found = pattern.matches(
            board.grid
        )

        for cells in found:

            matches.append(
                (pattern, cells)
            )

    return matches


def run_game():

    board = Board(
        rows=3,
        cols=5
    )

    resolver = CharmResolver()

    score_engine = ScoreEngine()

    owned_charms = []

    # ----------------------------------
    # GAME LOOP
    # ----------------------------------

    while game_state["spins_left"] > 0:

        print(
            f"\n===== SPIN "
            f"{game_state['spins_left']} ====="
        )

        # ------------------------------
        # CHARM ACTIVATION
        # ------------------------------

        activate_charms(
            owned_charms,
            game_state,
            resolver,
            event_bus
        )

        # ------------------------------
        # SPIN BOARD
        # ------------------------------

        weights = [
            s.weight
            for s in BASE_SYMBOL_CLASSES
        ]

        board.spin(
            BASE_SYMBOL_CLASSES,
            weights
        )

        # ------------------------------
        # ACTIVATE SYMBOLS
        # ------------------------------

        for row in board.grid:

            for symbol in row:

                symbol.activate()

        # ------------------------------
        # FIND PATTERNS
        # ------------------------------

        matches = find_matches(
            board
        )

        # ------------------------------
        # SCORE
        # ------------------------------

        score = score_engine.score_patterns(
            matches,
            board,
            game_state
        )

        print(
            f"\nSpin Score: {score}"
        )

        game_state["spins_left"] -= 1

    print(
        "\n===== GAME OVER ====="
    )


if __name__ == "__main__":

    run_game()