#!/usr/bin/env python3

import argparse
import dice
import logging
logger = logging.getLogger()

def flatten(thing):
    """
    Flatten a non-homogenous list

    Example:
        >>> flatten([1, 2, [3, [4, 5]], 6, [7, 8]])
        [1, 2, 3, 4, 5, 6, 7, 8]

    Args:
        thing (list): The list to flatten. Items can be lists or other types.

    Yields:
        Items from the list and any lists within it, as though condensed into a
            single, flat list.
    """
    for item in thing:
        if hasattr(item, '__iter__') and not isinstance(item, str):
            for flattened_item in flatten(item):
                yield flattened_item
        else:
            yield item

def main(args):
    try:
        argvars = vars(args)
        roller = dice.Roller(*argvars['dice'], tally_threshold=args.success, **argvars)
        if args.target is None:
            # repeat as requested
            repeats = args.repeats
            if repeats is None:
                repeats = 1

            for repeat in range(repeats):
                roller.do_roll()
                total = 0
                if args.debug:
                    print(roller.raw_results)

                for result in roller.results:
                    if isinstance(result, list):
                        result = list(flatten(result))
                        total += sum(result)
                        print(' '.join(map(str, result)))
                    else:
                        total += result
                        print(result)

                # print out the total if requested
                if args.aggregate:
                    print("Total:", total)
        else:
            # repeat until the target is met
            repeats = args.repeats
            if repeats is None:
                repeats = 1

            tally = 0
            rolls = 0
            if args.aggregate:
                print("Roll totals:")
            while tally < args.target and rolls < repeats:
                roller.do_roll()
                if args.debug:
                    endchar = ':' if args.aggregate else "\n"
                    print(roller.raw_results, end=endchar)
                if args.aggregate:
                    print('', sum(roller.results))
                tally += sum(roller.results)
                rolls += 1
                if args.repeats is None:
                    repeats += 1

            print("Target:", args.target)
            print(" Rolls:", rolls)
            print(" Tally:", tally)

        return 0
    except dice.UnknownDieTypeException as e:
        logger.error("Unknown die type '{0}'".format(e))
        return 1

if __name__ == '__main__':
    version = "1.0b1"
    parser = argparse.ArgumentParser(prog="Roll Dem Bones", description="Roll some dice.")

    parser.add_argument("-r", "--repeat", dest="repeats", metavar="N", type=int, default=None, help="Repeat the described rolls %(metavar)s times.")
    parser.add_argument("-u", "--repeat-until", dest="target", metavar="T", type=int, default=None, help="Repeat these rolls as many times as needed until the combined tally matches or exceeds %(metavar)s. Use --repeats to limit the maximum number of rolls.")
    parser.add_argument("-t", "--tally-above", dest="success", metavar="T", type=int, default=None, help="Every die whose roll matches or exceeds %(metavar)s adds 1 to the roll's tally.")
    parser.add_argument("-e", "--roll-again", dest="explode", metavar="T", type=int, default=None, help="Any time a die's roll matches or exceeds %(metavar)s, it is counted and rolled again.")
    parser.add_argument("-s", "--sum", dest="aggregate", action="store_true", default=False, help="Display the sum of all dice in the roll. In spread mode, counts the rolled faces for each die. In tally mode, counts the number of dice which exceeded the threshold.")
    parser.add_argument("--debug", dest="debug", action="store_true", default=False, help="Show the raw die data for each repetition")
    parser.add_argument("--version", action="version", version="%(prog)s v{0}".format(version))
    parser.add_argument("dice", nargs='*', help="Dice to roll, given as the number of dice followed by the number of sides those dice have. Supports dice with consecutive and increasing numerical sides, as well as two special types of die: nwod and fate.")

    group_nwod = parser.add_argument_group('New World of Darkness', 'Options with special behavior for the nwod die type.')
    group_nwod.add_argument("-o", "--rote", dest="rote", action="store_true", default=False, help="Each of the dice in the initial pool that rolls a 1-7 is automatically rolled again before normal re-rolls are made.")
    group_nwod.add_argument("-b", "--botch", dest="botch", action="store_true", default=False, help="Each die that rolls a 1 cancels out the highest success die (8-10) before re-rolls are made. If a 1 die cannot cancel a success die, it counts instead as a negative tally.")

    args = parser.parse_args()

    # some basic error checking
    if len(args.dice)%2 != 0:
        parser.error("Incorrect number of arguments: Rolls and faces must be paired")

    main(args)
