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

`roll <count> <sides or type> [<options>]`

* 6d8, sum the total: `roll 6 8 --mode tally` or `roll 6 8 -m tally`
* 4d6, re-roll on a 6: `roll 4 6 --reroll 6` or `roll 4 6 -e 6`

## Convenience options

`roll <count> <whatever> [<options>]`

* 6d10 three times in a row: `roll 6 10 --repeat 3` or `roll 6 10 -r 3`
* 2d6 as many times as needed until they sum to 42: `roll 2 6 --repeat-until 42` or `roll 2 6 -u 42`

# Die Types

Each die type behaves in a specific way that is somehow different than a normal numeric die.

## New World of Darkness (nwod)

The nwod die type uses the die rolling rules laid out in the *New World of Darkness* rulebook. These dice have the following properties:

* 10 sides, numbered 1 through 10
* Re-roll on a 10
* Tally one "success" on a roll of 8, 9, or 10
* Results are the tally of successes

**Special Options:**

| Option | Effect |
|--------|---------|
| -o, --rote | Each of the dice in the initial pool that rolls a 1-7 is automatically rolled again before normal re-rolls are made. |
| -b, --botch | Each die that rolls a 1 cancels out the highest success die (8-10) before re-rolls are made. If a 1 die cannot cancel a success die, it counts instead as a negative tally. |

If both `--rote` and `--botch` are used, the rote rule is applied first.

# Prerequisites

Roll Dem Bones requires [Python 3](https://www.python.org/).