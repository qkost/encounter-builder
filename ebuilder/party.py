"""

========
party.py
========

Tools for modeling the full party's power

"""


import numpy as np


class Party():
    """
    Class to represent a 5e party
    """

    def __init__(self):
        """
        Constructor for the party
        """
        self.pcs = []

    def add(self, pc):
        """Add player character to the party"""
        self.pcs.append(pc)

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
