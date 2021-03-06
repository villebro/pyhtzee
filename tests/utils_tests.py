from pyhtzee.utils import is_category_supported_by_rule
from pyhtzee.classes import Category, Rule
from unittest import TestCase


class UtilsTestCase(TestCase):
    def test_is_category_supported_by_rule(self):
        self.assertTrue(
            is_category_supported_by_rule(Category.ONE_PAIR, Rule.YATZY), True
        )  # noqa
        self.assertTrue(
            is_category_supported_by_rule(Category.TWO_PAIRS, Rule.YATZY), True
        )  # noqa
        self.assertFalse(
            is_category_supported_by_rule(
                Category.ONE_PAIR, Rule.YAHTZEE_FREE_CHOICE_JOKER
            ),
            False,
        )  # noqa
        self.assertFalse(
            is_category_supported_by_rule(
                Category.TWO_PAIRS, Rule.YAHTZEE_FREE_CHOICE_JOKER
            ),
            False,
        )  # noqa
        self.assertFalse(
            is_category_supported_by_rule(Category.ONE_PAIR, Rule.YAHTZEE), False
        )  # noqa
        self.assertFalse(
            is_category_supported_by_rule(Category.TWO_PAIRS, Rule.YAHTZEE), False
        )  # noqa
