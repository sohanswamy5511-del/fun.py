
import random

from board import Board
from gamestate import game_state

from charmdefinitions import get_all_obtainable_charms
from pattern import PATTERNS
from phoneabilities import show_phone_abilities
from scoreengine import ScoreEngine

from eventsystem import (
    activate_charms,
    event_bus,
    CharmResolver
)

from symbol import BASE_SYMBOL_CLASSES
from deadlines import DeadlineSystem


def create_store_inventory(crafted_recipes=None):
    obtainable = get_all_obtainable_charms(crafted_recipes)
    sample_size = min(4, len(obtainable))
    return random.sample(obtainable, sample_size) if obtainable else []


def build_charm_entry(charm):
    return {
        'charm': charm,
        'cooldown': 0,
        'uses': 0,
        'activations_this_round': 0
    }


def show_store(store_inventory, game_state, owned_charms):
    while True:
        print("\n" + "="*50)
        print("🛒 STORE - $5 per charm, $4 restock")
        print("="*50)

        if not store_inventory:
            print("Store is currently empty.")
        else:
            for idx, charm in enumerate(store_inventory, start=1):
                print(
                    f"{idx}. {charm.name} [{charm.rarity}] - {charm.description}"
                )

        print("\nR. Restock store ($4)")
        print("0. Leave store")
        choice = input("> ").strip().lower()

        if choice == "0":
            break

        if choice == "r":
            if game_state["balance"] < 4:
                print("Not enough balance to restock the store.")
                continue
            game_state["balance"] -= 4
            store_inventory[:] = create_store_inventory()
            print("Store restocked.")
            continue

        if not choice.isdigit():
            print("Invalid choice. Enter a number, R, or 0.")
            continue

        idx = int(choice)
        if idx < 1 or idx > len(store_inventory):
            print("Invalid choice. Enter a valid charm number.")
            continue

        if game_state["balance"] < 5:
            print("Not enough balance to buy that charm.")
            continue

        purchased = store_inventory.pop(idx - 1)
        game_state["balance"] -= 5
        game_state["charms_bought_this_deadline"] += 1
        game_state["last_bought_charm"] = purchased.name
        owned_charms.append(build_charm_entry(purchased))
        print(f"Bought {purchased.name} for $5.")

    return store_inventory


def craft_menu():
    print("\n" + "="*50)
    print("🛠️  Crafting menu (coming soon)")
    print("="*50)
    print("Crafting is not implemented yet. Check back after future updates.")
    print()


def find_matches(board):

    raw_matches = []

    for pattern in PATTERNS:

        found = pattern.matches(
            board.grid
        )

        for cells in found:
            raw_matches.append((pattern, cells))

    filtered_matches = []

    for pattern, cells in raw_matches:
        if pattern.name == "Jackpot":
            filtered_matches.append((pattern, cells))
            continue

        is_contained = any(
            len(other_cells) > len(cells)
            and cells.issubset(other_cells)
            and other_pattern.name != "Jackpot"
            for other_pattern, other_cells in raw_matches
            if other_pattern is not pattern or other_cells != cells
        )

        if not is_contained:
            filtered_matches.append((pattern, cells))

    return filtered_matches


def run_game():

    board = Board(
        rows=3,
        cols=5
    )

    resolver = CharmResolver()

    score_engine = ScoreEngine()

    owned_charms = []
    store_inventory = create_store_inventory()

    # Initialize deadline system and starting balance
    deadline_system = DeadlineSystem()
    game_state["balance"] = 12   # Starting money with store coverage
    game_state["total_winnings"] = 0
    game_state["charms_bought_this_deadline"] = 0
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
            game_state["charms_bought_this_deadline"] = 0
            if deadline_system.can_choose_phone_ability():
                show_phone_abilities()
            continue

        # Ask player how many spins for this round
        while True:
            choice = input(
                f"\nRounds left: {deadline_system.rounds_left} | "
                f"Choose spins - [4] or [8], [S]tore, [D]eadline pay, [C]raft: "
            ).strip().lower()

            if choice in ["4", "8"]:
                spins_this_round = int(choice)
                break

            if choice == "s":
                store_inventory = show_store(store_inventory, game_state, owned_charms)
                continue

            if choice == "d":
                deadline_amount = deadline_system.get_current_total()
                if game_state["balance"] < deadline_amount:
                    print("Not enough balance to pay the deadline early.")
                else:
                    game_state["balance"] -= deadline_amount
                    deadline_system.pay_deadline()
                    game_state["charms_bought_this_deadline"] = 0
                    print(f"Paid deadline early for ${deadline_amount:,}.")
                    if deadline_system.can_choose_phone_ability():
                        show_phone_abilities()
                continue

            if choice == "c":
                craft_menu()
                continue

            print("Invalid choice. Please enter 4, 8, S, D, or C.")

        # Execute the chosen number of spins
        for spin_index in range(spins_this_round):

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

            # Stop if balance hits zero
            if game_state["balance"] <= 0:
                break

            # Wait for user confirmation before the next respin
            if spin_index < spins_this_round - 1:
                input("\nPress Enter to respin...")

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