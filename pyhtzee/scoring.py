"""
Scoring functions for lists with five dice. All functions (except upper sectino bonus)
are given a a list of ints representing the number of dots on the face. If the list of
dice is not valid for the scoring function, a zero is retured, indicating that the user
has stricken that score box off the scorecard.
"""
from collections import Counter
from typing import Dict, List, Set

from pyhtzee.classes import Category, Rule

CONSTANT_SCORES: Dict[Category, int] = {
    Category.YAHTZEE: 50,
}

CONSTANT_SCORES_YAHTZEE: Dict[Category, int] = {
    Category.FULL_HOUSE: 25,
    Category.SMALL_STRAIGHT: 30,
    Category.LARGE_STRAIGHT: 40,
    Category.YAHTZEE_BONUS: 100,
    Category.UPPER_SECTION_BONUS: 35,
}

CONSTANT_SCORES_YATZY: Dict[Category, int] = {
    Category.UPPER_SECTION_BONUS: 50,
}


def score_upper_section(dice: List[int], face: int) -> int:
    return sum(die if die == face else 0 for die in dice)


def score_x_of_a_kind(dice: List[int], min_same_faces: int, rule: Rule) -> int:
    if rule == Rule.YATZY:
        return score_x_of_a_kind_yatzy(dice, min_same_faces)
    else:
        return score_x_of_a_kind_yahtzee(dice, min_same_faces)


def score_x_of_a_kind_yahtzee(dice: List[int], min_same_faces: int) -> int:
    """Return sum of dice if there are a minimum of equal min_same_faces dice, otherwise
    return zero.
    """
    for die, count in Counter(dice).most_common(1):
        if count >= min_same_faces:
            return sum(dice)
    return 0


def score_x_of_a_kind_yatzy(dice: List[int], min_same_faces: int) -> int:
    """Similar to yahtzee, but only return the sum of the dice that satisfy min_same_faces
    """
    for die, count in Counter(dice).most_common(1):
        if count >= min_same_faces:
            return die * min_same_faces
    return 0


def score_full_house(dice: List[int], rule: Rule) -> int:
    global CONSTANT_SCORES_YAHTZEE
    counter = Counter(dice)
    if len(counter.keys()) == 2 and min(counter.values()) == 2:
        if rule == Rule.YATZY:
            return sum(dice)
        else:
            return CONSTANT_SCORES_YAHTZEE[Category.FULL_HOUSE]
    return 0


def _are_two_sets_equal(a: Set, b: Set) -> bool:
    return a.intersection(b) == a


def score_one_pair(dice: List[int]) -> int:
    pairs: Set[int] = set()
    for die, count in Counter(dice).most_common():
        if count >= 2:
            pairs.add(die)
    if pairs:
        sorted_pairs = sorted(pairs, reverse=True)
        return sorted_pairs[0] * 2
    return 0


def score_two_pairs(dice: List[int]) -> int:
    pairs: Set[int] = set()
    for die, count in Counter(dice).most_common():
        if count >= 2:
            pairs.add(die)
    if len(pairs) >= 2:
        sorted_pairs = sorted(pairs, reverse=True)
        return sorted_pairs[0] * 2 + sorted_pairs[1] * 2
    return 0


def score_small_straight(dice: List[int], rule: Rule) -> int:
    if rule == Rule.YATZY:
        return score_small_straight_yatzy(dice)
    else:
        return score_small_straight_yahztee(dice)


def score_small_straight_yahztee(dice: List[int]) -> int:
    """
    Small straight scoring according to regular yahtzee rules
    """
    global CONSTANT_SCORES_YAHTZEE
    dice_set = set(dice)
    if _are_two_sets_equal({1, 2, 3, 4}, dice_set) or \
            _are_two_sets_equal({2, 3, 4, 5}, dice_set) or \
            _are_two_sets_equal({3, 4, 5, 6}, dice_set):
        return CONSTANT_SCORES_YAHTZEE[Category.SMALL_STRAIGHT]
    return 0


def score_small_straight_yatzy(dice: List[int]) -> int:
    """
    Small straight scoring according to yatzy rules
    """
    dice_set = set(dice)
    if _are_two_sets_equal({1, 2, 3, 4, 5}, dice_set):
        return sum(dice)
    return 0


def score_large_straight(dice: List[int], rule: Rule) -> int:
    if rule == Rule.YATZY:
        return score_large_straight_yatzy(dice)
    else:
        return score_large_straight_yahtzee(dice)


def score_large_straight_yahtzee(dice: List[int]) -> int:
    """
    Large straight scoring according to regular yahtzee rules
    """
    global CONSTANT_SCORES_YAHTZEE
    dice_set = set(dice)
    if _are_two_sets_equal({1, 2, 3, 4, 5}, dice_set) or \
            _are_two_sets_equal({2, 3, 4, 5, 6}, dice_set):
        return CONSTANT_SCORES_YAHTZEE[Category.LARGE_STRAIGHT]
    return 0


def score_large_straight_yatzy(dice: List[int]) -> int:
    """
    Large straight scoring according to yatzy rules
    """
    dice_set = set(dice)
    if _are_two_sets_equal({2, 3, 4, 5, 6}, dice_set):
        return sum(dice)
    return 0


def score_yahtzee(dice: List[int]) -> int:
    global CONSTANT_SCORES_YAHTZEE, CONSTANT_SCORES_YATZY
    if len(set(dice)) == 1:
        return CONSTANT_SCORES[Category.YAHTZEE]
    return 0


def score_chance(dice: List[int]) -> int:
    return sum(dice)


def score_upper_section_bonus(upper_section_score: int, rule: Rule) -> int:
    global CONSTANT_SCORES_YAHTZEE, CONSTANT_SCORES_YATZY
    if upper_section_score >= 63:
        if rule == Rule.YATZY:
            return CONSTANT_SCORES_YATZY[Category.UPPER_SECTION_BONUS]
        else:
            return CONSTANT_SCORES_YAHTZEE[Category.UPPER_SECTION_BONUS]
    return 0
