import random
import copy

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
                self.dice_bunch.append([Nwod(args.explode, self.mode, args.success, args.rote, args.botch) for r in range(dcount)])
            elif dtype in ['fudge', 'fate']:
                self.dice_bunch.append([Fudge(args.explode, self.mode, args.success) for r in range(dcount)])
            else:
                try:
                    dfaces = int(dtype)
                    self.dice_bunch.append([Plain(dfaces, args.explode, self.mode, args.success) for r in range(dcount)])
                except ValueError:
                    raise UnknownDieTypeException(dtype)

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

            die_type = die_set[0]
            dice_transformed = die_type.apply_rules(die_set)

            for die in dice_transformed:
                if isinstance(die.get_result(), list):
                    pair_result.extend(die.get_result())
                else:
                    pair_result.append(die.get_result())

            roll_mode = die_type.counting_mode if self.mode is None else self.mode

            self.raw_results.append(pair_result)
            if roll_mode == 'tally':
                self.results.append(sum(pair_result))
            elif roll_mode == 'spread':
                self.results.append(pair_result)

class Die:
    """Base dice class

    This class can technically be used on its own, but it's intended to be subclassed to create specific die types.
    """

    defaults = {
        'mode': 'spread',
        'explode': None,
        'success': None,
    }
    counting_mode = None
    children = []
    face = None
    sides = 0
    explode = 1
    success = None

    def __init__(self, new_sides, new_explode = None, forced_mode = None, success_target = None):
        self.sides = int(new_sides)

        if new_explode is None:
            self.explode = self.sides + 1 if self.defaults['explode'] is None else self.defaults['explode']
        else:
            self.explode = new_explode

        self.counting_mode = self.defaults['mode'] if forced_mode is None else forced_mode

        self.success = self.defaults['success'] if success_target is None else success_target

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

        tally = self.face if self.success is None else int(self.face >= self.success)

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

    def apply_rules(self, die_set):
        """Apply special die-type-specific post processing to a group of dice objects.

        Intended to be overridden by subclasses.
        """

        return die_set

class Plain(Die):
    """Represents a plain numeric die."""

    def __init__(self, new_sides, new_explode = None, forced_mode = None, success_target = None):
        super().__init__(new_sides, new_explode, forced_mode, success_target)

        # tally on our highest number by default
        if self.success is None:
            self.success = self.sides

class Nwod(Die):
    defaults = {
        'mode': 'tally',
        'explode': 10,
        'success': 8,
    }
    child_class = 'Nwod'
    rote = False
    botch = False

    def __init__(self, new_explode = 10, forced_mode = 'tally', success_target = 8, rote = False, botch = False):
        super().__init__(10, new_explode, forced_mode, success_target)
        self.rote = rote
        self.botch = botch

    def roll(self):
        self.face = random.randint(1, self.sides)

        if self.rote and self.face < self.success:
            self.face = random.randint(1, self.sides)

        super().roll_children()

    def tally(self):
        if self.botch and self.face == 1:
            return -1

        return super().tally()

    def make_child(self):
        return Nwod(self.explode, self.counting_mode, self.success)

class Fudge(Die):
    defaults = {
        'mode': 'tally',
        'explode': None,
        'success': None,
    }

    def __init__(self, new_explode = None, forced_mode = 'tally', success_target = None):
        super().__init__(3, new_explode, forced_mode, success_target)

    def roll(self):
        # Six sides of -1, -1, 0, 0, +1, +1 reduce trivially to three sides of -1, 0, +1. So that's what we use.
        self.face = random.randint(-1, 1)
        super().roll_children()

    def tally(self):
        return self.face

    def make_child(self):
        return Fudge(self.explode, self.counting_mode, self.success)

class UnknownDieTypeException(Exception):
    """Unrecognized die type"""