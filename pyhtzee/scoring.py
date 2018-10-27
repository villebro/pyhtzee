"""
Scoring functions for lists with five dice. All functions (except upper sectino bonus)
are given a a list of ints representing the number of dots on the face. If the list of
dice is not valid for the scoring function, a zero is retured, indicating that the user
has stricken that score box off the scorecard.
"""
from collections import Counter
from typing import Dict, List, Set

from pyhtzee.classes import Category

CONSTANT_SCORES: Dict[Category, int] = {
    Category.FULL_HOUSE: 25,
    Category.SMALL_STRAIGHT: 30,
    Category.LARGE_STRAIGHT: 40,
    Category.YAHTZEE: 50,
    Category.EXTRA_YAHTZEES: 100,
    Category.UPPER_SECTION_BONUS: 35,
}


def score_upper_section(dice: List[int], face: int) -> int:
    return sum(die if die == face else 0 for die in dice)


def score_x_of_a_kind(dice: List[int], min_same_faces: int) -> int:
    for die, count in Counter(dice).most_common(1):
        if count >= min_same_faces:
            return sum(dice)
    return 0


def score_full_house(dice: List[int], joker_rule: bool = True) -> int:
    global CONSTANT_SCORES
    counter = Counter(dice)
    if joker_rule:
        if len(counter.keys()) == 1:
            return CONSTANT_SCORES[Category.FULL_HOUSE]
    if len(counter.keys()) == 2 and min(counter.values()) == 2:
        return CONSTANT_SCORES[Category.FULL_HOUSE]
    return 0


def _are_two_sets_equal(a: Set, b: Set) -> bool:
    return a.intersection(b) == a


def score_small_straight(dice: List[int]) -> int:
    global CONSTANT_SCORES
    dice_set = set(dice)
    if _are_two_sets_equal({1, 2, 3, 4}, dice_set) or \
            _are_two_sets_equal({2, 3, 4, 5}, dice_set) or \
            _are_two_sets_equal({3, 4, 5, 6}, dice_set):
        return CONSTANT_SCORES[Category.SMALL_STRAIGHT]
    return 0


def score_large_straight(dice: List[int]) -> int:
    global CONSTANT_SCORES
    dice_set = set(dice)
    if _are_two_sets_equal({1, 2, 3, 4, 5}, dice_set) or \
            _are_two_sets_equal({2, 3, 4, 5, 6}, dice_set):
        return CONSTANT_SCORES[Category.LARGE_STRAIGHT]
    return 0


def score_yahtzee(dice: List[int]) -> int:
    if len(set(dice)) == 1:
        return CONSTANT_SCORES[Category.YAHTZEE]
    return 0


def score_extra_yahtzee() -> int:
    return CONSTANT_SCORES[Category.EXTRA_YAHTZEES]


def score_chance(dice: List[int]) -> int:
    return sum(dice)


def score_upper_section_bonus(upper_section_score: int) -> int:
    if upper_section_score >= 63:
        return CONSTANT_SCORES[Category.UPPER_SECTION_BONUS]
    return 0
