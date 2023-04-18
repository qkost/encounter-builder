"""

=====
pc.py
=====

Tools for modeling the player character's power

"""

import os

import json

import pandas as pd


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

PRI_LEVEL_POINTS = pd.read_csv(os.path.join(
    DATA_DIR,
    "pc_primary_level_points.csv"
)).set_index("level").to_dict()["level_points"]

AUX_LEVEL_POINTS = pd.read_csv(os.path.join(
    DATA_DIR,
    "pc_aux_level_points.csv"
)).set_index("level").to_dict()["level_points"]

ITEM_BONUSES = pd.read_csv(os.path.join(
    DATA_DIR,
    "item_bonuses.csv"
)).set_index("items").to_dict()["level_points"]

POWER = pd.read_csv(os.path.join(
    DATA_DIR,
    "pc_power.csv"
)).set_index("level_points").to_dict()["power"]


with open(os.path.join(DATA_DIR, "class_categories.json"), "r") as CATEGORIES:
    CLASS_CATEGORIES = json.load(CATEGORIES)
"""
Load in relevant data.
"""


class PlayerCharacter():
    """
    Class to represent a player character's power
    """

    def __init__(
        self,
        name,
        levels,
        items,
        pc_adv=False,
        monster_adv=False,
        monster_disadv=False
    ):
        """
        Constructor for player character

        Parameters
        ----------
        name : str
        levels : dict
            Class names and number of levels in each class
        items : dict
            Dictionary of items and their corresponding numerical bonuses
        pc_adv : bool, optional
            Flag to indicate if this player character will have advantage on all
            attacks. Defaults to False
        monster_adv : bool, optional
            Flag to indicate if the monster will have advantage against this PC on all
            attacks. Defaults to False
        monster_disadv : bool, optional
            Flag to indicate if the monster will have disadvantage against this PC on
            all attacks. Defaults to False
        """
        self.name = name
        self.primary_levels, self.aux_levels, self.junk_levels = self.extract_levels(
            levels
        )
        self.level = self.primary_levels + self.aux_levels + self.junk_levels
        self.items = items
        self.advantages = {
            "PC_ADVANTAGE": pc_adv,
            "MONSTER_ADVANTAGE": monster_adv,
            "MONSTER_DISADVANTAGE": monster_disadv
        }

    @staticmethod
    def extract_levels(levels):
        """
        Extract levels into primary, auxiliary, and junk levels

        Parameters
        ----------
        levels : dict
            Class names and number of levels in each class

        Returns
        -------
        primary_levels : int
            Number of primary levels
        aux_levels : int
            Number of auxiliary levels
        junk_levels : int
            Number of junk levels

        Raises
        ------
        ValueError if unexpected class name is used
        """

        # Get primary class category
        primary_class = max(levels, key=levels.get)
        primary_category = CLASS_CATEGORIES[primary_class.upper()]
        primary_level = levels[primary_class]

        # Get all scores by category
        caster_levels = 0
        martial_levels = 0
        half_levels = 0
        for class_name, num_levels in levels.items():
            if CLASS_CATEGORIES[class_name] == "CASTER":
                caster_levels += levels[class_name]
            elif CLASS_CATEGORIES[class_name] == "MARTIAL":
                martial_levels += levels[class_name]
            elif CLASS_CATEGORIES[class_name] == "HALF-CASTER":
                half_levels += levels[class_name]
            else:
                raise ValueError(
                    f"Unexpected class category: {CLASS_CATEGORIES[class_name]}"
                )

        if primary_category == "CASTER":
            return (
                primary_level,
                half_levels,
                caster_levels - primary_level + martial_levels
            )
        elif primary_category == "MARTIAL":
            return (
                primary_level,
                martial_levels - primary_level + half_levels,
                caster_levels
            )
        else:
            return (
                primary_level,
                caster_levels + martial_levels + half_levels - primary_level,
                0
            )

    def primary_level_points(self):
        """
        Compute primary level points for this character

        Returns
        -------
        primary_level_points : int
            Number of points from primary level of character
        """
        return PRI_LEVEL_POINTS[self.primary_levels]

    def aux_level_points(self):
        """
        Compute aux level points for this character

        Returns
        -------
        aux_level_points : int
            Number of points from aux levels of character
        """
        return AUX_LEVEL_POINTS[self.aux_levels]

    def junk_level_points(self):
        """
        Compute junk level points for this character

        Returns
        -------
        junk_level_points : int
            Number of points from junk levels of character
        """
        return self.junk_levels

    def class_level_points(self):
        """
        Compute total level points

        Returns
        -------
        level_points : int
            Total level points for this character
        """
        return (
            self.primary_level_points()
            + self.aux_level_points()
            + self.junk_level_points()
        )

    def item_bonuses(self):
        """
        Compute the item bonuses

        Returns
        -------
        item_bonuses : int
            Total item bonuses for this character
        """
        item_total = sum(self.items.values())
        return ITEM_BONUSES[item_total]

    def other_bonuses(self):
        """
        Compute the other bonuses (from advantages and disadvantages)

        Returns
        -------
        other_bonuses : int
            Total other bonuses for this character
        """

        other_bonuses = 0

        if self.advantages["PC_ADVANTAGE"] and not self.advantages["MONSTER_ADVANTAGE"]:
            other_bonuses += 2
        if self.advantages["MONSTER_DISADVANTAGE"]:
            other_bonuses += 3

        return other_bonuses

    def total_level_points(self):
        """
        Compute total level points

        Returns
        -------
        level_points : int
            Total player character level points
        """
        return self.class_level_points() + self.item_bonuses() + self.other_bonuses()

    def power(self):
        """
        Compute total power level

        Returns
        -------
        power : int
            Total player character power level
        """
        return POWER[self.total_level_points()]
