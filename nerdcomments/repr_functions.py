# encoding: utf-8

# Miscellaneous functions which make use of repr_equations module

import operator
from random import randrange, seed
from time import time

from repr_equations import ReprFunction, ReprArgument

# … = ReprFunction(repr, fun, arity, priority)
add = ReprFunction('%s+%s', operator.add, 2, 0)
mul = ReprFunction('%s∙%s', operator.mul, 2, 1)
sub = ReprFunction('%s−%s', operator.sub, 2, 0)
div = ReprFunction('%s÷%s', operator.div, 2, 1)
rabs = ReprFunction('%s', operator.abs, 1, 0)

def random_repr_number(a, b=None):
    """
    Generate a random number and put it in ReprArgument.
    """
    seed(time())
    n = randrange(a, b)
    return ReprArgument(n, n)
