"""

========
party.py
========

Tools for modeling the full party's power

"""


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
