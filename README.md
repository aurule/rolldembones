# Roll Dem Bones

Roll Dem Bones is a CLI python script for rolling dice. It is designed to be extendible, allowing new types of dice rules to be added with ease. It comes with presets for a few common dice rules used in tabletop games.

# Usage

Here are some examples that show ways to roll dice using Roll Dem Bones. For full usage information, run `roll -h`.

## Roll some dice without special rules

`roll <count> <sides>`

* 4d6: `roll 4 6`
* 1d20: `roll 1 20`
* 8d13: `roll 8 13`
* 4d6 and 3d8: `roll 4 6 3 8`

## Roll some dice using preset rules

`roll <count> <type>`

* New World of Darkness: `roll 6 nwod`

## Set custom rules on the fly

`roll <count> <whatever> [<options>]`

* 6d8, sum the total: `roll 6 8 --tally` or `roll 6 8 -t`
* 4d6, re-roll on a 6: `roll 4 6 --reroll 6` or `roll 4 6 -e 6`

## Convenience options

`roll <count> <whatever> [<options>]`

* 6d10 three times in a row: `roll 6 10 --repeat 3` or `roll 6 10 -r 3`

# Prerequisites

Roll Dem Bones requires [Python 3](https://www.python.org/).