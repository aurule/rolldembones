#!/usr/bin/python3

import argparse
import dice
import logging
logger = logging.getLogger()

def main():
    try:
        roller = dice.Roller(args)
        if args.target is None:
            # repeat as requested
            repeats = args.repeats or 1
            for repeat in range(repeats):
                roller.do_roll()
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
            print(" Rolls:", rolls)
            print(" Tally:", tally)

        return 0
    except dice.UnknownDieTypeException as e:
        logger.error("Unknown die type '{0}'".format(e))
        return 1
    except BaseException:
        logger.info("user stop")
        return 1

if __name__ == '__main__':
    version = "0.5"
    parser = argparse.ArgumentParser(prog="Roll Dem Bones", description="Roll some dice.")

    parser.add_argument("-r", "--repeat", dest="repeats", metavar="N", type=int, default=None, help="Repeat these rolls N times. When used alongside -u, a maximum of N rolls will be made.")
    parser.add_argument("-u", "--repeat-until", dest="target", metavar="T", type=int, default=None, help="Repeat these rolls as many times as needed until all their tallies combined match or exceed T. Overrides -m.")
    parser.add_argument("-m", "--mode", dest="mode", type=str, default=None, choices=['spread', 'tally'], help="Force all rolls to use the given MODE instead of each roll's default. Ignored when using -u.")
    parser.add_argument("-t", "--tally-above", dest="success", metavar="T", type=int, default=None, help="Any die whose roll matches or exceeds T adds 1 to the tally.")
    parser.add_argument("-e", "--roll-again", dest="explode", metavar="T", type=int, default=None, help="Any die whose roll matches or exceeds T is counted and rolled again. Setting T to 1 or lower disables re-rolls.")
    parser.add_argument("-s", "--sum-all", dest="aggregate", action="store_true", default=False, help="Display the sum of all rolls in each repetition. Incompatable with -u.")
    parser.add_argument("--version", action="version", version="%(prog)s v{0}".format(version))
    parser.add_argument("dice", nargs='*', help="Dice to roll, given in pairs of the number of dice to roll, and the sides those dice have.")

    group_nwod = parser.add_argument_group('New World of Darkness', 'Options with special behavior for the nwod die type.')
    group_nwod.add_argument("-o", "--rote", dest="rote", action="store_true", default=False, help="Each of the dice in the initial pool that rolls a 1-7 is automatically rolled again before normal re-rolls are made.")
    group_nwod.add_argument("-b", "--botch", dest="botch", action="store_true", default=False, help="Each die that rolls a 1 cancels out the highest success die (8-10) before re-rolls are made. If a 1 die cannot cancel a success die, it counts instead as a negative tally.")

    args = parser.parse_args()

    # some basic error checking
    if len(args.dice)%2 != 0:
        parser.error("Incorrect number of arguments: Rolls and faces must be paired")

    main()
