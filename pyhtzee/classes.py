"""
Common classes needed for gameplay
"""
from enum import Enum, IntEnum


class Category(IntEnum):
    ACES = 0
    TWOS = 1
    THREES = 2
    FOURS = 3
    FIVES = 4
    SIXES = 5
    THREE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 7
    FULL_HOUSE = 8
    SMALL_STRAIGHT = 9
    LARGE_STRAIGHT = 10
    YAHTZEE = 11
    CHANCE = 12
    UPPER_SECTION_BONUS = 13
    EXTRA_YAHTZEES = 14


# TODO: add FORCED_JOKER and ORIGINAL_JOKER
class Rule(Enum):
    REGULAR = 0
    FREE_CHOICE_JOKER = 1
