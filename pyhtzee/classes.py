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
    THREE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 7
    FULL_HOUSE = 8
    SMALL_STRAIGHT = 9
    LARGE_STRAIGHT = 10
    YAHTZEE = 11
    CHANCE = 12
    ONE_PAIR = 13
    TWO_PAIRS = 14
    UPPER_SECTION_BONUS = 15
    YAHTZEE_BONUS = 16


class Rule(Enum):
    YAHTZEE = 0
    YAHTZEE_FREE_CHOICE_JOKER = 1
    YATZY = 2
