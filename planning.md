# Implementation Planning

1. store args for later use
    rule overrides
    behavior switches
2. create a roll object for the remaining args
    consumes (count, type) pairs
    store rule overrides
3. call rollobj.get_roll()
    gets results from .tally() or .spread()
        results are in a list corresponding to dice pairs
    pulls default reporting mode from the type of each pair in turn
        applies override from args if present
4. apply behaviors (repeat, etc.)
5. print results