"""

=======
main.py
=======

Main script for running encounters

"""


from .encounter import AdventuringDay, Encounter
from .monsters import MonsterParty
from .party import Party


def main(party_json, monster_jsons, charge_consumables=None, onetime_consumables=None):
    """
    Main script for encounter builing

    Parameters
    ----------
    party_json : str
        Path to party JSON file
    monster_jsons : list of str
        List of files for monster party JSON files
    charge_consumables : list of str, optional
        List of rarities (UNCOMMON, RARE, VERYRARE, LEGENDARY) of consumable magic items
        that have charges per day
    onetime_consumables : list of str, optional
        List of rarities (UNCOMMON, RARE, VERYRARE, LEGENDARY) of consumable magic items
        that are one-time use only
    """

    # Build party
    party = Party.from_json(party_json)

    # Build adventuring day
    adventuring_day = AdventuringDay(party)
    for monster_json in monster_jsons:
        monster_party = MonsterParty.from_json(monster_json)
        adventuring_day.add(Encounter(party, monster_party))

    # Add consumables
    if charge_consumables is not None:
        for consumable in charge_consumables:
            adventuring_day.add_consumable(consumable, "CHARGE")
    if onetime_consumables is not None:
        for consumable in onetime_consumables:
            adventuring_day.add_consumable(consumable, "CONSUMABLE")
