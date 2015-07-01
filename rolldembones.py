#!/usr/bin/python3

import argparse
import dice

def main():
    roller = dice.Roller(args)
    for repeat in range(args.repeats):
        roller.do_roll()
        for result in roller:
            if isinstance(result, list):
                print(' '.join(map(str, result)))
            else:
                print(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Roll some dice.")

    parser.add_argument("-r, --repeat", dest="repeats", metavar="N", type=int, default=1, help="Repeat these rolls N times.")
    parser.add_argument("-e, --explode", dest="explode", metavar="", type=int, default=None, help="Any die whose roll matches or exceeds E is counted and rolled again. Set to 1 or lower to disable this behavior on special dice.")
    parser.add_argument("-m, --mode", dest="mode", metavar="MODE", type=str, default=None, help="Force all rolls to use the given MODE instead of each roll's default. Valid modes are 'tally' or 'spread'.")
    parser.add_argument("dice", nargs='*', help="Dice to roll, given in pairs of the number of dice to roll, and the sides those dice have.")

    args = parser.parse_args()

    # some basic error checking
    if len(args.dice)%2 != 0:
        parser.error("Incorrect number of arguments: Rolls and faces must be paired")

    main()
