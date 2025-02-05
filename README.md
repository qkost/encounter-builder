# encounter-builder

Encounter builder is a tool to help DMs balance combat encounters in D&D 5e. This tool is entirely based on [CR2.0 by DragnaCarta](https://www.gmbinder.com/share/-N4m46K77hpMVnh7upYa). This tool specifically uses the *Part II. Advanced Guide* section of CR2.0.

## Running Encounter Builder

Encounter builder is a command-line Python tool where the user provides arguments corresponding to each encounter in an adventuring day as well as optional arguments for the party make up (if the party is not already located in the default location) and any consumable magic items the party has.

**Example:**

In the below example two encounters, `encounter1.json` and `encounter2.json`, are the challenges the party will face on the adventuring day. The party is described in the optional argument `party.json`; if not supplied it is assumed the party JSON file is located in the default location (described below). Additionally, a list of all consumbables that have daily charges as well as one time uses are supplied with the remaining optional arguments `--charge_consumables` and `--onetime_consumables`.

```bash
python scripts/encounter_builder.py /path/to/encounter1.json /path/to/encounter2.json --party /path/to/party.json --charge_consumables UNCOMMON COMMON --onetime_consumables RARE
```

Please use the `--help` argument for more information on the required and optional arguments.

**Example Output:**

The output is to the command line and indicates the computed party composition and power, monster composition and power for each encounter, and the fatigue level for the adventuring day.

```
Party
--------------------------------------------------------------------------------
Characters: 4
Croll, Level 6 (6, 0, 0), LP 21, Power 45
Flynt, Level 6 (6, 0, 0), LP 22, Power 48
Bevil, Level 6 (6, 0, 0), LP 22, Power 48
Thellen, Level 6 (6, 0, 0), LP 22, Power 48
Party power: 189

Encounter
--------------------------------------------------------------------------------
Monsters: 2
1 x PHASE_SPIDER, CR 3 (3 eff.)
5 x GIANT_WOLF_SPIDER, CR 0.25 (0.25 eff.)
Monster power: 60
Difficulty: ('Trivial', 'Probably not even worth doing.', 1.5873015873015872)

Encounter
--------------------------------------------------------------------------------
Monsters: 2
1 x YOUNG_GREEN_DRAGON, CR 8 (8 eff.)
2 x GUARD_DRAKE, CR 2 (2 eff.)
Monster power: 131
Difficulty: ('Bruising', 'The PCs will win with minor injuries.', 5.241622574955908)

Adventuring Day
--------------------------------------------------------------------------------
('Taxing', 'The PCs will use a large minority of their resources.', 6.828924162257495)
```

In the party section each character is represeted by their name, their number of levels (with the primary, auxiliary, and junk levels in parentheses), Level Points (LP), and PC power. The total party power is indicated after all party members are listed.

Each encounter is then listed with the total number of monsters and enumerations of each monster in the encounter. The monsters have their CR and effective CR indicated in line with their descriptions. After the monsters, the total monster power is indicated. The `Difficulty` line corresponds to the table in Step 3 of [CR2.0 by DragnaCarta](https://www.gmbinder.com/share/-N4m46K77hpMVnh7upYa) with the entries corresponding to the encounter difficulty category, description, and cost (note the cost is not rounded down to the table values).

Finally, the total fatigue level for the adventuring day is indicated at the bottom. This corresponds to the table in the "Building an Adventuring Day" section of [CR2.0 by DragnaCarta](https://www.gmbinder.com/share/-N4m46K77hpMVnh7upYa) with entries corresponding to the total adventuring day fatigue category, description, and total cost.

## Party File

The party file is a JSON file that describes the composition of the party, each Player Character's (PC) level makeup, magic items in possession of each PC, and any advantages/disadvantages the PC regularly has.

The JSON file is a list of dictionaries where each dictionary corresponds to a PC. The fields of the dictionary are:
* `NAME`: The name of the character
* `LEVELS`: A dictionary of levels in each class (keys are class values are the number of levels in that class)
* `ITEMS` (optional): Additional item bonuses for the character. This is a dictionary of items where the key is the name of the item (no actual rescriction on name, just for the user to keep track of where the bonus comes from) and the value is the bonus provided by that item. Please see Step 1d in [CR2.0 by DragnaCarta](https://www.gmbinder.com/share/-N4m46K77hpMVnh7upYa) for what to use for the item bonuses.
* `ADVANTAGE` (optional): Regular advantages/disadvantages this player has during combat. Please see Step 1E in [CR2.0 by DragnaCarta](https://www.gmbinder.com/share/-N4m46K77hpMVnh7upYa) for more information on these bonuses. The options are
    * `PC_ADVANTAGE`: If the PC will have advantage on all of their attacks
    * `MONSTER_ADVANTAGE`: All enemies will also have advantage on attacks against the PC
    * `MONSTER_DISADVANTAGE`: All enemies will have disadvantage to attack the PC

**Example:**

```json
[
    {
        "NAME": "PC1",
        "LEVELS": {
            "DRUID": 6
        }
    },
    {
        "NAME": "PC2",
        "LEVELS": {
            "ROGUE": 5,
            "FIGHTER": 1
        },
        "ITEMS": {
            "WEAPON+1": 1,
            "PLATE_ARMOR": 2
        },
        "ADVANTAGE": {
            "PC_ADVANTAGE": true,
            "MONSTER_ADVANTAGE": false,
            "MONSTER_DISADVANTAGE": true
        }
    }
]
```

## Monster Party File

A monster party file describes all of the monsters that participate in a single encounter. Each monster is represented by a dictionary with the following fields:
* `NAME`: The name of the creature (can be anything)
* `CR`: The challenge rating as indicated in the Monster Manual or other source book
* `QUANTITY`: The numbers of this monster type present in the encounter.
* `BYPASS_RESISTANCE` (optional): If all PCs can consistently bypass a resistance or immunity the creature posesses. See Step 4 in [CR2.0 by DragnaCarta](https://www.gmbinder.com/share/-N4m46K77hpMVnh7upYa) for more information.
* `OHKO` (optional): If the monster can kill or knock out one or more PCs in the first turn of combat. See Step 4 in [CR2.0 by DragnaCarta](https://www.gmbinder.com/share/-N4m46K77hpMVnh7upYa) for more information.


**Example:**

```json
[
    {
        "NAME": "YOUNG_GREEN_DRAGON",
        "CR": 8,
        "BYPASS_RESISTANCE": true,
        "OHKO": true,
        "QUANTITY": 1
    },
    {
        "NAME": "GUARD_DRAKE",
        "CR": 2,
        "QUANTITY": 2
    }
]
```

## Consumables

Consumables are expected to change more often so these are supplied as command-line arguments when calling `/scripts/encounter_builder.py` rather than as input files which are more time-consuming to set up. To add consumables to the party, use the optional arguments `--charge_consumables` and `--onetime_consumables` for consumables that have daily charges and one-time use consumables respectively.

After each of these arguments, the user can supply any number of items by enumerating a list of item rarities from the options:
* UNCOMMON
* COMMON
* RARE
* VERYRARE
* LEGENDARY

**Example:**
```bash
--charge_consumables UNCOMMON COMMON --onetime_consumables RARE LEGENDARY RARE RARE UNCOMMON
```

Please see the "Building and Advanturing Day" section of [CR2.0 by DragnaCarta](https://www.gmbinder.com/share/-N4m46K77hpMVnh7upYa) for information.

## Setting Up Defaults

If you are running a long campaign, it is recommended that you place your party in the default party file location `/defaults/party.json`.

It is not required to do this, you can provide the party file as a command-line argument when calling `/scripts/encounter_builder.py`.

## Running Randomizer

Running the randomizer is a single command-line function. The `--filter` or `-f` argument allows arbitrary filtering of the compendium for any common tag.

Examples below:

```bash
python scripts/random_item.py -c spell -n 3 -f level=3

python scripts/random_item.py -c item -n 1 -f rarity=legendary

python .\scripts\random_item.py -c spell -f level=4 classes=druid -n 10
```