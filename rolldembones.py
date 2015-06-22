#!/usr/bin/python

import argparse
import random
import dice

class Roller:
    def __init__(self, args):
        self.args = args
        self.overrides = dict()

    def roll(self, count, die):
        """Roll a number of Die objects equal to `count`"""

        output = []
        for x in range(count):
            dieroll = random.randint(1, die.sides)
            output.append(dieroll)
        return output

    def do_rolls(self):
        repeats = 0
        while repeats < self.args.repeats:
            if repeats > 0:
                print("\n", end=' ')

            dice_to_roll = self.args.dice[:]

            # run through each pair of rolls (backwards)
            rolls_final = []
            while len(dice_to_roll) > 0:
                # set up the die type
                die_type = dice_to_roll.pop()
                die_type = die_type.lower()
                if (die_type == "nwod"):
                    # New World of Darkness die type
                    die = Die(10, add_roll_threshold = 10, tally_threshold = 8)
                else:
                    die = Die(int(die_type))

                # apply global overrides
                die.set_attributes(self.overrides)

                # roll this batch
                count = int(dice_to_roll.pop())
                raw_rolls = self.roll(count, die)

                rolls_final.append((die, self.post_process(raw_rolls, die)))

            # reverse rolls and print nicely, with each roll separated
            rolls_final.reverse()
            for (die, roll_set) in rolls_final:
                # print roll_set

                if die.tally():
                    # display a tally of the dice
                    tally = 0
                    for r in roll_set:
                        tally += die.apply_tally(r)

                    outstr = '\033[1;32m' + str(tally) + '\033[1;m'
                    if (self.args.repeats > 1):
                        if len(rolls_final) > 1:
                            outstr += ','
                        print(outstr, end=' ')
                    else:
                        print(outstr)
                else:
                    # no tally, so display the results as normal
                    outstr = '\033[1;32m' + ' '.join(map(str, roll_set)) + '\033[1;m'
                    if (self.args.repeats > 1):
                        if len(rolls_final) > 1:
                            outstr += ','
                        print(outstr, end=' ')
                    else:
                        print(outstr)

            repeats += 1

    def post_process(self, raw_rolls, die):
        output = []

        i = 0
        while i < len(raw_rolls):
            r = raw_rolls[i]

            # replace the roll if called for
            if die.reroll(r):
                r = self.roll(1, die)

            # add roll if needed
            if die.add_roll(r):
                raw_rolls.extend(self.roll(1, die))

            # TODO
            # subtract at/under threshold
            #   remove highest of other rolls first

            output.append(r)

            i += 1

        return output

def main():
    roller.do_rolls()
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Roll some dice.")

    parser.add_argument("-r, --repeat", dest="repeats", type=int, metavar="N", default=1, help="Repeat these rolls N times.")
    parser.add_argument("dice", nargs='*', help="Dice to roll, given in pairs of the number of dice to roll, and the sides those dice have.")

    args = parser.parse_args()

    # some basic error checking
    if len(args.dice)%2 != 0:
        parser.error("Incorrect number of arguments: Rolls and faces must be paired")

    roller = Roller(args)
    main()