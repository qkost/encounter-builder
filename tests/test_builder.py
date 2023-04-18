"""

===============
test_builder.py
===============

Tests for encounter builder

"""

import os

import json

import unittest

from .context import ebuilder


class TestEBuilder(unittest.TestCase):
    """
    Tests for Encounter Builder
    """

    def setUp(self):
        """
        Common setup for all tests
        """
        self.input_dir = os.path.join(os.path.dirname(__file__), "inputs")

    def test_player_character(self):
        """
        Test computation of player character
        """

        # Items are used in common
        items = {
            "ARMOR_ABOVE_START": 3,
            "SHIELD_ABOVE_START": 2,
            "MAGIC_ITEM_ATTACK": 1,
            "MAGIC_ITEM_SAVE_DC": 2,
            "MAGIC_ITEM_SAVING_THROWS": 2
        }

        # Primary caster
        pc = ebuilder.PlayerCharacter(
            "TMP",
            {
                "DRUID": 6,
                "CLERIC": 1,
                "PALADIN": 2,
                "FIGHTER": 3
            },
            items,
            pc_adv=True
        )
        self.assertEqual(pc.primary_levels, 6)
        self.assertEqual(pc.aux_levels, 2)
        self.assertEqual(pc.junk_levels, 4)
        self.assertEqual(pc.primary_level_points(), 20)
        self.assertEqual(pc.aux_level_points(), 4)
        self.assertEqual(pc.junk_level_points(), 4)
        self.assertEqual(pc.class_level_points(), 28)
        self.assertEqual(pc.item_bonuses(), 5)
        self.assertEqual(pc.other_bonuses(), 2)
        self.assertEqual(pc.total_level_points(), 35)
        self.assertEqual(pc.power(), 117)

        # Primary martial
        pc = ebuilder.PlayerCharacter(
            "TMP",
            {
                "ROGUE": 7,
                "CLERIC": 1,
                "PALADIN": 2,
                "FIGHTER": 3
            },
            items,
            monster_disadv=True
        )
        self.assertEqual(pc.primary_levels, 7)
        self.assertEqual(pc.aux_levels, 5)
        self.assertEqual(pc.junk_levels, 1)
        self.assertEqual(pc.primary_level_points(), 22)
        self.assertEqual(pc.aux_level_points(), 9)
        self.assertEqual(pc.junk_level_points(), 1)
        self.assertEqual(pc.class_level_points(), 32)
        self.assertEqual(pc.item_bonuses(), 5)
        self.assertEqual(pc.other_bonuses(), 3)
        self.assertEqual(pc.total_level_points(), 40)
        self.assertEqual(pc.power(), 165)

        # Half-caster
        pc = ebuilder.PlayerCharacter(
            "TMP",
            {
                "RANGER": 11,
                "CLERIC": 1,
                "PALADIN": 2,
                "FIGHTER": 3
            },
            items,
            pc_adv=True,
            monster_adv=True
        )
        self.assertEqual(pc.primary_levels, 11)
        self.assertEqual(pc.aux_levels, 6)
        self.assertEqual(pc.junk_levels, 0)
        self.assertEqual(pc.primary_level_points(), 28)
        self.assertEqual(pc.aux_level_points(), 10)
        self.assertEqual(pc.junk_level_points(), 0)
        self.assertEqual(pc.class_level_points(), 38)
        self.assertEqual(pc.item_bonuses(), 5)
        self.assertEqual(pc.other_bonuses(), 0)
        self.assertEqual(pc.total_level_points(), 43)
        self.assertEqual(pc.power(), 202)
