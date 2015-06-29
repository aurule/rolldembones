import random

class Roller:
    dice_bunch = []
    results = None

    def __init__(self, args):
        it = iter(args.dice)
        self.dice_conf = zip(it, it)

        for pair in self.dice_conf:
            dcount = int(pair[0])
            dtype = pair[1]

            if dtype == 'nwod':
                self.dice_bunch.append([Nwod(args.explode) for r in range(dcount)])
            else:
                self.dice_bunch.append([Plain(dtype, args.explode) for r in range(dcount)])

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
                if isinstance(die.get_result(), list):
                    pair_result.extend(die.get_result())
                else:
                    pair_result.append(die.get_result())

            if die_set[0].default_mode == 'tally':
                self.results.append(sum(pair_result))
            else:
                self.results.append(pair_result)

class Plain:
    """Represents a plain numeric die."""

    default_mode = 'spread'
    children = []
    face = None
    sides = 0
    explode = 1

    def __init__(self, new_sides, new_explode = None):
        self.sides = int(new_sides)

        if new_explode is None:
            self.explode = self.sides + 1 # never explode by default
        else:
            self.explode = new_explode

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

        # rolls = [self.face] + [child.spread() for child in self.children]
        rolls = [self.face]

        for child in self.children:
            rolls.extend(child.spread())

        return rolls

    def get_result(self):
        if self.default_mode == 'spread':
            return self.spread()
        elif self.default_mode == 'tally':
            return self.tally()

    def make_child(self):
        return Plain(self.sides, self.explode)

class Nwod(Plain):
    child_class = 'Nwod'
    default_mode = 'tally'
    success = 8

    def __init__(self, new_explode = 10):
        super().__init__(10, new_explode)

    def tally(self):
        if self.face is None:
            return 0

        tally = int(self.face >= self.success)

        for child in self.children:
            tally += child.tally()

        return tally

    def make_child(self):
        return Nwod(self.explode)
