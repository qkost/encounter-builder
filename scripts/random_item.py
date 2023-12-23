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
    "--category",
    "-c",
    type=str,
    help="Category of item.",
    choices=[
        "background",
        "class",
        "feat",
        "item",
        "monster",
        "race",
        "spell"
    ],
    default="item"
)

ARG_PARSER.add_argument(
    "--num",
    "-n",
    type=int,
    help="Number of items to generate.",
    default=1
)

ARG_PARSER.add_argument(
    "--rarity",
    "-r",
    type=str,
    choices=["common", "uncommon", "rare", "very", "legendary", "artifact", "varies"],
    help="Rarities to filter by. Defaults to None.",
    default=None,
    nargs="*"
)

ARG_PARSER.add_argument(
    "--type",
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

class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split("=")
            getattr(namespace, self.dest)[key] = [value]

ARG_PARSER.add_argument(
    "--filters",
    "-f",
    nargs="*",
    action=ParseKwargs,
    help="Arbitrary filters for items. Provide optional arguments like 'filter=value'.",
)


if __name__ == "__main__":
    args = ARG_PARSER.parse_args()

    kwargs = vars(args)
    additional_kwargs = kwargs.pop("kwargs")
    if additional_kwargs is not None:
        for k, v in additional_kwargs.items():
            kwargs[k] = v
    results = ebuilder.Randomizer().random_item(
        **kwargs
    ).dropna(axis=1)
    print(results)

    if args.output_file:
        if args.output_file.endswith(".csv"):
            results.to_csv(args.output_file, index=False)
        elif args.output_file.endswith(".json"):
            results.to_json(args.output_file, orient="records", lines=True)
