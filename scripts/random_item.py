"""

===============
random_item.py
===============

Generate random magic items

"""

import os
import sys

import json

import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))
import ebuilder


ARG_PARSER = argparse.ArgumentParser(
    description="Generate random magic items"
)

ARG_PARSER.add_argument(
    "--num",
    "-n",
    type=int,
    help="Number of items to generate.",
    default=1
)

ARG_PARSER.add_argument(
    "--rarities",
    "-r",
    type=str,
    choices=["common", "uncommon", "rare", "very", "legendary", "artifact", "varies"],
    help="Rarities to filter by. Defaults to None.",
    default=None,
    nargs="*"
)

ARG_PARSER.add_argument(
    "--types",
    "-t",
    type=str,
    choices=[
        "monetary",
        "ammo",
        "gear",
        "heavy_armor",
        "light_armor",
        "melee",
        "medium_armor",
        "ranged",
        "shield",
        "potion",
        "rod",
        "ring",
        "scroll",
        "staff",
        "wonderous",
        "wand"
    ],
    help="Item types to filter.",
    default=None,
    nargs="*"
)

ARG_PARSER.add_argument(
    "--output_file",
    "-o",
    type=str,
    help="Output file to save results.",
)


if __name__ == "__main__":
    ARGS = ARG_PARSER.parse_args()
    results = ebuilder.Randomizer().random_item(
        "item",
        rarities=ARGS.rarities,
        types=ARGS.types,
        num=ARGS.num
    ).dropna(axis=1)
    print(results)

    if ARGS.output_file:
        if ARGS.output_file.endswith(".csv"):
            results.to_csv(ARGS.output_file, index=False)
        elif ARGS.output_file.endswith(".json"):
            results.to_json(ARGS.output_file, orient="records", lines=True)
