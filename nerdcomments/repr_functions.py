# -*- encoding: utf-8 -*-
"""
Description
===========

Miscellaneous functions which use of `repr_equations` module.

Provides `ReprFunction` flavors of 4 basic arithmetic operations and
absolute value function.

`random_repr_number` helper function produces random `ReprArgument`
instances.

This module uses Unicode symbols for subtraction, multiplication and
division signs. Bullet is used for multiplication instead of × because
it's easier to distinguish from x.

See also `examples.txt`.
"""

import operator
from random import randrange, seed
from time import time

from repr_equations import ReprFunction, ReprArgument

# … = ReprFunction(repr, fun, arity, priority)
add = ReprFunction('%s+%s', operator.add, 2, 0)
mul = ReprFunction('%s∙%s', operator.mul, 2, 1)
sub = ReprFunction('%s−%s', operator.sub, 2, 0)
div = ReprFunction('%s÷%s', operator.div, 2, 1)
rabs = ReprFunction('|%s|', operator.abs, 1, 0)

def random_repr_number(a, b=None):
    """
    Generate a random number return `ReprArgument` instance for it.

    `a` and `b` are the same as in `random.randrange()`.

    Current time is used for random seed.

    >>> random_repr_number(5)() in range(5)
    True
    >>> random_repr_number(5) in map(str, range(5))
    True
    """
    seed(time())
    n = randrange(a, b)
    return ReprArgument(n, n)
