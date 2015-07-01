#!/usr/bin/python3

import argparse
import dice

def main():
    roller = dice.Roller(args)
    if args.target is None:
        # repeat as requested
        repeats = args.repeats or 1
        for repeat in range(repeats):
            roller.do_roll()
            print(roller.get_results())
            for result in roller:
                if isinstance(result, list):
                    print(' '.join(map(str, result)))
                else:
                    print(result)
    else:
        # repeat until the target is met
        tally = 0
        rolls = 0
        while tally < args.target and (args.repeats is None or rolls < args.repeats):
            roller.do_roll()
            tally += sum(roller.get_results())
            rolls += 1

        print("Target:", args.target)
        print("Rolls:", rolls)
        print("Outcome:", tally)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Roll Dem Bones", description="Roll some dice.")

    parser.add_argument("-r, --repeat", dest="repeats", metavar="N", type=int, default=None, help="Repeat these rolls N times. When used alongside -u, a maximum of N rolls will be made.")
    parser.add_argument("-u, --until", dest="target", metavar="T", type=int, default=None, help="Repeat these rolls as many times as needed until all their tallies combined are equal to or greater than T. Not compatable with -m.")
    parser.add_argument("-e, --explode", dest="explode", metavar="", type=int, default=None, help="Any die whose roll matches or exceeds E is counted and rolled again. Set to 1 or lower to disable this behavior on special dice.")
    parser.add_argument("-m, --mode", dest="mode", type=str, default=None, choices=['spread', 'tally'], help="Force all rolls to use the given MODE instead of each roll's default. Not compatable with -u.")
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")
    parser.add_argument("dice", nargs='*', help="Dice to roll, given in pairs of the number of dice to roll, and the sides those dice have.")

    args = parser.parse_args()

    # some basic error checking
    if len(args.dice)%2 != 0:
        parser.error("Incorrect number of arguments: Rolls and faces must be paired")

    main()
