import inspect

def reduce_by_predicate(iterable, predicate):
    """
    Test if predicate is true for all items of iterable.
    """
    return reduce(lambda x, y: x and predicate(y), iterable, True)

def all_are_instances(iterable, cl):
    """
    Test if all elements of iterable are instances of cl.
    """
    return reduce_by_predicate(iterable, lambda x: isinstance(x, cl))

class ExpressionPart:
    pass

class Repr(str, ExpressionPart):
    def __new__(cl, repr, *args, **keywords):
        return str.__new__(cl, repr)
    
class ReprFunction(Repr):
    """
    A class for functions which also have human-readable
    representation
    """
    def __init__(self, repr, fun, arity=None, priority=0):
        if not callable(fun):
            raise TypeError('Function must be callable')
        else:
            self._function = fun

        if arity is None:
            try:
                arity = len(inspect.getargspec(c)[0])
            except:
                raise StandardError('Arity information is unavailable')

        if not isinstance(arity, int):
            raise TypeError('Arity should be integer number')
        else:
            self.arity = arity

        self.priority = priority

    def __call__(self, *args, **keywords):
        return self._function(*args, **keywords)

class ReprArgument(ReprFunction):
    def __new__(cl, repr, value):
        return ReprFunction.__new__(cl, repr)

    def __init__(self, repr, value):
        self._function = lambda: value
        self.arity = self.priority = 0

class ExpressionArityError(StandardError):
    pass

class ExpressionTypeError(StandardError):
    pass

class ReprExpression():
    """
    Mathematical expression which knows how to print and eval itself.
    """
    def __traverse_expression(self, items, wrapper):
        """
        Form an expression using given items.

        Nested function calls are transformed into nested Expression
        subinstances.
        """
        if not all_are_instances(items, ExpressionPart):
            raise ExpressionTypeError('All items items must be ExpressionPart instances')

        head = items[0]
        
        if isinstance(head, ReprFunction):
            # Expression is a single function application
            if all_are_instances(items[1:], ReprArgument):
                if len(items) == head.arity + 1:
                    return items
                else:
                    raise ExpressionArityError('Wrong argument count')
            # Expression contains nested function calls
            else:
                try:
                    res = [head]
                    # Include nested expression
                    res.append(ReprExpression(items[1:(len(items) - head.arity + 1)],
                                              wrapper, head.priority))
                    res += items[(len(items) - head.arity + 1):]
                    return res
                except IndexError:
                    raise ExpressionArity('Not enough arguments for %s' % head)
        # Expression is a single argument
        elif isinstance(head, ReprArgument) and len(items) == 1:
            return items
        else:
            raise ExpressionTypeError('Unknown ExpressionPart')
    
    def __init__(self, items, wrapper='(%s)', enclosing_priority=0):
        self.__expr = self.__traverse_expression(items, wrapper=wrapper)

        head = items[0]
        self.__str_wrapper = enclosing_priority > head.priority and wrapper % '%s' \
                             or '%s'
        
    def __getitem__(self, key):
        return self.__expr[key]
    
    def __call__(self):
        """
        Evaluate expression.
        """
        return self[0](*map(apply, self[1:]))

    def __str__(self):
        """
        Print expression in infix form.
        """
        return self.__str_wrapper % (str(self[0]) % tuple(map(str, self[1:])))
    
class ReprEquation():
    """
    Wrap Expression
    """
    def __init__(self, items, priority_wrapper='(%s)', equal_wrapper='%s=%s'):
        self.__expression = ReprExpression(items, wrapper=priority_wrapper)
        self.__lvalue = self.__expression()
        self.equal_wrapper = equal_wrapper

    def __str__(self):
        return self.equal_wrapper % (str(self.__expression), str(self.__lvalue))
