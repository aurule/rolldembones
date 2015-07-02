# Roll Dem Bones

Roll Dem Bones is a CLI python script for rolling dice. It is designed to be extendible, allowing new types of dice rules to be added with ease. It comes with presets for a few common dice rules used in tabletop games.

# Installing

Download the latest release and unpack it to a directory of your choice. Symlink and/or add rolldembones to your path to use it from the console.

Roll Dem Bones requires [Python 3](https://www.python.org/).

# Examples

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

* 6d10 three times in a row: `roll 6 10 --repeat 3` or `roll 6 10 -r 3`
* 2d6 as many times as needed until they sum to 42: `roll 2 6 --repeat-until 42` or `roll 2 6 -u 42`

# Features

Roll Dem Bones has a number of command-line options to modify the dice individually and in aggregate.

## Reporting Mode

Roll Dem Bones can report die outcomes in two modes, tally and spread.

**Spread** mode shows the values of all the rolled dice. It's the default mode.

**Tally** mode shows the sum of the rolled dice.

Every type of die has a default reporting mode, and they can safely be mixed. If you want to force a certain reporting mode, the `--mode {tally, spread}` option lets you do so. Additionally, the `--repeat-until` option *always* uses tally mode.

The `--tally-above T` option changes the behavior of the tally mode. It counts how many dice rolled T or higher, instead of summing the values of the die faces.

## Repeat and Repeat-Until

These options repeat the set of rolls that were passed to Roll Dem Bones a certain number of times.

On its own, `--repeat N` simply repeats the dice rolls `N` times. So `--repeat 5` will repeat the rolls 5 times, printing the results of each repetition.

The option `--repeat-until M` sets the mode to `tally` and repeats the dice rolls until their combined tally meets or exceeds `M`. It overrides the default mode of each die type used, as well as the value of the `--mode` option (if present). Roll Dem Bones will display the target, number of rolls, and final tally instead of the outcome of each roll.

When `--repeat N` is used alongside Repeat-Until, Roll Dem Bones will not make more than `N` rolls.

## Adding Dice

The `--roll-again T` option adds a die every time a die rolls `T` or higher.

# Die Types

Each die type represents a specific set of dice rules that somehow differ from rolling a normal, numeric die. Below are explanations of the built-in die types in Roll Dem Bones.

## New World of Darkness (nwod)

The nwod die type uses the die rolling rules laid out in the *New World of Darkness* rulebook. These dice have the following properties:

* 10 sides, numbered 1 through 10
* Roll again on a 10
* Tally one "success" on a roll of 8, 9, or 10
* Uses tally mode by default, tallying 1 per success

**Special Options:**

| Option | Effect |
|--------|---------|
| -o, --rote | Each of the dice in the initial pool that rolls a 1-7 is automatically rolled again before normal re-rolls are made. |
| -b, --botch | Each die that rolls a 1 cancels out the highest success die (8-10) before re-rolls are made. If a 1 die cannot cancel a success die, it counts instead as a negative tally. |

If both `--rote` and `--botch` are used, the rote rule is applied first.
