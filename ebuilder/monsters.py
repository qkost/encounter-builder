"""

===========
monsters.py
===========

Tools for modeling the monster's power

"""


import os

import json

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

MONSTER_POWER = pd.read_csv(os.path.join(
    DATA_DIR,
    "monster_power.csv"
)).set_index("cr")


class Monster():
    """Class for modeling monster power"""

    def __init__(self, name, cr, bypass_resistance=False, ohko=False):
        """
        Constructor for monster

        Parameters
        ----------
        name : str
            Name of monster
        cr : int
            Monster challenge rating
        bypass_resistance : int, optional
            Flag that indicates PCs can easily bypass damage resistances or immunities.
            Defaults to False
        ohko : bool, optional
            Flag to indicate the monster can one-round knockout one or more PCs
        """
        self.name = name
        self.cr = cr

        # Effective CR
        self.cr_eff = cr
        if bypass_resistance:
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

    @classmethod
    def from_json(cls, json_file):
        """Create a monster party from a JSON file"""
        with open(json_file, "r") as json_data:
            monster_list = json.load(json_data)

        # Loop through each member in the party and add them in
        party = MonsterParty()
        for monster_dict in monster_list:
            monster = Monster(
                monster_dict["NAME"],
                monster_dict["CR"],
                monster_dict.get("BYPASS_RESISTANCE", False),
                monster_dict.get("OHKO", False)
            )
            party.add(monster, monster_dict["QUANTITY"])

        return party

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
