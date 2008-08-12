# encoding: utf-8

from random import randrange, seed
from md5 import md5
import time

class Captcha:
    def __init__(self, mask=[(0,10), u'+*', (0,10), u'+-*', (0,10)]):
        self.expression = ''
        self.result = 0
	seed(time.time())
        for part in mask:
            if isinstance(part, tuple):
                self.expression += str(randrange(part[0], part[1]))
            else:
                self.expression += part[randrange(0, len(part))]
        self.result = eval(self.expression)
        self.expression = self.expression.replace("*", u"×")
        self.hash = md5(str(self.result)).hexdigest()
