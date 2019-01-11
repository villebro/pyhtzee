"""
Common classes needed for gameplay
"""
from enum import Enum, IntEnum


class PyhtzeeException(Exception):
    pass


class Category(IntEnum):
    ACES = 0
    TWOS = 1
    THREES = 2
    FOURS = 3
    FIVES = 4
    SIXES = 5
    ONE_PAIR = 6
    TWO_PAIRS = 7
    THREE_OF_A_KIND = 8
    FOUR_OF_A_KIND = 9
    FULL_HOUSE = 10
    SMALL_STRAIGHT = 11
    LARGE_STRAIGHT = 12
    YAHTZEE = 13
    CHANCE = 14
    UPPER_SECTION_BONUS = 15
    YAHTZEE_BONUS = 16


class Rule(Enum):
    YAHTZEE = 0
    YAHTZEE_FREE_CHOICE_JOKER = 1
    YATZY = 2
