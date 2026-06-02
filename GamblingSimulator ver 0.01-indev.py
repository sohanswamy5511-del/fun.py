
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
from deadlines import DeadlineSystem


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

    # Initialize deadline system and starting balance
    deadline_system = DeadlineSystem()
    game_state["balance"] = 12   # Starting money with store coverage
    game_state["total_winnings"] = 0
    spin_count = 0

    # ----------------------------------
    # GAME LOOP
    # ----------------------------------

    while game_state["balance"] > 0:

        print(
            f"\n{'='*60}"
        )
        print(
            f"Balance: ${game_state['balance']:,} | "
            f"{deadline_system.get_status_string()}"
        )

        # Check if deadline payment is mandatory
        if deadline_system.must_pay():
            deadline_amount = deadline_system.get_current_total()
            
            if game_state["balance"] < deadline_amount:
                print(
                    f"\n❌ FAILED TO PAY DEADLINE!"
                )
                print(
                    f"Owed: ${deadline_amount:,} | "
                    f"Balance: ${game_state['balance']:,}"
                )
                print(
                    f"\n===== GAME OVER ====="
                )
                print(
                    f"Total winnings: ${game_state['total_winnings']:,}"
                )
                break
            
            # Make payment
            game_state["balance"] -= deadline_amount
            print(
                f"\n💸 PAID DEADLINE: ${deadline_amount:,}"
            )
            print(
                f"Remaining balance: ${game_state['balance']:,}"
            )
            deadline_system.pay_deadline()
            continue

        # Ask player how many spins for this round
        while True:
            choice = input(
                f"\nRounds left: {deadline_system.rounds_left} | "
                f"Choose spins - [4] or [8]? "
            ).strip()
            
            if choice in ["4", "8"]:
                spins_this_round = int(choice)
                break
            else:
                print("Invalid choice. Please enter 4 or 8.")

        # Execute the chosen number of spins
        for _ in range(spins_this_round):

            spin_count += 1
            print(
                f"\n===== SPIN {spin_count} ====="
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
                f"Spin Score: {score}"
            )

            # Update balance and winnings
            game_state["balance"] += score
            game_state["total_winnings"] += score

            print(
                f"Balance: ${game_state['balance']:,}"
            )

            # Stop if balance hits zero
            if game_state["balance"] <= 0:
                break

        # Decrement deadline rounds after all spins this round
        if game_state["balance"] > 0:
            deadline_system.decrement_round()

    print(
        f"\n===== GAME OVER ====="
    )
    print(
        f"Spins completed: {spin_count}"
    )
    print(
        f"Total winnings: ${game_state['total_winnings']:,}"
    )


if __name__ == "__main__":

    run_game()