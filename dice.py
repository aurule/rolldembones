import random

class Roller:
    dice_bunch = []
    results = None

    def __init__(self, args):
        self.overrides = dict()

        it = iter(args.dice)
        self.dice_conf = zip(it, it)

        for pair in self.dice_conf:
            dcount = int(pair[0])
            dtype = pair[1]

            if dtype == 'nwod':
                self.dice_bunch.append([Nwod() for r in range(dcount)])
            else:
                self.dice_bunch.append([Plain(dtype) for r in range(dcount)])

    def __iter__(self):
        return iter(self.results)

    def get_results(self):
        """Get the last set of results from this roll's dice. If there are no results, do_roll() is executed first."""

        if self.results == None:
            self.do_roll()

        return self.results

    def do_roll(self):
        self.results = []

        for die_set in self.dice_bunch:
            pair_result = []
            for die in die_set:
                die.roll()

            for die in die_set:
                pair_result.append(die.get_result())

            if die_set[0].default_mode == 'tally':
                self.results.append(sum(pair_result))
            else:
                self.results.append(pair_result)

class Plain:
    """Represents a plain numeric die."""

    default_mode = 'spread'
    face = None

    def __init__(self, sides):
        self.sides = int(sides)
        self.explode = self.sides + 1 # never explode by default

    def roll(self):
        self.face = random.randint(1, self.sides)

        self.children = []
        self.child_results = []

        if self.face >= self.explode:
            child = Plain()
            # TODO propagate settings

            child.roll()
            self.children.append(child)

    def tally(self):
        if self.face is None:
            return 0

        tally = self.face

        for child in self.children:
            tally += child.tally()

        return self.face

    def get_result(self):
        if self.default_mode == 'spread':
            return self.face
        elif self.default_mode == 'tally':
            return self.tally()

class Nwod(Plain):
    default_mode = 'tally'
    children = []
    success = 8
    explode = 10
    sides = 10

    def __init__(self):
        pass

    def tally(self):
        if self.face is None:
            return 0

        tally = int(self.face >= self.success)

        for child in self.children:
            tally += child.tally()

        return tally