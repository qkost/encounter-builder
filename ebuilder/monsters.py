"""

===========
monsters.py
===========

Tools for modeling the monster's power

"""


import os

import json

import pandas as pd

from .randomizer import Randomizer

MONSTERS = Randomizer().get_compendium("monster").set_index("name")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

MONSTER_POWER = pd.read_csv(os.path.join(
    DATA_DIR,
    "monster_power.csv"
)).set_index("cr")

XP_BY_CR = pd.read_csv(os.path.join(
    DATA_DIR,
    "xp_by_cr.csv"
)).set_index("cr")
XP_BY_CR.index = XP_BY_CR.index.astype(str)

def cr_num_to_str(cr_num):
    """
    Convert numerical CR to string

    Parameters
    ----------
    cr_num : int

    Returns
    -------
    cr_str : str
    """
    if (cr_num == 0) or (cr_num >= 1):
        return f"{cr_num:.0f}"
    return f"1/{int(1 / cr_num)}"

def cr_str_to_num(cr_str):
    """
    Convert string CR to numerical

    Parameters
    ----------
    cr_str : str

    Returns
    -------
    cr_num : int
    """

    if "/" in cr_str:
        num, den = cr_str.split("/")
        cr = float(num) / float(den)
    else:
        cr = int(cr_str)
    return cr


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

    def xp(self):
        """
        Compute the monster xp
        """
        return XP_BY_CR.loc[cr_num_to_str(self.cr), "xp"]

    def __str__(self):
        return (
            f"{self.name}, "
            + f"CR {self.cr} ({self.cr_eff} eff.)"
        )

    @staticmethod
    def from_name(name):
        """Create a Monster from the Name"""
        monster = MONSTERS.loc[name]

        cr = monster["cr"]
        cr = cr_str_to_num(cr)

        return Monster(name, cr)

class MonsterParty():
    """Class for modeling a party of monsters"""

    def __init__(self):
        """
        Constructor for the monster party
        """
        self.monsters = []

    @staticmethod
    def from_json(json_file):
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

    @staticmethod
    def from_names(names):
        """Create a monster party from a list of monster names"""
        party = MonsterParty()
        for name in names:
            party.add(Monster.from_name(name))
        return party

    def add(self, monster, quantity=1):
        """Add monster to the party"""
        self.monsters.append((monster, quantity))

    def count(self):
        return len(self.monsters)

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

    def xp(self):
        """
        Calculate the total XP for the monster party

        Returns
        -------
        xp : int
            Total xp from all the monsters
        """
        return sum([quantity * monster.xp() for monster, quantity in self.monsters])

    def __str__(self):
        return (
            f"Monsters: {self.count()}\n"
            + "\n".join([
                f"{monster[1]} x " + monster[0].__str__()
                for monster in self.monsters
            ])
        )
