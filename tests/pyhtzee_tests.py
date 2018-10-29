from pyhtzee.classes import Category, PyhtzeeException, Rule
from pyhtzee import Pyhtzee, utils
from pyhtzee.utils import (
    dice_roll_to_action_map,
    category_to_action_map
)

from unittest import TestCase


class PyhtzeeTestCase(TestCase):
    def test_dice_values(self):
        pyhtzee = Pyhtzee()
        for die in pyhtzee.dice:
            self.assertTrue(1 <= die <= 6)

    def test_sample_action(self):
        pyhtzee = Pyhtzee()
        action = pyhtzee.sample_action()
        self.assertIn(action, pyhtzee.get_possible_actions())

    def test_invalid_action(self):
        pyhtzee = Pyhtzee()
        action = dice_roll_to_action_map[(True, True, True, True, True)]
        pyhtzee.take_action(action)
        pyhtzee.take_action(action)
        self.assertRaises(PyhtzeeException, pyhtzee.take_action, action)

    def test_rolling_of_dice(self):
        pyhtzee = Pyhtzee(seed=123)
        self.assertListEqual([1, 3, 1, 4, 3], pyhtzee.dice)
        action = utils.dice_roll_to_action_map[(True, True, True, True, True)]
        reward = pyhtzee.take_action(action)
        self.assertListEqual([1, 1, 4, 5, 5], pyhtzee.dice)
        self.assertEqual(reward, 0)
        action = utils.dice_roll_to_action_map[(False, False, False, False, True)]
        pyhtzee.take_action(action)
        self.assertListEqual([1, 1, 4, 5, 3], pyhtzee.dice)

    def test_full_round_four_threes(self):
        pyhtzee = Pyhtzee(seed=234)
        self.assertListEqual([3, 3, 1, 5, 4], pyhtzee.dice)
        action = utils.dice_roll_to_action_map[(False, False, True, True, True)]
        pyhtzee.take_action(action)
        self.assertListEqual([3, 3, 5, 6, 4], pyhtzee.dice)
        action = utils.dice_roll_to_action_map[(False, False, True, True, True)]
        pyhtzee.take_action(action)
        self.assertListEqual([3, 3, 2, 3, 3], pyhtzee.dice)
        action = category_to_action_map[Category.THREES]
        reward = pyhtzee.take_action(action)
        self.assertEqual(reward, 12)
        self.assertEqual(pyhtzee.scores[Category.THREES], reward)

    def test_full_round_unsuccessful_yahtzee(self):
        pyhtzee = Pyhtzee(seed=234)
        self.assertListEqual([3, 3, 1, 5, 4], pyhtzee.dice)
        action = category_to_action_map[Category.YAHTZEE]
        reward = pyhtzee.take_action(action)
        self.assertEqual(reward, 0)
        self.assertEqual(pyhtzee.scores[Category.YAHTZEE], reward)

    def test_completing_roung(self):
        pyhtzee = Pyhtzee(seed=345)
        action = dice_roll_to_action_map[(True, True, True, True, True)]
        pyhtzee.take_action(action)
        pyhtzee.take_action(action)
        self.assertListEqual([3, 4, 6, 3, 1], pyhtzee.dice)

    def test_full_round_successful_yahtzee(self):
        pyhtzee = Pyhtzee()
        pyhtzee.dice = [1, 1, 1, 1, 1]
        action = category_to_action_map[Category.YAHTZEE]
        reward = pyhtzee.take_action(action)
        self.assertEqual(reward, 50)
        self.assertEqual(pyhtzee.scores[Category.YAHTZEE], reward)

    def test_full_round_successful_chance(self):
        pyhtzee = Pyhtzee()
        pyhtzee.dice = [6, 6, 6, 6, 5]
        action = category_to_action_map[Category.CHANCE]
        reward = pyhtzee.take_action(action)
        self.assertEqual(reward, 29)
        self.assertEqual(pyhtzee.scores[Category.CHANCE], reward)

    def test_upper_section_bonus(self):
        pyhtzee = Pyhtzee()
        pyhtzee.dice = [1, 1, 1, 1, 1]
        pyhtzee.take_action(category_to_action_map[Category.ACES])
        pyhtzee.dice = [2, 2, 2, 2, 2]
        pyhtzee.take_action(category_to_action_map[Category.TWOS])
        pyhtzee.dice = [3, 3, 3, 3, 3]
        pyhtzee.take_action(category_to_action_map[Category.THREES])
        pyhtzee.dice = [4, 4, 4, 4, 4]
        pyhtzee.take_action(category_to_action_map[Category.FOURS])
        pyhtzee.dice = [5, 5, 5, 5, 5]
        pyhtzee.take_action(category_to_action_map[Category.FIVES])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        action = category_to_action_map[Category.SIXES]
        reward = pyhtzee.take_action(action)
        self.assertEqual(reward, 65)
        self.assertEqual(pyhtzee.scores[Category.SIXES], 30)
        self.assertEqual(pyhtzee.scores[Category.UPPER_SECTION_BONUS], 35)

    def test_perfect_joker_score(self):
        pyhtzee = Pyhtzee(rule=Rule.FREE_CHOICE_JOKER)
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.YAHTZEE])
        pyhtzee.dice = [1, 1, 1, 1, 1]
        pyhtzee.take_action(category_to_action_map[Category.ACES])
        pyhtzee.dice = [2, 2, 2, 2, 2]
        pyhtzee.take_action(category_to_action_map[Category.TWOS])
        pyhtzee.dice = [3, 3, 3, 3, 3]
        pyhtzee.take_action(category_to_action_map[Category.THREES])
        pyhtzee.dice = [4, 4, 4, 4, 4]
        pyhtzee.take_action(category_to_action_map[Category.FOURS])
        pyhtzee.dice = [5, 5, 5, 5, 5]
        pyhtzee.take_action(category_to_action_map[Category.FIVES])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.SIXES])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.THREE_OF_A_KIND])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.FOUR_OF_A_KIND])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.FULL_HOUSE])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.SMALL_STRAIGHT])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.LARGE_STRAIGHT])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.CHANCE])
        self.assertEqual(pyhtzee.get_total_score(), 1575)
        self.assertTrue(pyhtzee.is_finished())

    def test_perfect_regular_score(self):
        pyhtzee = Pyhtzee(rule=Rule.REGULAR)
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.YAHTZEE])
        pyhtzee.dice = [1, 1, 1, 1, 1]
        pyhtzee.take_action(category_to_action_map[Category.ACES])
        pyhtzee.dice = [2, 2, 2, 2, 2]
        pyhtzee.take_action(category_to_action_map[Category.TWOS])
        pyhtzee.dice = [3, 3, 3, 3, 3]
        pyhtzee.take_action(category_to_action_map[Category.THREES])
        pyhtzee.dice = [4, 4, 4, 4, 4]
        pyhtzee.take_action(category_to_action_map[Category.FOURS])
        pyhtzee.dice = [5, 5, 5, 5, 5]
        pyhtzee.take_action(category_to_action_map[Category.FIVES])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.SIXES])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.THREE_OF_A_KIND])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.FOUR_OF_A_KIND])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.FULL_HOUSE])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.SMALL_STRAIGHT])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.LARGE_STRAIGHT])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.CHANCE])
        self.assertEqual(pyhtzee.get_total_score(), 1505)
        self.assertTrue(pyhtzee.is_finished())
