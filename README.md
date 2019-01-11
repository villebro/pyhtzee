[![Build Status](https://travis-ci.com/villebro/pyhtzee.svg?branch=master)](https://travis-ci.com/villebro/pyhtzee)
[![codecov](https://codecov.io/gh/villebro/pyhtzee/branch/master/graph/badge.svg)](https://codecov.io/gh/villebro/pyhtzee)
[![Requirements Status](https://requires.io/github/villebro/pyhtzee/requirements.svg?branch=master)](https://requires.io/github/villebro/pyhtzee/requirements/?branch=master)
[![PyPI version](https://img.shields.io/pypi/v/pyhtzee.svg)](https://badge.fury.io/py/pyhtzee)
[![PyPI](https://img.shields.io/pypi/pyversions/pyhtzee.svg)](https://www.python.org/downloads/)
# pyhtzee #

Yahtzee game engine supporting regular Yahtzee rules (maximum 1480), Joker rules 
(maximum 1575) and Yatzy aka. Scandinavian Yahtzee rules (maximum 305). Example code:

```python
from pyhtzee import Pyhtzee
from pyhtzee.classes import Category, Rule
from pyhtzee.utils import category_to_action_map, dice_roll_to_action_map

pyhtzee = Pyhtzee(rule=Rule.FREE_CHOICE_JOKER)
print(pyhtzee.dice)
```

This shows the dice:

```
[2, 5, 6, 1, 6]
```

Next reroll dice 1, 2 and 5:

```python
action = dice_roll_to_action_map[(True, True, False, False, True)]
pyhtzee.take_action(action)
print(pyhtzee.dice)
```

Now we have two pairs:

```
[4, 6, 6, 1, 1]
```

Let's reroll just the first die to see if we can get a full house:

```python
action = dice_roll_to_action_map[(True, False, False, False, False)]
pyhtzee.take_action(action)
print(pyhtzee.dice)
```

Bingo!

```
[6, 6, 6, 1, 1]
```

Now let's choose the action for full house and check the scorecard:

```python
action = category_to_action_map[Category.FULL_HOUSE]
reward = pyhtzee.take_action(action)
print(f'Reward: {reward}, Scorecard: {pyhtzee.scores}')
```

This shows that we got a reward of 25, which can be confirmed in the scorecard:

```
Reward: 25, Scorecard: {<Category.FULL_HOUSE: 8>: 25}
```

## Developers guide ##

Pipenv is recommended for setting up a development environment. Prior to installing
`pipenv`, creating a `.env` file with the following contents is recommended:

```
PYTHONPATH=.
```

To install pipenv and the required dependencies run the following commands:

```bash
pip install pipenv
pipenv install -r requirements.txt
pipenv shell
```

### Updating dependencies ###

`requirements.txt` is dynamically generated using `pip-compile`. To regenerate the
`requirements.txt`file run the following command:

```bash
pip-compile -U --output-file requirements.txt setup.py requirements-dev.in
```
