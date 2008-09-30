# encoding: utf-8

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
    items = []
    for i in range(functions):
        items.append(choice(funset))
    for i in range(arguments):
        items.append(rrn(min_arg, max_arg))
    return items

class NerdCaptcha():
    """
    Mathematical CAPTCHA.
    """
    def __init__(self, items, hidden_repr='?'):
        def first_argument_index():
            """
            Return index of first ReprArgument instance.
            """
            for i in range(len(items)):
                if isinstance(items[i], ReprArgument):
                    return i

        to_hide = randrange(first_argument_index(), len(items))
        hidden = items[to_hide]
        items[to_hide] = ReprArgument(hidden_repr, hidden())

        self.equation = ReprEquation(items)
        self.token = encode_answer(str(hidden()))
        
    def __str__(self):
        return str(self.equation)
