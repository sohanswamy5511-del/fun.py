from ast import pattern
import random
from time import sleep

from EventSystem import activate_charms

ANSI_RED = "\033[31m"
ANSI_RESET = "\033[0m"
ANSI_CLEAR_SCREEN = "\033[2J\033[H"

# Phone and Achievement system
PHONE_UPGRADE_LEVEL = 0
ACHIEVEMENTS_UNLOCKED = set()
CURRENT_PHONE_ABILITY = None

PHONE_ABILITY_UNLOCKS = {
    0: ["common", "uncommon", "rare"],
    1: ["uncommon", "rare", "legendary"],
    2: ["rare", "legendary", "exotic"],
    3: ["legendary", "exotic", "transcendent"]
}

ALL_OBTAINABLE_ABILITIES = []

# ============================================================
# PHONE ABILITIES (WITH UPGRADE PROBABILITIES)
# ============================================================
# Rarity probabilities change based on phone upgrades
# Base: Common 50%, Uncommon 30%, Rare 20%,
# Upgrade 1: Common 0%, Uncommon 60%, Rare 35%, Legendary 5%
# Upgrade 2: Common 0%, Uncommon 40%, Rare 50%, Legendary 9%, Exotic 1%
# Upgrade 3: Common 0%, Uncommon 0%, Rare 70%, Legendary 20%, Exotic 9%, Transcendent 1%

PHONE_ABILITIES = [
    # COMMON TIER (50% base, 0% with upgrade 1+)
    {"num": 1, "name": "Increase value of patterns by base value", "rarity": "common", "desc": "All patterns gain their base value"},
    {"num": 2, "name": "Double values of certain symbols", "rarity": "common", "desc": "Randomly double one symbol type"},
    {"num": 3, "name": "Restore charges on cooldown charms", "rarity": "common", "desc": "Reset all charm cooldowns"},
    
    # UNCOMMON TIER (30% base, 60% upgrade 1, 40% upgrade 2, 0% upgrade 3)
    {"num": 4, "name": "+1 manifestation for a symbol", "rarity": "uncommon", "desc": "Average +1 extra of one symbol type, permanently"},
    {"num": 5, "name": "Add a random trait to a charm", "rarity": "uncommon", "desc": "Enhance a charm with a trait"},
    {"num": 6, "name": "+1 charm space", "rarity": "uncommon", "desc": "Gain an extra charm slot"},
    
    # RARE TIER (15% base, 35% upgrade 1, 50% upgrade 2, 70% upgrade 3)
    {"num": 7, "name": "Remove mult options of a symbol", "rarity": "rare", "desc": "Simplify a symbol's multipliers"},
    {"num": 8, "name": "Increase Max mult of a symbol by 2", "rarity": "rare", "desc": "Higher multipliers for one symbol"},
    
    # LEGENDARY TIER (5% base, 5% upgrade 1, 9% upgrade 2, 20% upgrade 3)
    {"num": 9, "name": "Double Heads mult of coin", "rarity": "legendary", "desc": "Coin Heads becomes 10x instead of 5x"},
    {"num": 10, "name": "Remove all multipliers except 1 from a symbol", "rarity": "legendary", "desc": "Simplify a symbol's multipliers drastically"},
    {"num": 11, "name": "All cooldown charms take 1 less charge to recharge", "rarity": "legendary", "desc": "Speed up charm cooldowns (minimum 1)"},
    {"num": 12, "name": "+1 charm space", "rarity": "legendary", "desc": "Gain an extra charm slot (cannot be used 3+ times)"},
    {"num": 13, "name": "Increase max mult of all symbols by 10", "rarity": "legendary", "desc": "All symbols roll higher multipliers"},
    {"num": 14, "name": "Debt Decreases by 50%", "rarity": "legendary", "desc": "Next deadline amount reduced (uncopyable)"},
    {"num": 15, "name": "Apply a random trait to all charms", "rarity": "legendary", "desc": "Enhance all active charms (cannot apply eternal)"},
    {"num": 16, "name": "All patterns trigger one more time", "rarity": "legendary", "desc": "Every pattern gets +1 trigger permanently"},
    
    # EXOTIC TIER (1% upgrade 2, 9% upgrade 3)
    {"num": 17, "name": "I CAN LIVE FOREVER", "rarity": "exotic", "desc": "Give eternal trait to a charm (immune to destruction)"},
    {"num": 18, "name": "Spawn exotic charm & reset", "rarity": "exotic", "desc": "Spawn exotic charm, reset deadline, discard non-exotic/eternal charms"},
    {"num": 19, "name": "GODSMOS", "rarity": "exotic", "desc": "ALL charms trigger 1 more time permanently (does not reappear)"},
    {"num": 20, "name": "^1.2 to all patterns and symbols", "rarity": "exotic", "desc": "Multiply all pattern and symbol values permanently"},
    {"num": 21, "name": "^1.15 patterns, ^1.3 symbols, ^1.1 earnings", "rarity": "exotic", "desc": "Separate multipliers to each aspect"},
    {"num": 22, "name": "Gain 10% of deadline each round", "rarity": "exotic", "desc": "Passive income based on deadline (uncopyable, no reappear)"},
    {"num": 23, "name": "Apply trait to all charms & store", "rarity": "exotic", "desc": "All store charms get traits from now on"},
    {"num": 24, "name": "All charms cost 1 less", "rarity": "exotic", "desc": "Store charms now cost 1 less permanently (minimum FREE)"},
    
    # TRANSCENDENT TIER (1% upgrade 3)
    {"num": 25, "name": "Spawn 2 exotic charms", "rarity": "transcendent", "desc": "Add 2 exotic charms without destroying others"},
    {"num": 26, "name": "Spawn essence of the gods", "rarity": "transcendent", "desc": "Mysterious artifact appears (effects unknown)"},
]

