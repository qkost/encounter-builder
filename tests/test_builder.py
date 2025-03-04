"""

===============
test_builder.py
===============

Tests for encounter builder

"""

import os

import json

import numpy as np

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
        # Create party
        party = ebuilder.Party()

        # Items are used in common
        items = {
            "ARMOR_ABOVE_START": 3,
            "SHIELD_ABOVE_START": 2,
            "MAGIC_ITEM_ATTACK": 1,
            "MAGIC_ITEM_SAVE_DC": 2,
            "MAGIC_ITEM_SAVING_THROWS": 2
        }

        # Primary caster
        advantages = {
            "PC_ADVANTAGE": True,
            "MONSTER_ADVANTAGE": False,
            "MONSTER_DISADVANTAGE": False
        }
        pc = ebuilder.PlayerCharacter(
            "TMP",
            {
                "DRUID": 6,
                "CLERIC": 1,
                "PALADIN": 2,
                "FIGHTER": 3
            },
            items,
            advantages
        )
        party.add(pc)
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
        advantages = {
            "PC_ADVANTAGE": False,
            "MONSTER_ADVANTAGE": False,
            "MONSTER_DISADVANTAGE": True
        }
        pc = ebuilder.PlayerCharacter(
            "TMP",
            {
                "ROGUE": 7,
                "CLERIC": 1,
                "PALADIN": 2,
                "FIGHTER": 3
            },
            items,
            advantages
        )
        party.add(pc)
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
        advantages = {
            "PC_ADVANTAGE": True,
            "MONSTER_ADVANTAGE": True,
            "MONSTER_DISADVANTAGE": False
        }
        pc = ebuilder.PlayerCharacter(
            "TMP",
            {
                "RANGER": 11,
                "CLERIC": 1,
                "PALADIN": 2,
                "FIGHTER": 3
            },
            items,
            advantages
        )
        party.add(pc)
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

        # Check total party stats
        self.assertEqual(party.power(), 117 + 165 + 202)
        self.assertEqual(party.level(), (12 + 13 + 17) / 3)
        self.assertEqual(party.tier(), 3)

    def test_monsters(self):
        """
        Test monster calculations
        """

        tier = 3
        monster_party = ebuilder.MonsterParty()

        monster = ebuilder.Monster(
            "YOUNG_GREEN_DRAGON",
            8,
            bypass_resistance=True,
            ohko=True
        )
        monster_party.add(monster)
        self.assertEqual(monster.power(tier), 75)

        monster = ebuilder.Monster("GUARD_DRAKE", 2)
        monster_party.add(monster, 2)
        self.assertEqual(monster.power(tier), 19)

        self.assertEqual(monster_party.power(tier), 75 + 19*2)

    def test_monsters_from_names(self):
        """Test creation of monster party from names"""
        monster_party = ebuilder.MonsterParty.from_names([
            "Vampire", "Vampire [2024]"
        ])

    def test_json(self):
        """Test creating encounters from JSON file"""

        # Create party from JSON
        party = ebuilder.Party.from_json(
            os.path.join(self.input_dir, "test_party.json")
        )
        self.assertEqual(party.level(), 6)
        self.assertEqual(party.power(), 45 + 51 * 3)

        # Create monster party from JSON
        monster_party = ebuilder.MonsterParty.from_json(
            os.path.join(self.input_dir, "test_monsters.json")
        )
        self.assertEqual(monster_party.power(party.tier()), 95 + 23*2)

    def test_encounter(self):
        """Test encounter"""
        party = ebuilder.Party.from_json(
            os.path.join(self.input_dir, "test_party.json")
        )
        monster_party = ebuilder.MonsterParty.from_json(
            os.path.join(self.input_dir, "test_monsters.json")
        )

        encounter = ebuilder.Encounter(party, monster_party)
        encounter.difficulty()

        adventuring_day = ebuilder.AdventuringDay(party)
        adventuring_day.add(encounter)
        adventuring_day.add(encounter)

        adventuring_day.add_consumable("RARE", "CHARGE")
        adventuring_day.add_consumable("VERYRARE", "CONSUMABLE")

        adventuring_day.fatigue()

    def test_main_json(self):
        """Test main function of encounter builder"""
        print("\n\n\n")
        ebuilder.main(
            os.path.join(self.input_dir, "test_party.json"),
            [os.path.join(self.input_dir, "test_monsters.json")] * 2
        )

        print("\n\n\n")
        ebuilder.main(
            os.path.join(self.input_dir, "test_party.json"),
            [os.path.join(self.input_dir, "test_monsters.json")] * 2,
            ["RARE"],
            ["VERYRARE"]
        )

    def test_main_monster_names(self):
        """Test main funciton by passing monster names instead of JSON"""
        monsters = ["Vampire [2024]", "15", 15, 1/4, "1/4"]

        ebuilder.main(
            os.path.join(self.input_dir, "test_party.json"),
            monsters,
            ["RARE"],
            ["VERYRARE"]
        )

    def test_encounter_2024(self):
        """
        Test 2024 encounter building rules
        """
        party = ebuilder.Party.from_json(
            os.path.join(self.input_dir, "test_party.json")
        )
        monster_party = ebuilder.MonsterParty.from_json(
            os.path.join(self.input_dir, "test_monsters.json")
        )

        encounter = ebuilder.Encounter(party, monster_party)
        encounter.difficulty(method="2024")

    def test_cr_num_str_conversion(self):
        crs = np.concatenate([
            [0, 0.125, 0.25, 0.5],
            np.arange(1, 30.1, 1)
        ])

        for cr in crs:
            self.assertEqual(
                cr,
                ebuilder.cr_str_to_num(ebuilder.cr_num_to_str(cr))
            )