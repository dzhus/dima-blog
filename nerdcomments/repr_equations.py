"""
Description
===========

This module introduces several classes aimed to provide means of
constructing, evaluating and printing of arbitary (mathematical)
expressions:

- `ReprFunction`

- `ReprArgument`

- `ReprExpression`

- `ReprEquation`

Why Do I Use Infix Notation
===========================

KISS! This is merely a helper module to construct CAPTCHAs :-)

List of things to be done
========================

- Warn about wrong number of conversion specifiers in
  `ReprFunction()` and `ReprExpression()`

Examples
========

See how to work with this module in `examples.txt`. See also
real-world example in `nerdcaptcha.py`.
"""

import inspect

def true_for_all(iterable, predicate):
    """
    Test if predicate is true for all items of iterable.
    
    >>> true_for_all([1, 3, 1771], lambda x: x % 2 == 1)
    True
    """
    return reduce(lambda x, y: x and predicate(y), iterable, True)

def all_are_instances(iterable, cl):
    """
    Test if all elements of iterable are instances of cl.
    
    >>> all_are_instances([1, 2, 3], int)
    True
    >>> all_are_instances([-5, -6, 'foo'], int)
    False
    >>> all_are_instances([ValueError(), AssertionError()], BaseException)
    True
    """
    return true_for_all(iterable, lambda x: isinstance(x, cl))

class ExpressionPart:
    pass

class Repr(str, ExpressionPart):
    def __new__(cl, repr, *args, **keywords):
        return str.__new__(cl, repr)
    
class ReprFunction(Repr):
    
    """
    Loosely mimics functions and strings.

    Instances of this class are primarly used when constructing
    `ReprExpression` or `ReprEquation` objects.
    """
    
    def __init__(self, repr, fun, arity=None, priority=0):
        """
        Construct a new ReprFunction instance which is printed using
        `repr` string and acts like `fun` function when applied to
        argument(s).
        
        `repr` must contain ``%s`` conversion specifiers in amount
        equal to function arity, which is specified by `arity` integer
        argument.

        Variadic functions are not implemented.

        If `arity` is ``None``, then an attempt to get arity
        information via introspection is performed using `inspect`
        module.

        >>> r = ReprFunction('(add1 %s)', lambda x: x + 1)
        >>> # Hey, your parentheses are wrong. Wait… OH SHI~
        >>> r(5)
        6
        >>> print r % -100
        (add1 -100)
        
        You have to manually set arity for builtins, because `inspect`
        can't handle them.
        
        >>> r = ReprFunction('[%s]', round, 1)
        >>> print r
        [%s]
        >>> r(19.89)
        20.0
        >>> r(31.337) == round(31.337)
        True
        >>> print r % 31.337
        [31.337]

        >>> p = ReprFunction('%s^%s', pow, 2)
        >>> print p
        %s^%s
        >>> p(2, 5) == pow(2, 5)
        True
        >>> p(3, 3)
        27
        >>> print p % (4, 2)
        4^2
    
        `priority` is an integer number used only to properly *print*
        nested function calls in `ReprExpression` class. You'll need
        to properly set this option for binary operations, so that
        division has higher priority than addition etc.
        """
        if not callable(fun):
            raise TypeError('Function must be callable')
        else:
            self._function = fun

        if arity is None:
            try:
                arity = len(inspect.getargspec(fun)[0])
            except:
                raise StandardError('Arity information is unavailable')

        if not isinstance(arity, int):
            raise TypeError('Arity must be integer')
        else:
            self.arity = arity

        self.priority = priority

    def __call__(self, *args, **keywords):
        return self._function(*args, **keywords)

class ReprArgument(ReprFunction):
    
    """
    Constant flavor of ReprFunction.

    *Call* it with no arguments to get its value.

    Instances of this class are primarly used when constructing
    `ReprExpression` or `ReprEquation` objects.
    """
    
    def __new__(cl, repr, value):
        return ReprFunction.__new__(cl, repr)

    def __init__(self, repr, value):
        """
        Construct new ReprArgument instance.
        
        `repr` is a string with no conversion specifiers used for
        printing. `value` is any valid value this function evaluates
        to.

        >>> f = ReprArgument('four', 4)
        >>> print f
        four
        >>> f
        'four'
        >>> f()
        4
        """
        self._function = lambda: value
        self.arity = self.priority = 0

