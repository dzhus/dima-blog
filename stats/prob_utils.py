# -*- coding: utf-8 -*-
#
# Description
# ===========
#
# This module contains several generic procedures which return
# discrete cumulative distribution functions (CDF) for sets of
# measurable objects.


def raw_prob_function(object_list):
    """
    Return generator for total **length of objects** in [0:n]-slice of
    `object_list` for every n from 0 to `len(object_list)`.

    Objects in `object_list` must be measurable in sense of `len()`.

    Consider each object to be contributing to the shared pool P of
    contents, with each contribution equal to the measure of
    respective object. Contributions are ordered. This function yeilds
    an overall size of the pool after each contribution.

    The pool P equipped with the relation *contributed earlier than*
    is a partially ordered set. Note that the exact nature of object
    contents (and thus elements of P) does not matter.
    
    If all objects have nonnegative measure, so that P size is
    monotonically increasing with each contribution, this function
    produces a generator for values of the CDF of random element in P.
    Let L be the length of object list and F(n) the n-th yeilded
    value. Let M=F(L) and G(n)=F(n)/M. Then for n<L, G(n) is the
    probability that a random element of P was added to the pool
    before n-th contribution. Element here is to be understood in
    sense of any subset of contribution. Elements within one
    contribution are indistinguishable.

    Suppose object list consists of objects A, B, C which have
    measures 1, 2, 3. Then this function will yield 0, 1, 3, 6.

    Practical example follows.

    >>> a, b, c = 'intro', 'long content', 'fin'
    >>> r = raw_prob_function([a, b, c])
    >>> [x for x in r]
    [0, 5, 17, 20]

        -- Pool size --->
        [ 'intro'(5) ], |P|=5
        [ 'intro'(5) ][ 'long content'(12) ], |P|=17
        [ 'intro'(5) ][ 'long content'(12) ][ 'fin'(3) ], |P|=20
    
    In this example, M is equal to 20. G(2)=5/20 means that there is a
    1/4 probability that a random element (which is a character in
    this case) of P was added before second contribution. P after last
    contribution is 'introlong contentfin'.

    Combined with the information about timespans between consequent
    contribution, it's possible to examine how the pool grew over the
    time. Consider objects being blog posts, measured by their textual
    length, with P being all text ever posted to the blog. Plotting P
    sizes produced by `raw_prob_function` with respective posting (or
    contribution in our terms) dates used for *X* axis values, you may
    see how the blog grew with years. Using natural numbers for *X*
    values will produce **blog size after n posts** plot.
    """
    total_size = 0
    yield total_size
    for obj in object_list:
        total_size += len(obj)
        yield total_size

if __name__ == "__main__":
    import doctest
    doctest.testmod()
