#!/usr/bin/env python

import doctest
import repr_equations
import repr_functions
import nerdcaptcha

doctest.testmod(repr_equations)
doctest.testmod(repr_functions)
doctest.testfile("examples.txt")
doctest.testmod(nerdcaptcha)
