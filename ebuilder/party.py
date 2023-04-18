"""

========
party.py
========

Tools for modeling the full party's power

"""

import json

import numpy as np

from .pc import PlayerCharacter


class Party():
    """
    Class to represent a 5e party
    """

    def __init__(self):
        """
        Constructor for the party
        """
        self.pcs = []

    @classmethod
    def from_json(cls, json_file):
        """Create a party from a JSON file"""
        with open(json_file, "r") as json_data:
            party_list = json.load(json_data)

        # Loop through each member in the party and add them in
        party = Party()
        for pc_dict in party_list:

            advantage = pc_dict.get("ADVANTAGE", None)
            pc_adv = False
            monster_adv = False
            monster_disadv = False
            if advantage:
                pc_adv = advantage.get("PC_ADVANTAGE", False)
                monster_adv = advantage.get("MONSTER_ADVANTAGE", False)
                monster_disadv = advantage.get("MONSTER_DISADVANTAGE", False)

            pc = PlayerCharacter(
                pc_dict["NAME"],
                pc_dict["LEVELS"],
                pc_dict["ITEMS"],
                pc_dict.get("ADVANTAGE", {})
            )
            party.add(pc)

        return party

    def add(self, pc):
        """Add player character to the party"""
        self.pcs.append(pc)

    def count(self):
        return len(self.pcs)

    def power(self):
        """Compute the total party power"""
        return sum([pc.power() for pc in self.pcs])

    def level(self):
        """Compute the average level of the party"""
        return np.average([pc.level for pc in self.pcs])

    def tier(self):
        """Compute the party's tier"""
        level = self.level()
        if level <= 4:
            return 1
        elif level <= 10:
            return 2
        elif level <= 16:
            return 3
        elif level <= 20:
            return 4

        raise ValueError(f"Invalid party level: {level}")