def get_available_phone_abilities():
    """Return phone abilities available at the current phone upgrade level."""
    level = min(max(PHONE_UPGRADE_LEVEL, 0), max(PHONE_ABILITY_UNLOCKS.keys()))
    allowed_rarities = PHONE_ABILITY_UNLOCKS.get(level, ["common", "uncommon", "rare"])
    available = [ability for ability in PHONE_ABILITIES if ability["rarity"] in allowed_rarities]
    return available if available else PHONE_ABILITIES


def get_phone_ability_options():
    """Return a random sample of up to 3 obtainable phone abilities."""
    global ALL_OBTAINABLE_ABILITIES
    obtainable = get_available_phone_abilities()
    sample_size = min(3, len(obtainable))
    ALL_OBTAINABLE_ABILITIES = random.sample(obtainable, sample_size)
    return ALL_OBTAINABLE_ABILITIES


def show_phone_abilities():
    """Display available phone abilities for the player to choose from."""
    global CURRENT_PHONE_ABILITY
    
    available_abilities = get_phone_ability_options()

    print("\n" + "="*50)
    print(f"📞 PHONE ABILITIES - Choose one (Upgrade level {PHONE_UPGRADE_LEVEL}):")
    print("="*50)
    
    for idx, ability in enumerate(available_abilities, start=1):
        print(f"{idx}. {ability['name']} [{ability['rarity'].upper()}]")
        print(f"   {ability['desc']}")
    
    print("\nEnter the number of the ability to select, or 0 to skip:")
    
    while True:
        choice = input("> ").strip()
        
        if choice == "0":
            print("No ability selected.")
            CURRENT_PHONE_ABILITY = None
            break
        
        if not choice.isdigit():
            print("Invalid choice. Please enter a number.")
            continue
        
        choice_num = int(choice)
        
        if choice_num < 0 or choice_num > len(available_abilities):
            print(f"Invalid choice. Please enter 0-{len(available_abilities)}.")
            continue
        
        if choice_num == 0:
            print("No ability selected.")
            CURRENT_PHONE_ABILITY = None
            break
        
        selected = available_abilities[choice_num - 1]
        CURRENT_PHONE_ABILITY = selected
        print(f"✅ Selected: {selected['name']}")
        break
    
    print()

def trigger_button():
    """Activate the current phone ability."""
    if CURRENT_PHONE_ABILITY:
        print(f"📞 PHONE ABILITY TRIGGERED: {CURRENT_PHONE_ABILITY['name']}")
    else:
        print("No phone ability selected.")

