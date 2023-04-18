"""

====================
encounter_builder.py
====================

Main script for encounter builder

"""

import os
import sys

import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))
import ebuilder


ARG_PARSER = argparse.ArgumentParser(
    description="Build encounters using CR2.0"
)

ARG_PARSER.add_argument(
    "encounters",
    type=str,
    help="Path to encounter JSON files",
    nargs="*"
)

ARG_PARSER.add_argument(
    "--party",
    type=str,
    help="Path to party JSON",
    default=os.path.join(os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "defaults",
        "party.json"
    ))
)

ARG_PARSER.add_argument(
    "--charge_consumables",
    "-c",
    help="Array of rarities of charge consumable items."
)

ARG_PARSER.add_argument(
    "--onetime_consumables",
    "-o",
    help="Array of rarities of one-time use consumable items."
)


if __name__ == "__main__":
    ARGS = ARG_PARSER.parse_args()
    if not ARGS.encounters:
        raise ValueError("At least one encounter required.")
    ebuilder.main(
        ARGS.party,
        ARGS.encounters,
        ARGS.charge_consumables,
        ARGS.onetime_consumables
    )
