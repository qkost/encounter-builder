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


class TestRandomizer(unittest.TestCase):
    """
    Tests for Randomizer
    """

    def setUp(self):
        """
        Common setup for all tests
        """
        self.input_dir = os.path.join(os.path.dirname(__file__), "inputs")

    def test_create_csvs(self):
        """Test loading and parsing of XML file"""
        rand = ebuilder.Randomizer()
        categories = ["item", "race", "class", "feat", "background", "spell", "monster"]
        for category in categories:
            rand.create_csv(category)
    
    def test_random(self):
        """Test generating a random item"""
        rand = ebuilder.Randomizer()
        rand.random_item("item", rarity=["rare", "very"])
        rand.random_item("item", rarity=["rare", "very"], type=["wand"])
        rand.random_item("spell", level=["1"])