def add_achievement(name):
    if name not in ACHIEVEMENTS_UNLOCKED:
        ACHIEVEMENTS_UNLOCKED.add(name)
        print(f"🏆 ACHIEVEMENT UNLOCKED: {name}")

# ============================================================
# ACHIEVEMENTS
# ============================================================
ACHIEVEMENTS_LIST = [
    "Score a Jackpot",
    "True Player: Unlock the World Ender",
    "777: Score your first 777",
    "Phone titan: Have all phone upgrades",
    "Trait master: All charms on table have traits",
    "#: Get into the numbers with hyperions",
    "Exotic master: Get all exotic charms",
    "Unlucky: Score no coins in a round",
    "Even Unluckier: Score no coins in a deadline",
    "I… Lost?: Lose",
    "Button master: Trigger button 5 times before spin",
    "Hey that's ME: Fuse to get Sohan Swamy"
]

# ============================================================
# HELPERS
# ============================================================

def has_available_cooldown_charms(owned_charms):

    return any(
        d['cooldown'] == 0
        and d['charm'].cooldown_rounds > 0
        for d in owned_charms
    )

# ============================================================
# DEADLINE SYSTEM
# ============================================================
class DeadlineSystem:
    """
    Deadline system with 3-round progression per deadline.

    - Each deadline lasts 3 rounds
    - Display "X rounds left" (starting at 3)
    - After each set of spins, rounds decrement
    - When rounds reach 0 rounds left, payment is MANDATORY
    - After payment, reset to 3 rounds left for next deadline
    - Deadline amounts increase by 300% (4x) each payment
    """

    def __init__(self):
        self.current_deadline = 1
        self.rounds_left = 3
        self.payments_made = 0

    def get_deadline_amount(self, deadline_num):
        """Calculate deadline amount based on deadline number."""
        return int(1200 * (4 ** (deadline_num - 1)))

    def get_current_total(self):
        """Return the current amount owed."""
        return self.get_deadline_amount(self.current_deadline)

    def get_status_string(self):
        """Return display string for rounds and deadline."""
        return f"💀 DEADLINE {self.current_deadline} | {self.rounds_left} rounds left | ${self.get_current_total():,}"

    def decrement_round(self):
        """Decrement rounds after a set of spins is completed."""
        self.rounds_left -= 1

    def must_pay(self):
        """Check if payment is mandatory (rounds reached 0)."""
        return self.rounds_left == 0

    def pay_deadline(self):
        """Pay the deadline and advance to next one."""
        self.current_deadline += 1
        self.rounds_left = 3
        self.payments_made += 1

    def can_choose_phone_ability(self):
        """Check if the player can choose a phone ability (deadline 2 or higher)."""
        return self.current_deadline >= 2

# ============================================================
# MAIN GAME LOOP
# ============================================================