class ExpressionArityError(StandardError):
    pass

class ExpressionTypeError(StandardError):
    pass

class ReprExpression():
    
    """
    Mathematical expression which can be printed and evaluated.

    To get `ReprExpression` value, call it with no arguments. Use
    standard ways of printing, like `print`.
    """
    
    def __traverse_expression(self, items, wrapper):
        """
        Form an expression using given items.

        Nested function calls are transformed into nested Expression
        subinstances.
        """
        head = items[0]
        
        if isinstance(head, ReprFunction):
            # Expression is a single function application
            # (case: [+, 5, 5])
            if all_are_instances(items[1:], ReprArgument):
                if len(items) == head.arity + 1:
                    return items
                else:
                    raise ExpressionArityError('Wrong argument count')
            # Expression contains nested function calls
            # (case: [+, *, 5, 3, 2])
            else:
                try:
                    res = [head]
                    # Include nested expression
                    res.append(ReprExpression(items[1:(len(items) - head.arity + 1)],
                                              wrapper, head.priority))
                    res += items[(len(items) - head.arity + 1):]
                    return res
                # Case: [+, *, 5, 3]
                except IndexError:
                    raise ExpressionArity('Not enough arguments for %s' % head)
        # Expression is a single argument
        elif isinstance(head, ReprArgument) and len(items) == 1:
            return items
        else:
            raise ExpressionTypeError('Unknown ExpressionPart')
    
    def __init__(self, items, wrapper='(%s)', enclosing_priority=0):
        """
        Construct new ReprExpression from `items`.

        `items` must be a list of `ExpressionPart` instances. `items`
        ordering must follow standard infix notation with
        `ReprFunction` instances coming first, being followed by
        matching number of `ReprArgument` objects. If arity of
        functions does not match, `ExpressionArityError` exception is
        raised.

        `wrapper` is a string with one ``%s`` specifier which used to
        format expression when it occurs within another one which has
        higher priority, given by `enclosing_priority`. This string is
        set to ``(%s)`` by default, but you may change it.

        Setting `wrapper` and `enclosing_priority` is not needed to
        create new `ReprExpression` class.
        """
        if not all_are_instances(items, ExpressionPart):
            raise ExpressionTypeError('All items must be ExpressionPart instances')
        
        self.__expr = self.__traverse_expression(items, wrapper=wrapper)

        head = items[0]
        self.__str_wrapper = enclosing_priority > head.priority and wrapper % '%s' \
                             or '%s'
        
    def __getitem__(self, key):
        return self.__expr[key]
    
    def __call__(self):
        """Evaluate expression."""
        return self[0](*map(apply, self[1:]))

    def __str__(self):
        """Print expression in *infix* form."""
        return self.__str_wrapper % (str(self[0]) % tuple(map(str, self[1:])))
    
class ReprEquation():
    
    """
    `ReprEquation` is a thin wrapper for `ReprExpression`, which uses
    both expression and its *value* when printing.
    """
    
    def __init__(self, items, equal_wrapper='%s=%s', priority_wrapper='(%s)'):
        """
        Constructs `ReprEquation` instance using `items` the same way
        `ReprExpression` class constructor does.

        `equal_wrapper` is a string with two ``%s`` specifiers
        substituted for expression and its value when printing.

        `priority_wrapper` has the same meaning as in
        `ReprExpression`.

        >>> a = ReprFunction('absolute value of %s', abs, 1)
        >>> f = ReprArgument('minus four', -4)
        >>> print ReprEquation([a, f])
        absolute value of minus four=4
        >>> print ReprEquation([a, f], '%s is actually equal to %s')
        absolute value of minus four is actually equal to 4
        """
        self.__expression = ReprExpression(items, wrapper=priority_wrapper)
        self.__lvalue = self.__expression()
        self.equal_wrapper = equal_wrapper

    def __str__(self):
        return self.equal_wrapper % (str(self.__expression), str(self.__lvalue))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
