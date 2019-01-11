from random import Random
from typing import Callable, Dict, List

from pyhtzee.classes import Category, PyhtzeeException, Rule
from pyhtzee.utils import (
    action_to_category_map,
    action_to_dice_roll_map,
    CATEGORY_ACTION_OFFSET,
    category_to_action_map,
    is_joker_category,
    is_upper_section_category,
)
from pyhtzee.scoring import (
    CONSTANT_SCORES_YAHTZEE,
    score_chance,
    score_full_house,
    score_one_pair,
    score_two_pairs,
    score_large_straight,
    score_small_straight,
    score_upper_section,
    score_upper_section_bonus,
    score_x_of_a_kind,
    score_yahtzee,
)


class Pyhtzee:
    def __init__(self, seed: int = None, rule: Rule = None):
        self.scoring_functions: Dict[int, Callable[[List[int]], int]] = {}
        self.scores: Dict[Category, int] = {}
        self.rule = rule if rule else Rule.YAHTZEE_FREE_CHOICE_JOKER
        self.init_scoring_functions()

        # a game has a total of 12 rounds
        self.round = 0

        # a round consists of max 3 dice rolls + 1 action = 4. Sub-round zero is
        # reserved for two player game when a player has not yet started the round
        self.sub_round = 1

        if seed:
            self.rnd = Random(seed)
        else:
            self.rnd = Random()

        # initialize dice
        self.dice = [0, 0, 0, 0, 0]
        self.roll_dice(True, True, True, True, True)

    def roll_dice(self, d1: bool, d2: bool, d3: bool, d4: bool, d5: bool):
        dice = [d1, d2, d3, d4, d5]
        for i, die in enumerate(dice):
            if die:
                self.dice[i] = self.rnd.choice([1, 2, 3, 4, 5, 6])

    def get_possible_actions(self):
        possible_actions = []

        # determine if rerolling dice is possible; is so, add all possible permutations
        if self.sub_round < 3:
            possible_actions.extend(list(range(CATEGORY_ACTION_OFFSET)))

        # See which categories are still unused
        for category in Category:
            if not self.scores.get(category):
                action = category_to_action_map.get(category)
                # Check if the category has an action associated with it
                # (upper section bonus is automatic).
                if action:
                    possible_actions.append(action)

        return possible_actions

    def sample_action(self):
        actions = self.get_possible_actions()
        return self.rnd.sample(actions, 1)[0]

    def take_action(self, action: int) -> int:
        possible_actions = self.get_possible_actions()
        if action not in possible_actions:
            raise PyhtzeeException('Action not allowed')

        # if dice rolling action
        if action < CATEGORY_ACTION_OFFSET:
            self.sub_round += 1
            self.roll_dice(*action_to_dice_roll_map[action])
            return 0

        # all non-rolling actions lead to the sub-round
        # ending and moving to the next round
        self.round += 1
        self.sub_round = 0

        scores = self.get_action_score(action)
        for k, v in scores.items():
            old_score = self.scores.get(k, 0)
            self.scores[k] = old_score + v
        return sum(scores.values())

    def is_eligible_for_yahtzee_bonus(self):
        if self.rule != Rule.YATZY and self.is_yahtzee() and self.scores.get(Category.YAHTZEE, 0) > 0:  # noqa
            return True
        return False

    def is_yahtzee(self):
        return True if len(set(self.dice)) == 1 else False

    def is_finished(self):
        return True if self.round == 13 else False

    def get_total_score(self):
        return sum([v for v in self.scores.values()])

    def get_action_score(self, action: int) -> Dict[Category, int]:
        category = action_to_category_map[action]
        scores: Dict[Category, int] = {}

        # yahtzee bonus
        if self.is_eligible_for_yahtzee_bonus():
            scores[Category.YAHTZEE_BONUS] = CONSTANT_SCORES_YAHTZEE[Category.YAHTZEE_BONUS]  # noqa

        # Joker rule
        if self.is_yahtzee() and self.rule == Rule.YAHTZEE_FREE_CHOICE_JOKER and is_joker_category(category):  # noqa
            scores[category] = CONSTANT_SCORES_YAHTZEE[category]
        else:  # Regular rule
            scoring_function = self.scoring_functions[category]
            scores[category] = scoring_function(self.dice)

        # upper section bonus
        if is_upper_section_category(category):
            upper_scores = [v for k, v in self.scores.items()
                            if int(k) <= int(Category.SIXES)]
            upper_scores.append(category)
            if len(upper_scores) == 6:
                bonus_reward = score_upper_section_bonus(sum(upper_scores), self.rule)
                scores[Category.UPPER_SECTION_BONUS] = bonus_reward

        return scores

    def init_scoring_functions(self):
        self.scoring_functions[Category.ACES] = lambda x: score_upper_section(x, 1)
        self.scoring_functions[Category.TWOS] = lambda x: score_upper_section(x, 2)
        self.scoring_functions[Category.THREES] = lambda x: score_upper_section(x, 3)
        self.scoring_functions[Category.FOURS] = lambda x: score_upper_section(x, 4)
        self.scoring_functions[Category.FIVES] = lambda x: score_upper_section(x, 5)
        self.scoring_functions[Category.SIXES] = lambda x: score_upper_section(x, 6)
        self.scoring_functions[Category.ONE_PAIR] = lambda x: score_one_pair(x)
        self.scoring_functions[Category.TWO_PAIRS] = lambda x: score_two_pairs(x)
        self.scoring_functions[Category.THREE_OF_A_KIND] = lambda x: score_x_of_a_kind(x, 3, self.rule)  # noqa
        self.scoring_functions[Category.FOUR_OF_A_KIND] = lambda x: score_x_of_a_kind(x, 4, self.rule)  # noqa
        self.scoring_functions[Category.FULL_HOUSE] = lambda x: score_full_house(x, self.rule)  # noqa
        self.scoring_functions[Category.SMALL_STRAIGHT] = lambda x: score_small_straight(x, self.rule)  # noqa
        self.scoring_functions[Category.LARGE_STRAIGHT] = lambda x: score_large_straight(x, self.rule)  # noqa
        self.scoring_functions[Category.YAHTZEE] = lambda x: score_yahtzee(x)
        self.scoring_functions[Category.CHANCE] = lambda x: score_chance(x)