def main():

    print("Welcome to the Slot Machine Game!")
    sleep(0.75)

    money = 12
    BASE_MAX_SPINS = 8

    owned_charms = []
    crafted_recipes = set()

    charm_space_max = 6

    deadlines = DeadlineSystem()

    board = Board(3, 5)

    resolver = CharmResolver()

    # ============================================================
    # CENTRAL GAME STATE
    # ============================================================

    game_state = {

    # Persistent modifiers
    'active_bonuses': {},

    # Multipliers
    'symbols_mult': 1,
    'patterns_mult': 1,

    # Runtime combat-style effects
    'repetition_targets': [],
    'chain_targets': [],
    'recharge_targets': [],

    # Misc
    'pending_luck': 0,
    'spins_left': 0
    }

    # ============================================================
    # INITIAL DEADLINE DISPLAY
    # ============================================================

    print(deadlines.get_status_string())
    print()

    # ============================================================
    # MAIN GAME LOOP
    # ============================================================

    while money > 0:

    # --------------------------------------------------------
    # EFFECTIVE MAX SPINS
    # --------------------------------------------------------

    max_spins = compute_effective_max_spins(
        BASE_MAX_SPINS,
        owned_charms
    )

    # --------------------------------------------------------
    # PLAYER CHOICE
    # --------------------------------------------------------

    choice = get_spin_amount(
        money,
        max_spins,
        owned_charms
    )

    # ========================================================
    # QUIT
    # ========================================================

    if choice == "q":
        print("Thanks for playing!")
        break

    # ========================================================
    # STORE
    # ========================================================

    if choice == "store":

        result = store_phase(
            money,
            owned_charms,
            crafted_recipes
        )

        if result:
            money, owned_charms = result

        continue

    # ========================================================
    # CRAFT
    # ========================================================

    if choice == "craft":

        crafted_recipes = craft_phase(
            owned_charms,
            crafted_recipes
        )

        continue

    # ========================================================
    # MANUAL CHARM ACTIVATION
    # ========================================================

    if choice == "charm":

        activate_charms(
            owned_charms,
            game_state,
            resolver
        )

        continue

    # ========================================================
    # DEADLINE PAYMENT
    # ========================================================

    if choice == "deadline_pay":

        deadline_amount = deadlines.get_current_total()

        if money >= deadline_amount:

            money -= deadline_amount

            print(
                f"Deadline paid! "
                f"You now have ${money}."
            )

            sleep(0.75)

            deadlines.pay_deadline()

            # Reset persistent bonus state
            game_state['active_bonuses'] = {}

            # Reset charm runtime tracking
            for d in owned_charms:

                d['activations_this_round'] = 0
                d['last_increase'] = 0

            reset_manifestation_targets(
                owned_charms
            )

            print(
                deadlines.get_status_string()
            )

        else:

            print(
                f"Insufficient funds. "
                f"Need ${deadline_amount:,}, "
                f"have ${money}."
            )

        continue

    # ========================================================
    # BUTTON
    # ========================================================

    if choice == "button":

        trigger_button()
        continue

    # ========================================================
    # START ROUND
    # ========================================================

    spins = choice
    spins_left = choice

    game_state['spins_left'] = spins_left

    board.start_round()

    money -= spins

    # --------------------------------------------------------
    # COOLDOWNS
    # --------------------------------------------------------

    for d in owned_charms:

        if d['cooldown'] > 0:
            d['cooldown'] -= 1

        d['activations_this_round'] = 0

    # --------------------------------------------------------
    # SPIN LUCK
    # --------------------------------------------------------

    spin_luck = compute_spin_luck(
        owned_charms,
        board
    )

    # --------------------------------------------------------
    # WEIGHT OVERRIDES
    # --------------------------------------------------------

    weight_overrides = compute_weight_overrides(
        BASE_SYMBOL_CLASSES,
        game_state['active_bonuses'],
        owned_charms
    )

    board.grand_total = 0

    patterns_scored_this_round = 0

    # ========================================================
    # SPINS
    # ========================================================

    for i in range(spins):

        # ----------------------------------------------------
        # RESET TEMPORARY EFFECTS EACH SPIN
        # ----------------------------------------------------

        game_state['symbols_mult'] = 1
        game_state['patterns_mult'] = 1

        game_state['repetition_targets'].clear()
        game_state['chain_targets'].clear()
        game_state['recharge_targets'].clear()

        # ----------------------------------------------------
        # RESOLVE PASSIVE CHARMS
        # ----------------------------------------------------

        for d in owned_charms:

            charm = d['charm']

            effects = resolver.resolve(
                charm,
                context=game_state
            )

            for effect in effects:

                if effect.effect_type == "ADD_SYMBOL_MULT":

                    game_state['symbols_mult'] *= (
                        effect.amount
                    )

                elif effect.effect_type == "ADD_PATTERN_MULT":

                    game_state['patterns_mult'] *= (
                        effect.amount
                    )

                elif effect.effect_type == "ADD_REPETITION":

                    game_state[
                        'repetition_targets'
                    ].append(
                        effect.target
                    )

                elif effect.effect_type == "ADD_CHAIN":

                    game_state[
                        'chain_targets'
                    ].append(
                        effect.target
                    )

                elif effect.effect_type == "ADD_RECHARGE_TARGET":

                    game_state[
                        'recharge_targets'
                    ].append(
                        effect.target
                    )

        # ----------------------------------------------------
        # CURRENT SPIN
        # ----------------------------------------------------

        board.current_spin(
            BASE_SYMBOL_CLASSES,
            weight_overrides,
            owned_charms,
            game_state['active_bonuses'],
            spin_luck,
            spin_number=i + 1,

            # NEW EFFECT STATE
            game_state=game_state
        )

        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

        board.display_total(
            owned_charms,
            spin_number=i + 1
        )

        patterns_scored_this_round += (
            board.patterns_scored_this_spin
        )

        # ====================================================
        # MID-ROUND CHARM ACTIVATION
        # ====================================================

        if (
            spins_left != 0
            and has_available_cooldown_charms(
                owned_charms
            )
        ):

            print(
                "\n📜 Activate charms?"
            )

            print(
                "(type 'charm' or press Enter)"
            )

            charm_input = (
                input("> ")
                .strip()
                .lower()
            )

            if charm_input == "charm":

                game_state['spins_left'] = (
                    spins_left
                )

                activate_charms(
                    owned_charms,
                    game_state,
                    resolver
                )

                spins_left = (
                    game_state['spins_left']
                )

                # Recompute weights
                weight_overrides = (
                    compute_weight_overrides(
                        BASE_SYMBOL_CLASSES,
                        game_state[
                            'active_bonuses'
                        ],
                        owned_charms
                    )
                )

        # ----------------------------------------------------
        # NEXT SPIN
        # ----------------------------------------------------

        if i + 1 < spins:

            input(
                "Press Enter to spin again..."
            )

            spins_left -= 1

            game_state['spins_left'] = (
                spins_left
            )

    # ========================================================
    # END ROUND
    # ========================================================

    deadlines.decrement_round()

    # --------------------------------------------------------
    # FINAL TOTAL
    # --------------------------------------------------------

    print("\n==============================")
    print("      FINAL GRAND TOTAL")
    print("==============================")

    print(board.grand_total)
    print()

    money += board.grand_total

    print(
        f"You now have ${money}.\n"
    )

    # ========================================================
    # WIN CONDITION
    # ========================================================

    if money >= 1000000:

        print(
            "WIN: You have reached "
            "$1,000,000!"
        )

        add_achievement(
            "Reach 1 Million"
        )

    # ========================================================
    # DEADLINE STATUS
    # ========================================================

    print(
        deadlines.get_status_string()
    )

    # ========================================================
    # MANDATORY DEADLINE PAYMENT
    # ========================================================

    if deadlines.must_pay():

        deadline_amount = (
            deadlines.get_current_total()
        )

        # ----------------------------------------------------
        # GAME OVER
        # ----------------------------------------------------

        if money < deadline_amount:

            print(
                f"\n💀 GAME OVER!"
            )

            print(
                f"You don't have enough "
                f"money to pay "
                f"${deadline_amount:,}."
            )

            print(
                f"You only have ${money}."
            )

            break

        # ----------------------------------------------------
        # FORCE PAYMENT
        # ----------------------------------------------------

        print(
            f"\n⚠️ DEADLINE REACHED!"
        )

        print(
            f"You must pay "
            f"${deadline_amount:,} "
            f"to proceed."
        )

        while True:

            choice = (
                input(
                    "Enter "
                    "'deadline_pay' "
                    "or '1' to pay: "
                )
                .strip()
                .lower()
            )

            if (
                choice == "deadline_pay"
                or choice == "1"
            ):

                money -= deadline_amount

                print(
                    f"💰 Deadline paid!"
                )

                print(
                    f"You now have ${money}."
                )

                sleep(0.75)

                deadlines.pay_deadline()

                # Reset persistent bonuses
                game_state[
                    'active_bonuses'
                ] = {}

                # Reset charm runtime tracking
                for d in owned_charms:

                    d[
                        'activations_this_round'
                    ] = 0

                    d[
                        'last_increase'
                    ] = 0

                reset_manifestation_targets(
                    owned_charms
                )

                print(
                    "\nNew deadline: "
                    + deadlines.get_status_string()
                )

                # Phone abilities
                if deadlines.can_choose_phone_ability():

                    show_phone_abilities()

                break

            else:

                print(
                    "Invalid input."
                )

    print()

    # ============================================================
    # GAME END
    # ============================================================

    print("\n" + "=" * 40)

    if money <= 0:

    print(
        "You lost all your money."
    )

    print("Game over.")

    else:

    print("Thanks for playing!")

    print("=" * 40)