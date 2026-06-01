ACHIEVEMENTS_UNLOCKED = set()

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
    "Button master: Trigger all cooldown charms in inventory 5 times in one round",
    "Hey that's ME: Fuse to get Sohan Swamy"
]