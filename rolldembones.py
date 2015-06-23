#!/usr/bin/python

import argparse
import dice

def main():
    for repeat in range(args.repeats):
        roller.do_roll()
        results = roller.get_results()
        for result in results:
            print ' '.join(map(str, result))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Roll some dice.")

    parser.add_argument("-r, --repeat", dest="repeats", type=int, metavar="N", default=1, help="Repeat these rolls N times.")
    parser.add_argument("dice", nargs='*', help="Dice to roll, given in pairs of the number of dice to roll, and the sides those dice have.")

    args = parser.parse_args()

    # some basic error checking
    if len(args.dice)%2 != 0:
        parser.error("Incorrect number of arguments: Rolls and faces must be paired")

    roller = dice.Roll(args)
    main()