"""

==========
sorlock.py
==========

Tools for making warlock to sorcerer conversion charts.

"""

CLASS_LEVELS = {
    7: {"WARLOCK": 5, "SORCERER": 2},
    8: {"WARLOCK": 5, "SORCERER": 3},
    9: {"WARLOCK": 5, "SORCERER": 4},
    10: {"WARLOCK": 5, "SORCERER": 5},
    11: {"WARLOCK": 5, "SORCERER": 6},
    12: {"WARLOCK": 5, "SORCERER": 7},
    13: {"WARLOCK": 5, "SORCERER": 8},
    14: {"WARLOCK": 5, "SORCERER": 9},
    15: {"WARLOCK": 5, "SORCERER": 10},
    16: {"WARLOCK": 5, "SORCERER": 11},
    17: {"WARLOCK": 5, "SORCERER": 12},
    18: {"WARLOCK": 5, "SORCERER": 13},
    19: {"WARLOCK": 5, "SORCERER": 14},
    20: {"WARLOCK": 5, "SORCERER": 15},
}
"""
Warlock and sorcerer levels by total level based on Shadowclaw's plan.
"""

SPELL_LEVEL_COST = {
    2: 1,
    3: 2,
    5: 3,
    6: 6,
    7: 5
}
"""
Conversion from sorcery points (keys) to spell slot level (values)
"""

PACT_MAGIC_LEVEL = {
    1: {"SLOT_LEVEL": 1, "NUM_SLOTS": 1},
    2: {"SLOT_LEVEL": 1, "NUM_SLOTS": 2},
    3: {"SLOT_LEVEL": 2, "NUM_SLOTS": 2},
    4: {"SLOT_LEVEL": 2, "NUM_SLOTS": 2},
    5: {"SLOT_LEVEL": 3, "NUM_SLOTS": 2},
    6: {"SLOT_LEVEL": 3, "NUM_SLOTS": 2},
    7: {"SLOT_LEVEL": 4, "NUM_SLOTS": 2},
    8: {"SLOT_LEVEL": 4, "NUM_SLOTS": 2},
    9: {"SLOT_LEVEL": 5, "NUM_SLOTS": 2},
    10: {"SLOT_LEVEL": 5, "NUM_SLOTS": 2},
    11: {"SLOT_LEVEL": 5, "NUM_SLOTS": 3},
    12: {"SLOT_LEVEL": 5, "NUM_SLOTS": 3},
    13: {"SLOT_LEVEL": 5, "NUM_SLOTS": 3},
    14: {"SLOT_LEVEL": 5, "NUM_SLOTS": 3},
    15: {"SLOT_LEVEL": 5, "NUM_SLOTS": 3},
    16: {"SLOT_LEVEL": 5, "NUM_SLOTS": 3},
    17: {"SLOT_LEVEL": 5, "NUM_SLOTS": 4},
    18: {"SLOT_LEVEL": 5, "NUM_SLOTS": 4},
    19: {"SLOT_LEVEL": 5, "NUM_SLOTS": 4},
    20: {"SLOT_LEVEL": 5, "NUM_SLOTS": 4},
}
"""
Table mapping warlock level to the pact magic slot level and number of those slots
"""

def level_to_sorcerer_warlock_levels(level):
    return CLASS_LEVELS[level]["SORCERER"], CLASS_LEVELS[level]["WARLOCK"]


def sorcerer_level_to_num_sorcery_points(sorcerer_level):
    return sorcerer_level


def spell_level_to_sorcery_points(spell_level):
    return spell_level


def sorcery_points_to_spell_slot(sorcery_points):
    return SPELL_LEVEL_COST[sorcery_points]


def spell_slot_to_sorcery_points(spell_slot):
    return spell_slot


def pact_magic_slots(warlock_level):
    return (
        PACT_MAGIC_LEVEL[warlock_level]["SLOT_LEVEL"],
        PACT_MAGIC_LEVEL[warlock_level]["NUM_SLOTS"]
    )


def buy_sorcery_points(pact_slots, pact_level, sorcery_points, sorcery_points_max):
    # Spend one pact slot
    new_sp = spell_level_to_sorcery_points(pact_level)
    sorcery_points = min(sorcery_points + new_sp, sorcery_points_max)
    pact_slots -= 1
    return [[pact_slots, sorcery_points, []]]


def buy_spell_slots(pact_slots, pact_level, sorcery_points, sorcery_points_max):
    # Spend sorcery points for spell slots
    options = []
    for sp in range(sorcery_points + 1):
        try:
            sorcerer_spell_level = sorcery_points_to_spell_slot(sp)
        except KeyError:
            # If there is a KeyError, this means we spent an invalid number of sorcery
            # points
            continue
        options.append([pact_slots, sorcery_points - sp, [sorcerer_spell_level]])
    return options


def spend_pact_slots(pact_slots, pact_level, sorcery_points, sorcery_points_max):
    """
    Spend pact slots for sorcer spell levels and sorcery points.

    Parameters
    ----------
    pact_slots : int
        Number of remaining pact slots
    pact_level : int
        The level of the pact slots
    sorcery_point : int
        The current number of sorcery points
    sorcery_points_max : int
        The maximum number of sorcery points you can have at any one time

    Returns
    -------
    pact_slots : int
        Number of remaining pact slots
    sorcery_points : int
        The current number of sorcery points
    sorcerer_spells : list
        List of the levels of purchased sorcerer spells
    """

    if pact_slots == 0:
        return pact_slots, sorcery_points, []

    
    purchase_options = [buy_sorcery_points, buy_spell_slots]

    receipts = []
    for purchase_option in purchase_options:
        purchases = purchase_option(
            pact_slots,
            pact_level,
            sorcery_points,
            sorcery_points_max
        )
        for purchase in purchases:
            new_pact_slots, new_sorcery_points, new_sorcery_spells = tuple(purchase)        
            
            receipts.append([new_pact_slots, new_sorcery_points, new_sorcery_spells])
            spend_pact_slots(new_pact_slots, pact_level, new_sorcery_points, sorcery_points_max)
    return receipts


def sorlock_table_level(level, pact_slots, sorcery_points):
    """
    Create table of all purchase options for pact slots

    Parameters
    ----------
    level : int
        Character level
    pact_slots : int
        The number of pact slots to spend
    sorcery_points : int
        The current number of sorcery points
    """

    # Get the sorcerer and warlock levels from the character level
    sorcerer_level, warlock_level = level_to_sorcerer_warlock_levels(level)
    
    # Make sure the number of pact slots and sorcery points are legal
    pact_level, pact_num_slots = pact_magic_slots(warlock_level)
    sorcery_points_max = sorcerer_level_to_num_sorcery_points(sorcerer_level)
    if pact_slots > pact_num_slots:
        raise RuntimeError(f"More pact slots than allowable. ({pact_slots} > {pact_num_slots})")
    if sorcery_points > sorcery_points_max:
        raise RuntimeError(f"More pact slots than allowable. ({sorcery_points} > {sorcery_points_max})")

    # Spend pact slots
    results = spend_pact_slots(pact_slots, pact_level, sorcery_points, sorcery_points_max)
