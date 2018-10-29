from random import Random
from typing import Dict

from pyhtzee.classes import Category, Rule
from pyhtzee.utils import (
    action_to_category_map,
    action_to_dice_roll_map,
    CATEGORY_ACTION_OFFSET,
    category_to_action_map,
    category_to_scoring_function_map,
    is_joker_category,
    is_upper_section_category,
)
from pyhtzee.scoring import CONSTANT_SCORES, score_upper_section_bonus


class State:
    def __init__(self, seed: int = None, rule: Rule = None):
        self.scores: Dict[Category, int] = {}
        self.rule = rule if rule else Rule.FREE_CHOICE_JOKER

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
            return 0

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
        if self.is_yahtzee() and self.scores.get(Category.YAHTZEE, 0) > 0:
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
        if self.is_eligible_for_yahtzee_bonus() and (
                is_upper_section_category(category) or
                self.rule == Rule.FREE_CHOICE_JOKER):
            scores[Category.YAHTZEE_BONUS] = CONSTANT_SCORES[Category.YAHTZEE_BONUS]

        # Joker rule
        if self.is_eligible_for_yahtzee_bonus() and \
                self.rule == Rule.FREE_CHOICE_JOKER and \
                is_joker_category(category):
            scores[category] = CONSTANT_SCORES[category]

        # Regular rule
        else:
            scoring_function = category_to_scoring_function_map[category]
            scores[category] = scoring_function(self.dice)

        # upper section bonus
        if is_upper_section_category(category):
            upper_scores = [v for k, v in self.scores.items()
                            if int(k) <= int(Category.SIXES)]
            upper_scores.append(category)
            if len(upper_scores) == 6:
                bonus_reward = score_upper_section_bonus(sum(upper_scores))
                scores[Category.UPPER_SECTION_BONUS] = bonus_reward

        return scores
