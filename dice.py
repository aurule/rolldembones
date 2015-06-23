import random

class Roll:
    raw_rolls = None
    results = None

    def __init__(self, args):
        self.overrides = dict()

        it = iter(args.dice)
        self.dice = zip(it, it)

    def get_results(self):
        """Get the last set of results from this roll's dice. If there are no results, do_roll() is executed first."""

        if self.results == None:
            self.do_roll()

        return self.results

    def do_roll(self):
        self.raw_rolls = []
        self.results = []

        for pair in self.dice:
            dcount = int(pair[0])
            dtype = pair[1]

            if dtype == 'nwod':
                die = Nwod()
            else:
                die = Plain(dtype)

            pair_rolls = [die.roll() for r in range(dcount)]
            self.raw_rolls.append(pair_rolls)

            if die.default_mode == 'tally':
                self.results.append([sum(pair_rolls)])
            elif die.default_mode == 'spread':
                self.results.append(pair_rolls)


    def tally(self):
        # tally the dice, reporting a single number
        pass

    def spread(self):
        # return a list of the rolled dice numbers
        # 1D
        pass

    def get_last_rolls(self):
        return self.raw_rolls

    # def roll(self, count, die):
    #     """Roll a number of Die objects equal to `count`"""

    #     output = []
    #     for x in range(count):
    #         dieroll = random.randint(1, die.sides)
    #         output.append(dieroll)
    #     return output

    # def do_rolls(self):
    #     repeats = 0
    #     while repeats < self.args.repeats:
    #         if repeats > 0:
    #             print("\n", end=' ')

    #         dice_to_roll = self.args.dice[:]

    #         # run through each pair of rolls (backwards)
    #         rolls_final = []
    #         while len(dice_to_roll) > 0:
    #             # set up the die type
    #             die_type = dice_to_roll.pop()
    #             die_type = die_type.lower()
    #             if (die_type == "nwod"):
    #                 # New World of Darkness die type
    #                 die = Die(10, add_roll_threshold = 10, tally_threshold = 8)
    #             else:
    #                 die = Die(int(die_type))

    #             # apply global overrides
    #             die.set_attributes(self.overrides)

    #             # roll this batch
    #             count = int(dice_to_roll.pop())
    #             raw_rolls = self.roll(count, die)

    #             rolls_final.append((die, self.post_process(raw_rolls, die)))

    #         # reverse rolls and print nicely, with each roll separated
    #         rolls_final.reverse()
    #         for (die, roll_set) in rolls_final:
    #             # print roll_set

    #             if die.tally():
    #                 # display a tally of the dice
    #                 tally = 0
    #                 for r in roll_set:
    #                     tally += die.apply_tally(r)

    #                 outstr = '\033[1;32m' + str(tally) + '\033[1;m'
    #                 if (self.args.repeats > 1):
    #                     if len(rolls_final) > 1:
    #                         outstr += ','
    #                     print(outstr, end=' ')
    #                 else:
    #                     print(outstr)
    #             else:
    #                 # no tally, so display the results as normal
    #                 outstr = '\033[1;32m' + ' '.join(map(str, roll_set)) + '\033[1;m'
    #                 if (self.args.repeats > 1):
    #                     if len(rolls_final) > 1:
    #                         outstr += ','
    #                     print(outstr, end=' ')
    #                 else:
    #                     print(outstr)

    #         repeats += 1

    # def post_process(self, raw_rolls, die):
    #     output = []

    #     i = 0
    #     while i < len(raw_rolls):
    #         r = raw_rolls[i]

    #         # replace the roll if called for
    #         if die.reroll(r):
    #             r = self.roll(1, die)

    #         # add roll if needed
    #         if die.add_roll(r):
    #             raw_rolls.extend(self.roll(1, die))

    #         # TODO
    #         # subtract at/under threshold
    #         #   remove highest of other rolls first

    #         output.append(r)

    #         i += 1

    #     return output

class Plain:
    """Represents a plain numeric die."""

    default_mode = 'spread'

    def __init__(self, sides):
        self.sides = int(sides)

    def roll(self):
        return random.randint(1, self.sides)

class Nwod(Plain):
    default_mode = 'tally'

    def __init__(self):
        pass

    def roll(self):
        face = random.randint(1, 10)

        return face > 8
