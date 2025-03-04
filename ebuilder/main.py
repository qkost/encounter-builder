"""

=======
main.py
=======

Main script for running encounters

"""

import os

from .encounter import AdventuringDay, Encounter
from .monsters import MonsterParty, Monster, cr_str_to_num
from .party import Party


def main(
        party_json,
        monsters,
        charge_consumables=None,
        onetime_consumables=None,
        difficulty_method="cr2"
    ):
    """
    Main script for encounter builing

    Parameters
    ----------
    party_json : str
        Path to party JSON file
    monster_jsond : list of str
        List of of monster names or list of monster party JSON files
    charge_consumables : list of str, optional
        List of rarities (UNCOMMON, RARE, VERYRARE, LEGENDARY) of consumable magic items
        that have charges per day
    onetime_consumables : list of str, optional
        List of rarities (UNCOMMON, RARE, VERYRARE, LEGENDARY) of consumable magic items
        that are one-time use only
    difficulty_method : str, optional
        Method for computing difficulty. Defaults to "cr2"
    """

    # Build party
    party = Party.from_json(party_json)

    # Build adventuring day
    adventuring_day = AdventuringDay(party)
    if os.path.isfile(monsters[0]):
        for monster_json in monsters:
            monster_party = MonsterParty.from_json(monster_json)
            adventuring_day.add(
                Encounter(party, monster_party, method=difficulty_method)
            )
    else:
        monster_party = MonsterParty()
        for name in monsters:
            if isinstance(name, int) or isinstance(name, float):
                monster_party.add(Monster.from_cr(name))
            elif name.isnumeric():
                monster_party.add(Monster.from_cr(cr_str_to_num(name)))
            else:
                try:
                    cr_str_to_num(name)
                    monster_party.add(Monster.from_cr(cr_str_to_num(name)))
                except ValueError:
                    monster_party.add(Monster.from_name(name))
        adventuring_day.add(Encounter(party, monster_party, method=difficulty_method))

    # Add consumables
    if charge_consumables is not None:
        for consumable in charge_consumables:
            adventuring_day.add_consumable(consumable, "CHARGE")
    if onetime_consumables is not None:
        for consumable in onetime_consumables:
            adventuring_day.add_consumable(consumable, "CONSUMABLE")

    # Print results
    print(adventuring_day)
