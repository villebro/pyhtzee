from pyhtzee.classes import Category, PyhtzeeException, Rule
from pyhtzee import Pyhtzee, utils
from pyhtzee.utils import dice_roll_to_action_map, category_to_action_map

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

    def test_possible_actions_yahtzee(self):
        pyhtzee = Pyhtzee(rule=Rule.YAHTZEE)
        initial_possible_actions = pyhtzee.get_possible_actions()
        actions = [
            category_to_action_map[Category.YAHTZEE],
            category_to_action_map[Category.ACES],
            category_to_action_map[Category.TWOS],
            category_to_action_map[Category.THREES],
            category_to_action_map[Category.FOURS],
            category_to_action_map[Category.FIVES],
            category_to_action_map[Category.SIXES],
            category_to_action_map[Category.THREE_OF_A_KIND],
            category_to_action_map[Category.FOUR_OF_A_KIND],
            category_to_action_map[Category.FULL_HOUSE],
            category_to_action_map[Category.SMALL_STRAIGHT],
            category_to_action_map[Category.LARGE_STRAIGHT],
        ]

        expected_final_possible_actions = list(initial_possible_actions)
        for action in actions:
            pyhtzee.take_action(action)
            expected_final_possible_actions.remove(action)

        final_possible_actions = pyhtzee.get_possible_actions()
        self.assertListEqual(final_possible_actions, expected_final_possible_actions)

    def test_possible_actions_yatzy(self):
        pyhtzee = Pyhtzee(rule=Rule.YATZY)
        initial_possible_actions = pyhtzee.get_possible_actions()
        actions = [
            category_to_action_map[Category.YAHTZEE],
            category_to_action_map[Category.ACES],
            category_to_action_map[Category.TWOS],
            category_to_action_map[Category.THREES],
            category_to_action_map[Category.FOURS],
            category_to_action_map[Category.FIVES],
            category_to_action_map[Category.SIXES],
            category_to_action_map[Category.ONE_PAIR],
            category_to_action_map[Category.TWO_PAIRS],
            category_to_action_map[Category.THREE_OF_A_KIND],
            category_to_action_map[Category.FOUR_OF_A_KIND],
            category_to_action_map[Category.FULL_HOUSE],
            category_to_action_map[Category.SMALL_STRAIGHT],
            category_to_action_map[Category.LARGE_STRAIGHT],
        ]

        expected_final_possible_actions = list(initial_possible_actions)
        for action in actions:
            pyhtzee.take_action(action)
            expected_final_possible_actions.remove(action)

        final_possible_actions = pyhtzee.get_possible_actions()
        self.assertListEqual(final_possible_actions, expected_final_possible_actions)

    def test_invalid_action(self):
        pyhtzee = Pyhtzee()
        action = dice_roll_to_action_map[(True, True, True, True, True)]
        pyhtzee.take_action(action)
        pyhtzee.take_action(action)
        self.assertRaises(PyhtzeeException, pyhtzee.take_action, action)

    def test_rolling_of_dice(self):
        pyhtzee = Pyhtzee(seed=123)
        original_dice = tuple(pyhtzee.dice)
        # This is a bad test; it is perfectly possible to get the exact
        # same dice twice despite full reroll
        action = utils.dice_roll_to_action_map[(True, True, True, True, True)]
        pyhtzee.take_action(action)
        self.assertNotEqual(original_dice, tuple(pyhtzee.dice))
        # This test makes more sense; make sure first four dice aren't rerolled
        original_dice = tuple(pyhtzee.dice)
        action = utils.dice_roll_to_action_map[(False, False, False, False, True)]
        pyhtzee.take_action(action)
        self.assertEqual(original_dice[0], pyhtzee.dice[0])
        self.assertEqual(original_dice[1], pyhtzee.dice[1])
        self.assertEqual(original_dice[2], pyhtzee.dice[2])
        self.assertEqual(original_dice[3], pyhtzee.dice[3])

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
        pyhtzee = Pyhtzee(rule=Rule.YAHTZEE_FREE_CHOICE_JOKER)
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

    def test_perfect_yahtzee_score(self):
        pyhtzee = Pyhtzee(rule=Rule.YAHTZEE)
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
        self.assertEqual(pyhtzee.get_total_score(), 1480)
        self.assertTrue(pyhtzee.is_finished())

    def test_perfect_yahztee_score_with_yatzy_rules(self):
        pyhtzee = Pyhtzee(rule=Rule.YATZY)
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
        pyhtzee.dice = [6, 6, 6, 5, 5]
        pyhtzee.take_action(category_to_action_map[Category.FULL_HOUSE])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.SMALL_STRAIGHT])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.LARGE_STRAIGHT])
        pyhtzee.dice = [6, 6, 6, 6, 6]
        pyhtzee.take_action(category_to_action_map[Category.CHANCE])
        self.assertEqual(pyhtzee.get_total_score(), 305)
        self.assertTrue(pyhtzee.is_finished())
