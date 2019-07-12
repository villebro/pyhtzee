from pyhtzee.classes import Category, Rule
from pyhtzee.scoring import (
    CONSTANT_SCORES_YAHTZEE,
    score_upper_section,
    score_x_of_a_kind,
    score_one_pair,
    score_two_pairs,
    score_full_house,
    score_small_straight,
    score_large_straight,
    score_yahtzee,
    score_chance,
    score_upper_section_bonus,
)
from unittest import TestCase


class ScoringTestCase(TestCase):
    def test_score_upper_section(self):
        self.assertEqual(score_upper_section([1, 1, 1, 2, 3], face=1), 3)
        self.assertEqual(score_upper_section([2, 1, 2, 2, 4], face=2), 6)
        self.assertEqual(score_upper_section([1, 1, 1, 2, 3], face=6), 0)

    def test_score_three_of_a_kind_yahtzee(self):
        rule = Rule.YAHTZEE
        self.assertEqual(score_x_of_a_kind([1, 1, 1, 2, 2], 3, rule), 7)
        self.assertEqual(score_x_of_a_kind([2, 2, 2, 3, 2], 3, rule), 11)
        self.assertEqual(score_x_of_a_kind([1, 2, 2, 3, 6], 3, rule), 0)
        self.assertEqual(score_x_of_a_kind([6, 6, 6, 6, 6], 3, rule), 30)

    def test_score_three_of_a_kind_yatzy(self):
        rule = Rule.YATZY
        self.assertEqual(score_x_of_a_kind([1, 1, 1, 2, 2], 3, rule), 3)
        self.assertEqual(score_x_of_a_kind([2, 2, 2, 3, 2], 3, rule), 6)
        self.assertEqual(score_x_of_a_kind([1, 2, 2, 3, 6], 3, rule), 0)
        self.assertEqual(score_x_of_a_kind([6, 6, 6, 6, 6], 3, rule), 18)

    def test_score_four_of_a_kind_yahtzee(self):
        rule = Rule.YAHTZEE
        self.assertEqual(score_x_of_a_kind([1, 1, 1, 2, 1], 4, rule), 6)
        self.assertEqual(score_x_of_a_kind([2, 2, 2, 3, 2], 4, rule), 11)
        self.assertEqual(score_x_of_a_kind([1, 2, 2, 3, 6], 4, rule), 0)
        self.assertEqual(score_x_of_a_kind([6, 6, 6, 6, 6], 4, rule), 30)

    def test_score_four_of_a_kind_yatzy(self):
        rule = Rule.YATZY
        self.assertEqual(score_x_of_a_kind([1, 1, 1, 2, 1], 4, rule), 4)
        self.assertEqual(score_x_of_a_kind([2, 2, 2, 3, 2], 4, rule), 8)
        self.assertEqual(score_x_of_a_kind([1, 2, 2, 3, 6], 4, rule), 0)
        self.assertEqual(score_x_of_a_kind([6, 6, 6, 6, 6], 4, rule), 24)

    def test_score_one_pair(self):
        self.assertEqual(score_one_pair([1, 1, 2, 3, 4]), 2)
        self.assertEqual(score_one_pair([1, 1, 2, 2, 3]), 4)
        self.assertEqual(score_one_pair([1, 1, 6, 6, 6]), 12)
        self.assertEqual(score_one_pair([1, 2, 3, 4, 5]), 0)

    def test_score_two_pairs(self):
        self.assertEqual(score_two_pairs([1, 1, 2, 2, 4]), 6)
        self.assertEqual(score_two_pairs([1, 1, 2, 3, 4]), 0)
        self.assertEqual(score_two_pairs([2, 3, 2, 3, 2]), 10)
        self.assertEqual(score_two_pairs([1, 2, 3, 4, 5]), 0)

    def test_score_full_house_yahtzee(self):
        rule = Rule.YAHTZEE
        self.assertEqual(score_full_house([1, 1, 1, 2, 2], rule), 25)
        self.assertEqual(score_full_house([1, 1, 1, 2, 3], rule), 0)
        self.assertEqual(score_full_house([6, 6, 6, 5, 5], rule), 25)
        self.assertEqual(score_full_house([6, 6, 6, 6, 6], rule), 0)

    def test_score_full_house_yatzy(self):
        rule = Rule.YATZY
        self.assertEqual(score_full_house([1, 1, 1, 2, 2], rule), 7)
        self.assertEqual(score_full_house([1, 1, 1, 2, 3], rule), 0)
        self.assertEqual(score_full_house([6, 6, 6, 5, 5], rule), 28)
        self.assertEqual(score_full_house([6, 6, 6, 6, 6], rule), 0)

    def test_score_small_straight_yahtzee(self):
        rule = Rule.YAHTZEE
        self.assertEqual(score_small_straight([1, 3, 2, 5, 4], rule), 30)
        self.assertEqual(score_small_straight([6, 3, 5, 4, 1], rule), 30)
        self.assertEqual(score_small_straight([2, 3, 5, 4, 2], rule), 30)
        self.assertEqual(score_small_straight([1, 1, 1, 1, 1], rule), 0)
        self.assertEqual(score_small_straight([1, 2, 3, 5, 4], rule), 30)

    def test_score_small_straight_yatzy(self):
        rule = Rule.YATZY
        self.assertEqual(score_small_straight([1, 3, 2, 5, 4], rule), 15)
        self.assertEqual(score_small_straight([6, 3, 5, 4, 1], rule), 0)
        self.assertEqual(score_small_straight([2, 3, 5, 4, 6], rule), 0)
        self.assertEqual(score_small_straight([1, 1, 1, 1, 1], rule), 0)
        self.assertEqual(score_small_straight([1, 2, 3, 5, 4], rule), 15)

    def test_score_large_straight_yahtzee(self):
        rule = Rule.YAHTZEE
        self.assertEqual(score_large_straight([1, 3, 2, 5, 4], rule), 40)
        self.assertEqual(score_large_straight([6, 3, 5, 4, 2], rule), 40)
        self.assertEqual(score_large_straight([2, 3, 5, 4, 2], rule), 0)
        self.assertEqual(score_large_straight([1, 1, 1, 1, 1], rule), 0)

    def test_score_large_straight_yatzy(self):
        rule = Rule.YATZY
        self.assertEqual(score_large_straight([1, 3, 2, 5, 4], rule), 0)
        self.assertEqual(score_large_straight([6, 3, 5, 4, 2], rule), 20)
        self.assertEqual(score_large_straight([2, 3, 5, 4, 2], rule), 0)
        self.assertEqual(score_large_straight([1, 1, 1, 1, 1], rule), 0)

    def test_score_yahtzee(self):
        self.assertEqual(score_yahtzee([1, 1, 1, 1, 1]), 50)
        self.assertEqual(score_yahtzee([2, 2, 2, 3, 2]), 0)
        self.assertEqual(score_yahtzee([6, 6, 6, 6, 6]), 50)

    def test_score_chance(self):
        self.assertEqual(score_chance([1, 1, 1, 1, 1]), 5)
        self.assertEqual(score_chance([6, 6, 6, 6, 6]), 30)
        self.assertEqual(score_chance([1, 2, 3, 4, 5]), 15)

    def test_upper_section_bonus_yahtzee(self):
        rule = Rule.YAHTZEE
        self.assertEqual(score_upper_section_bonus(0, rule), 0)
        self.assertEqual(score_upper_section_bonus(63, rule), 35)
        self.assertEqual(score_upper_section_bonus(100, rule), 35)

    def test_upper_section_bonus_yatzy(self):
        rule = Rule.YATZY
        self.assertEqual(score_upper_section_bonus(0, rule), 0)
        self.assertEqual(score_upper_section_bonus(63, rule), 50)
        self.assertEqual(score_upper_section_bonus(100, rule), 50)

    def test_score_extra_yahtzee(self):
        self.assertEqual(CONSTANT_SCORES_YAHTZEE[Category.YAHTZEE_BONUS], 100)

    def test_naive_max_score_yahtzee(self):
        rule = Rule.YAHTZEE
        upper_section_score = (
            score_upper_section([1, 1, 1, 1, 1], 1)
            + score_upper_section([2, 2, 2, 2, 2], 2)
            + score_upper_section([3, 3, 3, 3, 3], 3)
            + score_upper_section([4, 4, 4, 4, 4], 4)
            + score_upper_section([5, 5, 5, 5, 5], 5)
            + score_upper_section([6, 6, 6, 6, 6], 6)
        )
        upper_section_bonus = score_upper_section_bonus(upper_section_score, rule)
        lower_section_score = (
            score_x_of_a_kind([6, 6, 6, 6, 6], 3, rule)
            + score_x_of_a_kind([6, 6, 6, 6, 6], 4, rule)
            + score_full_house([6, 6, 6, 5, 5], rule)
            + score_small_straight([1, 2, 3, 4, 5], rule)
            + score_large_straight([1, 2, 3, 4, 5], rule)
            + score_yahtzee([6, 6, 6, 6, 6])
            + score_chance([6, 6, 6, 6, 6])
        )

        self.assertEqual(upper_section_score, 105)
        self.assertEqual(upper_section_bonus, 35)
        self.assertEqual(lower_section_score, 235)
        self.assertEqual(
            upper_section_score + upper_section_bonus + lower_section_score, 375
        )
