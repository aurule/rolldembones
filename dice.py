import random

class Roller:
    dice_bunch = []
    results = None
    raw_results = None
    mode = None

    def __init__(self, args):
        it = iter(args.dice)
        self.dice_conf = zip(it, it)

        self.mode = args.mode if args.target is None else 'tally'

        for pair in self.dice_conf:
            dcount = int(pair[0])
            dtype = pair[1]

            if dtype == 'nwod':
                self.dice_bunch.append([Nwod(args.explode, self.mode, args.rote, args.botch) for r in range(dcount)])
            else:
                self.dice_bunch.append([Plain(dtype, args.explode, self.mode) for r in range(dcount)])

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

            die_type = die_set[0]
            die_type.apply_rules(die_set)

            roll_mode = die_type.counting_mode if self.mode is None else self.mode

            self.raw_results.append(pair_result)
            if roll_mode == 'tally':
                self.results.append(sum(pair_result))
            elif roll_mode == 'spread':
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
            self.explode = self.sides + 1 if self.defaults['explode'] is None else self.defaults['explode']
        else:
            self.explode = new_explode

        self.counting_mode = self.defaults['mode'] if forced_mode is None else forced_mode

    def roll(self):
        self.face = random.randint(1, self.sides)
        self.roll_children()

    def roll_children(self):
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
        return Plain(self.sides, self.explode, self.counting_mode)

    def apply_rules(self, dice_bunch):
        """Used to apply special die-type-specific rules to a group of rolled dice objects.

        Intended to be overridden by subclasses.
        """

        pass

class Nwod(Plain):
    defaults = {
        'mode': 'tally',
        'explode': 10,
    }
    child_class = 'Nwod'
    success = 8
    rote = False
    botch = False

    def __init__(self, new_explode = 10, forced_mode = 'tally', rote = False, botch = False):
        super().__init__(10, new_explode, forced_mode)
        self.rote = rote
        self.botch = botch

    def roll(self):
        self.face = random.randint(1, self.sides)

        if self.rote and self.face < self.success:
            self.face = random.randint(1, self.sides)

        super().roll_children()


    def tally(self):
        if self.face is None:
            return 0

        tally = int(self.face >= self.success)

        for child in self.children:
            tally += child.tally()

        return tally

    def make_child(self):
        return Nwod(self.explode, self.counting_mode)

    def apply_rules(self, dice_bunch):
        pass

