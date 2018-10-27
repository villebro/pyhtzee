[![Build Status](https://travis-ci.com/villebro/pyhtzee.svg?branch=master)](https://travis-ci.com/villebro/pyhtzee)
[![codecov](https://codecov.io/gh/villebro/pyhtzee/branch/master/graph/badge.svg)](https://codecov.io/gh/villebro/pyhtzee)
[![Requirements Status](https://requires.io/github/villebro/pyhtzee/requirements.svg?branch=master)](https://requires.io/github/villebro/pyhtzee/requirements/?branch=master)
[![PyPI version](https://img.shields.io/pypi/v/pyhtzee.svg)](https://badge.fury.io/py/pyhtzee)
[![PyPI](https://img.shields.io/pypi/pyversions/pyhtzee.svg)](https://www.python.org/downloads/)
# pyhtzee #

Yahtzee game engine. Currently only supports a loose interpretation of the Free 
Choice Joker Rule, where an extra yahtzee cannot be substituted for a straight and 
upper section usage isn't enforced for extra yahtzees. The maximum score is 1505, as 
opposed to 1375 using traditional Joker Rules.

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
