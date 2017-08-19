import random
import copy

class Roller:
    def __init__(self, *dice, explode=None, tally_threshold=None, **kwargs):
        self.results = None
        self.raw_results = None

        self.rollable_dice = []
        dice_iter = iter(dice)
        dice_pairs = zip(dice_iter, dice_iter)
        for pair in dice_pairs:
            die_count = int(pair[0])
            die_type = pair[1]

            # handle special types first
            if die_type == 'nwod':
                new_set = RollSet(
                        dice=[Nwod(explode=explode, tally_threshold=tally_threshold, **kwargs) for r in range(die_count)],
                        result_mode='tally')
            elif die_type in ['fudge', 'fate']:
                new_set = RollSet(
                    dice=[Fudge() for r in range(die_count)],
                    result_mode='tally')
            else:
                try:
                    dfaces = int(die_type)
                    new_set = RollSet(
                        dice=[Plain(dfaces, explode=explode, tally_threshold=tally_threshold) for r in range(die_count)],
                        result_mode='spread')
                except ValueError:
                    raise UnknownDieTypeException(die_type)
            self.rollable_dice.append(new_set)

    def __iter__(self):
        return iter(self.results)

    def do_roll(self):
        self.results = []
        self.raw_results = []

        for die_set in self.rollable_dice:
            set_raw_result = []
            set_result = []

            die_set.roll()
            self.raw_results.append(die_set.raw_results)
            self.results.append(die_set.get_result())

class RollSet:
    def __init__(self, dice, result_mode='spread'):
        self.dice = dice
        self.result_mode = result_mode
        self.raw_results = None
        self.results = None

    def roll(self):
        self.raw_results = []
        self.results = []
        for die in self.dice:
            die.roll()
            self.raw_results.extend(die.spread())
            self.results.append(die.get_result(self.result_mode))

    def get_result(self):
        if self.result_mode == 'spread':
            return self.results
        elif self.result_mode == 'tally':
            return sum(self.results)

class Die:
    """
    Base dice class

    This class can technically be used on its own, but it's intended to be
    subclassed to create specific die types. For a generic die, use the Plain class.
    """

    def __init__(self, sides, explode = None, tally_threshold = None):
        self.sides = int(sides)

        self.explode = explode
        self.tally_threshold = tally_threshold

        self.children = []
        self.face = None

    def roll(self):
        self.children = []
        self.face = random.randint(1, self.sides)
        self.make_children()
        self.roll_children()

    def make_children(self):
        """
        Handle child dice for rerolls

        By default, this handles simple exploding dice. When overriding, be sure
        to call super.
        """
        if self.explode and self.face >= self.explode:
            self.add_child()

    def roll_children(self):
        """
        Roll all child dice

        Roll every die in the children array that has not already been rolled.
        """
        for die in self.children:
            if die.face is None:
                die.roll()

    def tally(self):
        """Add one to the total if the rolled value is greater than the threshold"""
        if self.face is None:
            return 0

        if self.tally_threshold is None:
            tally = self.face
        else:
            tally = int(self.face >= self.tally_threshold)

        for child in self.children:
            tally += child.tally()

        return tally

    def spread(self):
        """Make an array of our value and all child values"""
        if self.face is None:
            return 0

        rolls = [self.face]

        for child in self.children:
            rolls.extend(child.spread())

        return rolls

    def get_result(self, mode='spread'):
        """
        Get the result of this die roll based on reporting mode

        Arguments:
            mode (str) One of 'spread' or 'tally'.
        """
        if mode == 'spread':
            return self.spread()
        elif mode == 'tally':
            return self.tally()

    def add_child(self):
        """
        Add a child die

        Calls make_child to actually create the new die. Convenience method that
        isn't meant to be overwritten.
        """
        self.children.append(self.make_child())

    def make_child(self):
        """
        Construct a child die

        This must be overwritten by subclasses to define the sort of die that
        should be added when another roll is needed.
        """
        pass

class Plain(Die):
    """Represents a plain numeric die."""

    def make_child(self):
        """
        Construct a child die

        This must be overwritten by subclasses to define the sort of die that
        should be added when another roll is needed.
        """
        return Plain(self.sides, explode=self.explode, tally_threshold=self.tally_threshold)

class Nwod(Die):
    """
    Represents a d10 using the New World of Darkness dice rules.

    The special rules:
    * Tally mode is the default
    * A success is counted on a roll of 8 or higher
    * A roll of 10 rolls another die

    Additional optional rules:
    * Rote: When true, all dice in the initial pool that are below 8 add another
            die to the pool, effectively re-rolling them. This property *does not*
            get passed on to child dice.
    * Botch: When true, dice that roll a 1 *subtract* one success from the tally.
    """
    def __init__(self, explode=10, tally_threshold=8, rote=False, botch=False, **kwargs):
        if explode is None:
            explode = 10
        if tally_threshold is None:
            tally_threshold = 8
        if rote is None:
            rote = False
        if botch is None:
            botch = False

        super().__init__(10, explode=explode, tally_threshold=tally_threshold)
        self.rote = rote
        self.botch = botch

    def make_children(self):
        super().make_children()

        if self.rote and self.face < self.tally_threshold:
            self.add_child()

    def tally(self):
        if self.botch and self.face == 1:
            return -1

        return super().tally()

    def make_child(self):
        """
        Create a re-rolled child die
        """
        return Nwod(explode=self.explode, tally_threshold=self.tally_threshold, rote=False, botch=self.botch)

    def get_result(self, mode='tally'):
        return super().get_result(mode)

class Fudge(Die):
    """
    Represents a d6 with sides corresponding to a Fudge die: -1, -1, 0, 0, +1, +1

    Defualt result mode is tally.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(6)

    def roll(self):
        # Six sides of -1, -1, 0, 0, +1, +1 reduce trivially to three sides of -1, 0, +1. So that's what we use.
        self.face = random.randint(-1, 1)

    def tally(self):
        return self.face

    def get_result(self, mode='tally'):
        return super().get_result(mode)

class UnknownDieTypeException(Exception):
    """Unrecognized die type"""
