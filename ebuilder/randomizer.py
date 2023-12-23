"""

=============
randomizer.py
=============

Tools for randomizing loot

"""

import os

import pandas as pd

import numpy as np

import xmltodict


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

COMPENDIUM_FILE = os.path.join(
    DATA_DIR,
    "220241_Official_Only.xml"
)


class Randomizer():
    """Class for randomizing the compendium."""

    def __init__(self):
        """
        Constructor for randomizer
        """
        # Initialize an empty compendium (only loaded if needed)
        self.compendium = None

        # Initialize empty compendium dataframes
        self.compendium_dfs = {}

    def csv_filename(self, category):
        """Get the filename for a CSV for a given category."""
        return os.path.join(DATA_DIR, f"compendium_{category}.csv")

    
    def create_csv(self, category):
        """
        Create a CSV file for a given category

        Parameters
        ----------
        category : str
            Category of compendium
        """

        if self.compendium is None:
            with open(COMPENDIUM_FILE, "rb") as fd:
                self.compendium = xmltodict.parse(fd.read())['compendium']

        # Get all the common keys for this category
        keys = list(set().union(*[list(item.keys()) for item in self.compendium[category]]))
        entries = [{key: item.get(key, None) for key in keys} for item in self.compendium[category]]
        df = pd.DataFrame(entries)

        # Add any special categories
        if category == "item":
            df["rarity"] = None
            magic = pd.notnull(df["magic"]) & pd.notnull(df["detail"])
            
            df.loc[magic, "rarity"] = (
                df.loc[magic, "detail"].str.split(" ")
                .apply(lambda x: "".join(filter(str.isalnum, next(iter(x), "").lower())))
            )

        df.to_csv(self.csv_filename(category), index=False)

    def get_compendium(self, category):
        """
        Get the proper compendium CSV

        Parameters
        ----------
        category : str
            Category of compendium
        
        Returns
        -------
        compendium : pandas.DataFrame
            Corresponding compendium
        """

        if category not in self.compendium_dfs.keys():
            self.compendium_dfs["category"] = pd.read_csv(self.csv_filename(category))
        return self.compendium_dfs["category"]
    
    def random_item(self, category, rarities=None, num=1):
        """
        Get a random item

        Parameters
        ----------
        category : str
            Category of compendium
        rarities : list, optional
            List of rarities to filter by
        num : int
            Number of random items. Defaults to 1

        Returns
        -------
        items : pandas.DataFrame
            Random items
        """
        df = self.get_compendium(category)

        # filter by rarities
        filtered = df
        if rarities is not None:
            filtered = filtered[filtered["rarity"].isin(rarities)].reset_index(drop=True)

        
        return filtered.loc[np.random.randint(1, len(filtered)+1, num)].reset_index(drop=True)
