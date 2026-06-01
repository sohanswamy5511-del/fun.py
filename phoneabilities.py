# Phone system
PHONE_UPGRADE_LEVEL = 0
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