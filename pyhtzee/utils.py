"""
Common utilities needed that make it possible to convert actions (e.g. choosing
threes on the scorecard) to categories (e.g. full house on the scorecard) and vice versa.
Similar maps are also provided for mapping dice rolling lists (e.g. reroll dice 2, 3 and
4 but keep dice 1 and 5) to and from actions and categories to scoring functions.
"""
from typing import Dict, List, Tuple

from pyhtzee.classes import Category, Rule

# Mapping from action id to permutations of rerolling of dice. Each unique combination
# of dice rolls is given a unique id, resulting in 32 unique constellations. However,
# keeping all dice is left out, as the player should then choose a category from the
# scorecard, hence there are 31 unique rerolling patterns. An offset constant is
# provided, as category actions are located after dice rolling actions.
CATEGORY_ACTION_OFFSET = 31
action_to_dice_roll_map: Dict[int, Tuple[bool, bool, bool, bool, bool]] = {}
dice_roll_to_action_map: Dict[Tuple[bool, bool, bool, bool, bool], int] = {}
for d1 in [1, 0]:
    for d2 in [1, 0]:
        for d3 in [1, 0]:
            for d4 in [1, 0]:
                for d5 in [1, 0]:
                    # make rolling all dice the first action, i.e. zero
                    key = 31 - (d5 * 2**0 + d4 * 2**1 + d3 * 2**2 + d2 * 2**3 + d1 * 2**4)
                    value = bool(d1), bool(d2), bool(d3), bool(d4), bool(d5)
                    # not rolling any dice is not a valid action
                    if key < 31:
                        action_to_dice_roll_map[key] = value
                        dice_roll_to_action_map[value] = key


# Mapping from action id to category and vice versa.
action_to_category_map: Dict[int, Category] = {}
category_to_action_map: Dict[Category, int] = {}
for i in range(15):
    category_ = Category(i)
    action_to_category_map[i + CATEGORY_ACTION_OFFSET] = category_
    category_to_action_map[category_] = i + CATEGORY_ACTION_OFFSET

# List of actionable categories e.g. for determining valid actions
actionable_categories: List[Category] = []
for category_ in Category:
    if category_ not in (Category.UPPER_SECTION_BONUS, Category.YAHTZEE_BONUS):
        actionable_categories.append(category_)


def is_upper_section_category(category: Category) -> bool:
    return True if int(category) < 6 else False


def is_joker_category(category: Category) -> bool:
    return True if category in [
        Category.FULL_HOUSE,
        Category.SMALL_STRAIGHT,
        Category.LARGE_STRAIGHT
    ] else False


def is_category_supported_by_rule(category: Category, rule: Rule) -> bool:
    if rule != Rule.YATZY and (category == Category.ONE_PAIR
                               or category == Category.TWO_PAIRS):
        return False
    return True
