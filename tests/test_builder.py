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

        # Primary caster
        pc = ebuilder.PlayerCharacter(
            "TMP",
            {
                "DRUID": 6,
                "CLERIC": 1,
                "PALADIN": 2,
                "FIGHTER": 3
            }
        )
        self.assertEqual(pc.primary_levels, 6)
        self.assertEqual(pc.aux_levels, 2)
        self.assertEqual(pc.junk_levels, 4)
        self.assertEqual(pc.primary_level_points(), 20)
        self.assertEqual(pc.aux_level_points(), 4)
        self.assertEqual(pc.junk_level_points(), 4)
        self.assertEqual(pc.level_points(), 28)

        # Primary martial
        pc = ebuilder.PlayerCharacter(
            "TMP",
            {
                "ROGUE": 7,
                "CLERIC": 1,
                "PALADIN": 2,
                "FIGHTER": 3
            }
        )
        self.assertEqual(pc.primary_levels, 7)
        self.assertEqual(pc.aux_levels, 5)
        self.assertEqual(pc.junk_levels, 1)
        self.assertEqual(pc.primary_level_points(), 22)
        self.assertEqual(pc.aux_level_points(), 9)
        self.assertEqual(pc.junk_level_points(), 1)
        self.assertEqual(pc.level_points(), 32)

        # Half-caster
        pc = ebuilder.PlayerCharacter(
            "TMP",
            {
                "RANGER": 11,
                "CLERIC": 1,
                "PALADIN": 2,
                "FIGHTER": 3
            }
        )
        self.assertEqual(pc.primary_levels, 11)
        self.assertEqual(pc.aux_levels, 6)
        self.assertEqual(pc.junk_levels, 0)
        self.assertEqual(pc.primary_level_points(), 28)
        self.assertEqual(pc.aux_level_points(), 10)
        self.assertEqual(pc.junk_level_points(), 0)
        self.assertEqual(pc.level_points(), 38)
