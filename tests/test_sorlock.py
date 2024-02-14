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
        ebuilder.sorlock_table_level(8, 2, 3)

        with self.assertRaises(RuntimeError):
            ebuilder.sorlock_table_level(8, 3, 3)
        with self.assertRaises(RuntimeError):
            ebuilder.sorlock_table_level(8, 2, 5)



