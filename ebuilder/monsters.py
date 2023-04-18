"""

===========
monsters.py
===========

Tools for modeling the monster's power

"""


import os


import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

MONSTER_POWER = pd.read_csv(os.path.join(
    DATA_DIR,
    "monster_power.csv"
)).set_index("cr")


class Monster():
    """Class for modeling monster power"""

    def __init__(self, name, cr, bypass_damage=False, ohko=False):
        """
        Constructor for monster

        Parameters
        ----------
        name : str
            Name of monster
        cr : int
            Monster challenge rating
        bypass_damage : int, optional
            Flag that indicates PCs can easily bypass damage resistances or immunities.
            Defaults to False
        ohko : bool, optional
            Flag to indicate the monster can one-round knockout one or more PCs
        """
        self.name = name
        self.cr = cr

        # Effective CR
        self.cr_eff = cr
        if bypass_damage:
            self.cr_eff -= 2
        if ohko:
            self.cr_eff += 4

    def power(self, tier):
        """
        Compute the monster power

        Parameters
        ----------
        tier : int
            Tier of play (1-4)

        Returns
        -------
        monster_power : int
            Power of monsters in the party
        """
        return MONSTER_POWER[f"tier{tier}"][self.cr_eff]


class MonsterParty():
    """Class for modeling a party of monsters"""

    def __init__(self):
        """
        Constructor for the monster party
        """
        self.monsters = []

    def add(self, monster, quantity=1):
        """Add monster to the party"""
        self.monsters.append((monster, quantity))

    def power(self, tier):
        """
        Compute the total party power

        Parameters
        ----------
        tier : int
            Tier of play (1-4)

        Returns
        -------
        monsters_power : int
            Total power of all monsters in the party
        """
        return sum([monster.power(tier) * quantity for monster, quantity in self.monsters])
