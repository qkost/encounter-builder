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

ENCOUNTER_2024 = pd.read_csv(os.path.join(
    DATA_DIR,
    "encounter_difficulty_2024.csv"
))

with open(os.path.join(DATA_DIR, "encounter_difficulty_descriptions_2024.json"), "r") as ediff_file:
    ENCOUNTER_DESC_2024  = json.load(ediff_file)

FATIGUE = pd.read_csv(os.path.join(
    DATA_DIR,
    "fatigue.csv"
))


CONSUMABLES = pd.read_csv(os.path.join(
    DATA_DIR,
    "consumables.csv"
)).set_index("tier")


class Encounter():
    """Class for modeling encounter difficulty"""

    def __init__(self, party, monster_party, method="cr2"):
        """
        Constructor for encounter

        Parameters
        ----------
        party : ebuilder.Pary
            Player character party
        monster_party : ebuilder.MonsterParty
            Party of monsters
        method : str, optional
            Method for computing difficulty. Defaults to "cr2"
        """
        self.party = party
        self.monster_party = monster_party
        self.method = method

    def difficulty(self, method=None, **kwargs):
        """
        Compute the encounter difficulty using Challenge Rating 2.0

        Parameters
        ----------
        interpolate : bool, optional
            Flag to interpolate the encounter cost. Defaults to True
        method : str, optional
            Method for computing difficulty. Defaults to self.method

        Returns
        -------
        difficulty_category : str
            String label for difficulty category
        difficulty_description : str
            Description of difficulty
        cost : float
            Cost of encounter
        """
        if method is None:
            method = self.method

        if method == "cr2":
            return self.difficulty_cr2(**kwargs)
        elif method == "2024":
            return self.difficulty_2024()
        
        raise RuntimeError(f"Unexpected difficulty method: {method}")

    def difficulty_2024(self):
        """
        Compute the encounter difficulty using DMG 2024
        """
        xp = self.monster_party.xp()
        level = self.party.level()

        difficulties = ENCOUNTER_2024[ENCOUNTER_2024["party_level"] <= level].iloc[-1]

        # Get the last difficulty exceeded
        difficulty_labels = ["low", "moderate", "high"]
        above_threshold = [xp >= difficulties[col] for col in difficulty_labels]
        difficulty_category = difficulty_labels[
            len(above_threshold) - above_threshold[::-1].index(True) - 1
        ]

        return difficulty_category, ENCOUNTER_DESC_2024[difficulty_category], np.nan

    def difficulty_cr2(self, interpolate=True):
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

    def __str__(self):
        return (
            "Encounter\n"
            + "-" * 80 + "\n"
            + self.monster_party.__str__()
            + f"\nMonster power: {self.monster_party.power(self.party.tier())}"
            + f"\nDifficulty: {self.difficulty()}"
            + "\n"
        )


class AdventuringDay():
    """Class for modeling an adventuring day."""

    def __init__(self, party):
        """
        Constructor for the adventuring day

        Parameters
        ----------
        party : ebuilder.Pary
        """
        self.party = party
        self.encounters = []
        self.consumables = 0

    def add(self, encounter):
        """Add encounter to the party"""
        self.encounters.append(encounter)

    def add_consumable(self, rarity, consumable_category):
        """
        Add consumable categories to party

        Parameters
        ----------
        rarity : str
            Rarity category for consumable magic item. Must be UNCOMMON, RARE, VERYRARE,
            or LEGENDARY
        consumable_category : str
            Category of consumable. Must be CHARGE or CONSUMABLE
        """
        self.consumables += CONSUMABLES.loc[
            self.party.tier(),
            f"{rarity}_{consumable_category}"
        ]

    def fatigue(self):
        """Compute the fatigue level for the adventuring day."""

        costs = []
        for encounter in self.encounters:
            _, _, cost = encounter.difficulty()
            costs.append(cost)

        total_cost = sum(costs)

        # Subtract consumables
        consumable_savings = self.consumables / self.party.count()

        # Get the fatigue for the day
        fatigue = FATIGUE[
            (FATIGUE["cost"] + consumable_savings) <= total_cost
        ].iloc[-1]

        return fatigue["category"], fatigue["description"], total_cost

    def __str__(self):
        return (
            self.party.__str__()
            + "\n".join([encounter.__str__() for encounter in self.encounters])
            + "\nAdventuring Day\n"
            + "-" * 80 + "\n"
            + f"{self.fatigue()}"
        )
