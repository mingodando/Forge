LEVEL_XP_BASE = 40
LEVEL_XP_STEP = 20

# Each level has its own name. Early levels are cheap and named individually
# so new players see fresh titles often; the XP needed per level grows by
# LEVEL_XP_STEP every level, so the climb slowly gets steeper.
LEVEL_NAMES = [
    "Tinkerer", "Coal Sweeper", "Kindler", "Bellows Hand", "Ember Keeper",
    "Apprentice Smith", "Hammer Hand", "Anvil Novice", "Steel Initiate", "Forge Tender",
    "Journeyman Smith", "Iron Shaper", "Blade Apprentice", "Quench Hand", "Alloy Student",
    "Rivet Setter", "Temper Adept", "Forge Artisan", "Steel Adept", "Craft Sergeant",
    "Adept Forgemaster", "Ingot Warden", "Blade Artisan", "Sigil Smith", "Runed Hammer",
    "Master's Apprentice", "Foundry Overseer", "Steel Sentinel", "Forge Champion", "Ember Warlord",
    "Master Smith", "Grand Anvil", "Steel Virtuoso", "Forgeborn Elite", "Ironheart Master",
    "Sovereign Smith", "Flameforged Lord", "Ember Sovereign", "Anvil Legend", "Forge Sage",
    "Grandmaster", "Grand Forgemaster", "Steel Ascendant", "Ember Deity", "Forgefather",
    "Iron Colossus", "Blazing Sovereign", "Eternal Smith", "Mythic Forgemaster", "Legendary Forgemaster",
]


def xp_for_level(level):
    """XP required to advance from `level` to `level + 1`."""
    return LEVEL_XP_BASE + LEVEL_XP_STEP * level


def get_level_title(level):
    if level < len(LEVEL_NAMES):
        return LEVEL_NAMES[level]
    tier = level - len(LEVEL_NAMES) + 2
    return f"{LEVEL_NAMES[-1]} {tier}"


def get_level_info(xp):
    level = 0
    remaining = xp
    need = xp_for_level(level)
    while remaining >= need:
        remaining -= need
        level += 1
        need = xp_for_level(level)

    return {
        "level": level,
        "xp_into_level": remaining,
        "xp_to_next": need - remaining,
        "progress": remaining / need,
        "title": get_level_title(level),
    }
