import random

class Roller:
    dice_bunch = []
    results = None
    raw_results = None
    mode = None
    explode = None

    def __init__(self, args):
        it = iter(args.dice)
        self.dice_conf = zip(it, it)
        self.explode = args.explode

        if args.target is None:
            # use settings as given
            self.mode = args.mode
        else:
            # the target setting overrides the mode in order to work
            self.mode = 'tally'

        for pair in self.dice_conf:
            dcount = int(pair[0])
            dtype = pair[1]

            if dtype == 'nwod':
                self.dice_bunch.append([Nwod(self.explode, self.mode) for r in range(dcount)])
            else:
                self.dice_bunch.append([Plain(dtype, self.explode, self.mode) for r in range(dcount)])

    def __iter__(self):
        return iter(self.results)

    def get_results(self):
        """Get the last set of results from this roll's dice. If there are no results, do_roll() is executed first."""

        if self.results == None:
            self.do_roll()

        return self.results

    def do_roll(self):
        self.results = []
        self.raw_results = []

        for die_set in self.dice_bunch:
            pair_result = []
            for die in die_set:
                die.roll()

            for die in die_set:
                if isinstance(die.get_result(), list):
                    pair_result.extend(die.get_result())
                else:
                    pair_result.append(die.get_result())

            if self.mode is None:
                roll_mode = die_set[0].counting_mode
            else:
                roll_mode = self.mode

            self.raw_results.append(pair_result)
            if roll_mode == 'tally':
                self.results.append(sum(pair_result))
            else:
                self.results.append(pair_result)

class Plain:
    """Represents a plain numeric die."""

    defaults = {
        'mode': 'spread',
        'explode': None,
    }
    counting_mode = None
    children = []
    face = None
    sides = 0
    explode = 1

    def __init__(self, new_sides, new_explode = None, forced_mode = None):
        self.sides = int(new_sides)

        if new_explode is None:
            if self.defaults['explode'] is None:
                self.explode = self.sides + 1 # never explode by default
            else:
                self.explode = self.defaults['explode']
        else:
            self.explode = new_explode

        if forced_mode is None:
            self.counting_mode = self.defaults['mode']
        else:
            self.counting_mode = forced_mode

    def roll(self):
        self.face = random.randint(1, self.sides)

        self.children = []
        self.child_results = []

        if self.face >= self.explode:
            child = self.make_child()

            child.roll()
            self.children.append(child)

    def tally(self):
        if self.face is None:
            return 0

        tally = self.face

        for child in self.children:
            tally += child.tally()

        return tally

    def spread(self):
        if self.face is None:
            return 0

        rolls = [self.face]

        for child in self.children:
            rolls.extend(child.spread())

        return rolls

    def get_result(self):
        if self.counting_mode == 'spread':
            return self.spread()
        elif self.counting_mode == 'tally':
            return self.tally()

    def make_child(self):
        return Plain(self.sides, self.explode)

class Nwod(Plain):
    defaults = {
        'mode': 'tally',
        'explode': 10,
    }
    child_class = 'Nwod'
    success = 8

    def __init__(self, new_explode = 10, forced_mode = 'tally'):
        super().__init__(10, new_explode, forced_mode)

    def tally(self):
        if self.face is None:
            return 0

        tally = int(self.face >= self.success)

        for child in self.children:
            tally += child.tally()

        return tally

    def make_child(self):
        return Nwod(self.explode)
