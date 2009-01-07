"""
Description
===========

This module provides `NerdCaptcha()` class and several helper
functions which are used to implement CAPTCHA for Django comments
module. See also `forms.py`.
"""

from random import choice, randrange
from time import time
from md5 import md5

from repr_equations import ReprEquation, ReprArgument
from repr_functions import add, mul, sub, rabs
from repr_functions import random_repr_number as rrn

def encode_answer(answer):
    return md5(answer).hexdigest()

# CAPTCHA object state cannot be stored across requests, so this
# function is decoupled from NerdCaptcha class
def check_answer(answer, token):
    """
    Check if provided answer is correct.
    """
    return encode_answer(answer) == token

def make_random_expr_items(functions, arguments, funset=(add, sub, mul), min_arg=1, max_arg=10):
    """Return a list of random expression parts."""
    items = []
    for i in range(functions):
        items.append(choice(funset))
    for i in range(arguments):
        items.append(rrn(min_arg, max_arg))
    return items

class NerdCaptcha():
    """
    Mathematical CAPTCHA.

    `equation` is an instance of `ReprEquation` built from items
    originally provided to class constructor, with one of randomly
    chosen arguments being hidden.
        
    `token` is the rvalue of equation, encoded using `encode_answer`.

    Candidate CAPTCHA answers should be tested against `token` using
    `check_answer()` function.
    """
    def __init__(self, items, hidden_repr='?'):
        """
        Construct new `NerdCaptcha` instance.
        
        `items` are the same as in `ReprEquation` from
        `repr_equations` module.
        
        `hidden_repr` is a string used to print hidden argument.
        """
        def first_argument_index():
            """
            Return index of first ReprArgument instance.
            """
            for i in range(len(items)):
                if isinstance(items[i], ReprArgument):
                    return i

        # Choose random argument and hide it
        to_hide = randrange(first_argument_index(), len(items))
        hidden = items[to_hide]
        items[to_hide] = ReprArgument(hidden_repr, hidden())

        self.equation = ReprEquation(items)
        self.token = encode_answer(str(hidden()))
        
    def __str__(self):
        return str(self.equation)
