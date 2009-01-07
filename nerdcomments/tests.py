#!/usr/bin/env python

import doctest
import repr_equations
import repr_functions

doctest.testmod(repr_equations)
doctest.testmod(repr_functions)
doctest.testfile("examples.txt")
