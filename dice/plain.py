class Plain:
    """Represents a die type.

    Attributes:
    + sides - number of sides of the die
    + reroll_threshold - replace any die roll if its value is at or below this threshold
    + add_roll_threshold - add an extra roll if this die's value is at or above this threshold
    + tally_threshold - increase tally by one if this die's value is at or above this threshold
    """

    default_mode = 'count'

    def __init__(self, sides, reroll_threshold = None, add_roll_threshold = None, tally_threshold = None):
        self.sides = sides
        self.reroll_threshold = reroll_threshold
        self.add_roll_threshold = add_roll_threshold
        self.tally_threshold = tally_threshold

    def set_attributes(self, attrs):
        """Override existing settings using values from `attrs`

        @param attrs dict Attributes to replace
        """

        pass

    def reroll(self, value):
        """Get whether a die with result `value` should be re-rolled

        @param value int Die value
        """

        if self.reroll_threshold is None:
            return False

        return value <= self.reroll_threshold

    def add_roll(self, value):
        """Get whether a roll should be added based on a die with result `value`

        @param value int Die value
        """

        if self.add_roll_threshold is None:
            return False

        return value >= self.add_roll_threshold

    def tally(self):
        """Get whether results from this object should be tallied"""

        return self.tally_threshold is not None

    def apply_tally(self, value):
        """Convert `value` into a tally, either 1 or 0

        @param value int Die value
        """

        if value >= self.tally_threshold:
            return 1
        return 0
