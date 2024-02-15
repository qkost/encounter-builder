"""

==========
sorlock.py
==========

Tools for making warlock to sorcerer conversion charts.

"""

import pandas as pd

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
    6: 4,
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


class SorlockState:

    def __init__(
            self,
            pact_slots,
            pact_level,
            sorcerer_spells,
            sorcery_points,
            sorcery_point_max=None
        ):
        """
        Constructor for SorlockState

        Parameters
        ----------
        pact_slots : int
            Number of remaining pact slots
        pact_level : int
            The level of the pact slots
        sorcery_points : int
            The current number of sorcery points
        sorcerer_spells : list
            List of the purchased sorcerer spells
        sorcery_point_max : int, optional
            The maximum number of sorcery points you can have at any one time. Defaults
            to None
        """

        # Save attributes
        self.pact_slots = pact_slots
        self.pact_level = pact_level
        self.sorcerer_spells = sorted(sorcerer_spells)
        self.sorcery_points = sorcery_points        
        self.sorcery_point_max = sorcery_point_max

    @classmethod
    def from_level(cls, level, pact_slots=None, sorcery_points=None):
        # Get the sorcerer and warlock levels from the character level
        sorcerer_level, warlock_level = level_to_sorcerer_warlock_levels(level)
        pact_level, pact_num_slots = pact_magic_slots(warlock_level)
        sorcery_point_max = sorcerer_level_to_num_sorcery_points(sorcerer_level)

        if pact_slots is None:
            pact_slots = pact_num_slots
        if sorcery_points is None:
            sorcery_points = sorcery_point_max

        # Make sure the number of pact slots and sorcery points are legal
        if pact_slots > pact_num_slots:
            raise RuntimeError(
                f"More pact slots than allowable. ({pact_slots} > {pact_num_slots})"
            )
        if sorcery_points > sorcery_point_max:
            raise RuntimeError(
                "More pact slots than allowable. "
                f"({sorcery_points} > {sorcery_point_max})"
            )

        return SorlockState(
            pact_slots,
            pact_level,
            [],
            sorcery_points,
            sorcery_point_max=sorcery_point_max
        )


    def buy_sorcery_points(self):
        # Spend one pact slot
        purchased_sp = spell_level_to_sorcery_points(self.pact_level)

        # Update current values
        new_sorcery_points = min(self.sorcery_points + purchased_sp, self.sorcery_point_max)
        new_pact_slots = self.pact_slots -1
    
        return [SorlockState(
            new_pact_slots,
            self.pact_level,
            self.sorcerer_spells,
            new_sorcery_points,
            sorcery_point_max=self.sorcery_point_max
        )]


    def buy_spell_slots(self):
        # Spend sorcery points for spell slots
        options = []
        for sp in range(self.sorcery_points + 1):
            try:
                sorcerer_spell_level = sorcery_points_to_spell_slot(sp)
            except KeyError:
                # If there is a KeyError, this means we spent an invalid number of sorcery
                # points
                continue
            options.append(SorlockState(
                self.pact_slots,
                self.pact_level,
                self.sorcerer_spells + [sorcerer_spell_level],
                self.sorcery_points - sp,
                sorcery_point_max=self.sorcery_point_max
            ))


        return options
    
    def __str__(self):
        return (
            f"Warlock ({self.pact_slots}x{self.pact_level}), "
            f"Sorcerer ({self.sorcerer_spells}, {self.sorcery_points} sp)"
        )

    def spell_counts_by_level(self):
        return [self.sorcerer_spells.count(x) for x in range(1, 10)]

    def to_dict(self):
        _dict = {f"level{level + 1}": count for level, count in enumerate(self.spell_counts_by_level())}
        # _dict["pact_slots"] = self.pact_slots
        # _dict["pact_level"] = self.pact_level
        _dict["sorcery_points"] =self.sorcery_points
        return _dict


def spend_pact_slots(state):
    """
    Spend pact slots for sorcer spell levels and sorcery points.

    Parameters
    ----------
    state : Sorlock State
        Starting state of Sorlock with pact slots and such

    Returns
    -------
    next_states : list
        List of possible next states
    """
    
    if state.pact_slots == 0:
        return [state]
        
    purchase_options = [state.buy_sorcery_points, state.buy_spell_slots]

    next_states = []
    for purchase_option in purchase_options:
        next_states.extend(purchase_option())

    return_states = []
    for next_state in next_states:
        entries = spend_pact_slots(next_state)
        for entry in entries:
            if entry.pact_slots == 0:
                return_states.append(entry)
    return return_states


def sorlock_table_level(state):
    """
    Create table of all purchase options for pact slots

    Parameters
    ----------
    state : Sorlock State
        Starting state of Sorlock with pact slots and such
    """    
    
    # Spend pact slots
    results = spend_pact_slots(state)

    # Form dataframe
    df = pd.DataFrame([result.to_dict() for result in results])

    # Trim things up
    df = df.drop_duplicates()
    df = df.loc[:, (df != 0).any(axis=0)].reset_index(drop=True)


    # https://stackoverflow.com/questions/68522283/removing-dominated-rows-from-a-pandas-dataframe-rows-with-all-values-lower-th
    # Broadcasted comparison explanation below
    cmp = (df.values[:, None] <= df.values).all(axis=2).sum(axis=1) == 1
    df = df[cmp].reset_index(drop=True)

    # Sort the list intelligently
    level_cols = [col for col in df.columns if "level" in col]
    df = df.sort_values(sorted(level_cols, reverse=True) + ["sorcery_points"]).reset_index(drop=True)

    return df