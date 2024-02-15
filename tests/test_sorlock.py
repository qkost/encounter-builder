"""

===============
test_sorlock.py
===============

Tests for sorlock tools

"""

import os

import unittest

from .context import ebuilder


class TestSorlock(unittest.TestCase):
    """
    Tests for Sorlock tools
    """
    def test_sorlock(self):
        """
        Test sorlock tables
        """
        state = ebuilder.SorlockState.from_level(12, sorcery_points=0)

        print("")
        print(ebuilder.sorlock_table_level(state))

        with self.assertRaises(RuntimeError):
            ebuilder.SorlockState.from_level(8, 3, 3)
        with self.assertRaises(RuntimeError):
            ebuilder.SorlockState.from_level(8, 2, 5)
        
        ebuilder.SorlockState(2, 3, [1, 1, 3, 5, 9], 5).spell_counts_by_level()

