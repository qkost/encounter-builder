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

COMPENDIUM_FILES = [
    os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".xml")
]

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
    "W": "wonderous",
    "WD": "wand"
}

TYPE_MAP_REVERSED = {v: k for k, v in TYPE_MAP.items()}

SOURCEBOOKS_OWNED = [
    "Bigby Presents: Glory of the Giants",
    "Dungeon Master's Guide",
    "Dungeon Master's Guide 2024",
    "Explorer's Guide to Wildemount",
    "Fizban's Treasury of Dragons",
    "Ghosts of Saltmarsh",
    "Lost Mines of Phandelver"
    "Monster Manual",
    "Monster Manual,",
    "Monster Manual 2024",
    "Mordenkainen Presents: Monsters of the Multiverse",
    "Phandelver and Below: The Shattered Obelisk",
    "Player's Handbook",
    "Player's Handbook 2024",
    "Tasha's Cauldron of Everything",
    "The Book of Many Things",
    "The Wild Beyond the Witchlight",
    "Xanathar's Guide to Everything",
    "Xanathar's Guide to Everything,"
]


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

        Returns
        -------
        df : pandas.DataFrame
            Data frame with the compendium loaded
        """

        if self.compendium is None:
            self.compendium = {}
            for compentium_file in COMPENDIUM_FILES:
                with open(compentium_file, "rb") as fd:
                    compendium = xmltodict.parse(fd.read())['compendium']
                    for key, value in compendium.items():
                        if key in self.compendium:
                            if isinstance(self.compendium[key], str):
                                pass
                            elif isinstance(self.compendium[key], list):
                                self.compendium[key].extend(compendium[key])
                            else:
                                raise RuntimeError(
                                    f"Unexpected compendium type: {type(self.compendium[key])}"
                                )
                        else:
                            self.compendium[key] = compendium[key]

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
        
        # Add sources
        has_source = True
        if category in ["monster"]:
            # Add monster sources
            sources = []
            for irow, row in df.iterrows():
                if row["description"] is None:
                    row["description"] = ""
                if "Source" in row["description"]:
                    # 2024 monster manual has the Source in description
                    sources.append(row["description"].split("\t")[-1])
                elif isinstance(row["trait"], dict):
                    sources.append(row["trait"]["text"])
                else:
                    entry = row["trait"][0]["text"]
                    if isinstance(entry, list):
                        sources.append(entry[-1])
                    else:
                        sources.append(entry)
            df["source"] = sources
        elif "text" in df.columns:#"text" in df.columns:
            # All other sources are in a similar spot
            sources = []
            for irow, row in df.iterrows():
                if row["text"] is None:
                    sources.append(None)
                else:
                    sources.append(row["text"][-1])
            df["source"] = sources
        else:
            has_source = False

        # Remove page number
        df["book"] = "None"
        if has_source:
            books = []
            for _source in df["source"]:
                if _source is not None:
                    books.append(_source.split(" p.")[0])
                else:
                    books.append("None")
            df["book"] = books
        df["book"] = df["book"].str.replace("Source: ", "")
        df["owned"] = df["book"].apply(lambda x: x in SOURCEBOOKS_OWNED).astype(str)

        df.to_csv(self.csv_filename(category), index=False)

        return df

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
            df = pd.read_csv(self.csv_filename(category))
        
        # Convert numeric columns to be ints
        for col in df:
            if pd.api.types.is_numeric_dtype(df[col].dtype):
                try:
                    df[col] = df[col].astype(pd.Int64Dtype())
                except TypeError:
                    pass
        
        self.compendium_dfs["category"] = df
        return df
    
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
            # The types of items are non-intuitive abbreviations
            # Map them to something more sensible for humans to remember
            types = kwargs.pop("type")
            types_r = [TYPE_MAP_REVERSED[type] for type in types]
            filtered = filtered[filtered["type"].isin(types_r)].reset_index(drop=True)

        if (category == "spell") and (kwargs.get("classes", None) is not None):
            # Classes appear as a string of class names separated by columns
            # Just check if any of the class names are a subset of the string
            classes = kwargs.pop("classes")
            has_any = []
            for _class in classes:
                lowered = filtered["classes"].str.lower()
                has_class = lowered.str.contains(classes[0].lower())
                has_any.append(has_class.to_numpy())
            has_any = np.array(has_any).sum(axis=0).astype(bool)
            filtered = filtered[has_any].reset_index(drop=True)

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
        
        # Return random values
        rng = np.random.default_rng()
        numbers = rng.choice(len(filtered), size=num, replace=False)
        return filtered.loc[numbers].reset_index(drop=True)
