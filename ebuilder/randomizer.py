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

TYPE_MAP = {
    "$": "monetary",
    "A": "ammo",
    "G": "gear",
    "HA": "heavy_armor",
    "LA": "light_armor",
    "M": "melee",
    "MA": "medium_armor",
    "R": "ranged",
    "S": "shield",
    "P": "potion",
    "RD": "rod",
    "RG": "ring",
    "SC": "scroll",
    "ST": "staff",
    "W": "wonderous_item",
    "WD": "wand"
}

TYPE_MAP_REVERSED = {v: k for k, v in TYPE_MAP.items()}


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
    
    def random_item(self, category, num=1, **kwargs):
        """
        Get a random item

        Parameters
        ----------
        category : str
            Category of compendium
        rarities : list, optional
            List of rarities to filter by
        rarities : list, optional
            List of types to filter by
        num : int
            Number of random items. Defaults to 1

        Returns
        -------
        items : pandas.DataFrame
            Random items
        """
        df = self.get_compendium(category)


        # Filter special cases
        filtered = df
        if (category == "item") and (kwargs.get("type", None) is not None):
            types = kwargs.pop(type)
            types_r = [TYPE_MAP_REVERSED[type] for type in types]
            filtered = filtered[filtered["type"].isin(types_r)].reset_index(drop=True)

        # Filter non-special cases
        for key, values in kwargs.items():
            # If no value is provided, continue
            if values is None:
                continue
    
            # Let the user know if they provided a bad key
            if key not in filtered.columns:
                raise KeyError(
                    f"Requested filter {key} not in available columns: "
                    f"{list(filtered.columns)}"
                )

            # Match data types
            filtered = (
                filtered[filtered[key].astype(type(values[0])).isin(values)]
                .reset_index(drop=True)
            )

        if filtered.empty:
            raise RuntimeError("No remaining items after filtering.")
        return filtered.loc[np.random.randint(1, len(filtered)+1, num)].reset_index(drop=True)
