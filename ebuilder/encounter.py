"""

============
encounter.py
============

Tools for ranking encounter difficulty

"""
import os

import json

import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

ENCOUNTER = pd.read_csv(os.path.join(
    DATA_DIR,
    "encounter_difficulty.csv"
))

FATIGUE = pd.read_csv(os.path.join(
    DATA_DIR,
    "fatigue.csv"
))


class Encounter():
    """Class for modeling encounter difficulty"""

    def __init__(self, party, monster_party):
        """
        Constructor for encounter

        Parameters
        ----------
        party : ebuilder.Pary
            Player character party
        monster_party : ebuilder.MonsterParty
            Party of monsters
        """
        self.party = party
        self.monster_party = monster_party

    def difficulty(self, interpolate=True):
        """
        Compute the encounter difficulty

        Parameters
        ----------
        interpolate : bool, optional
            Flag to interpolate the encounter cost. Defaults to True

        Returns
        -------
        difficulty_category : str
            String label for difficulty category
        difficulty_description : str
            Description of difficulty
        cost : float
            Cost of encounter
        """

        # Compute the power ratio
        power_ratio = (
            self.monster_party.power(self.party.tier())
            / self.party.power()
        )

        # Floor the table
        difficulty = ENCOUNTER[ENCOUNTER["multiplier"] <= power_ratio].iloc[-1]
        difficulty_category = difficulty["category"]
        difficulty_description = difficulty["description"]

        cost = difficulty["cost"]
        if interpolate:
            cost = np.interp(
                power_ratio, ENCOUNTER["multiplier"], ENCOUNTER["cost"]
            )

        return difficulty["category"], difficulty["description"], cost


class AdventuringDay():
    """Class for modeling an adventuring day."""

    def __init__(self):
        """
        Constructor for the adventuring day
        """
        self.encounters = []

    def add(self, encounter):
        """Add encounter to the party"""
        self.encounters.append(encounter)

    def fatigue(self):
        """Compute the fatigue level for the adventuring day."""

        costs = []
        for encounter in self.encounters:
            _, _, cost = encounter.difficulty()
            costs.append(cost)

        total_cost = sum(costs)

        # Subtract consumables
        # TODO

        # Get the fatigue for the day
        fatigue = FATIGUE[FATIGUE["cost"] <= total_cost].iloc[-1]

        return fatigue["category"], fatigue["description"], total_cost
