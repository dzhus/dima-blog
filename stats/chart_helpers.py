"""
Helper functions used in `views.py`
"""

import time
import datetime

def fit_to_unit(data):
    """
    Shift and rescale `data` to fit unit interval.

    >>> rescale_x([5, 10, 15])
    [0.0, 0.5, 1.0]
    """
    head = data[0]
    data = map(lambda x: x - head, data)
    tail = data[-1:][0]
    return map(lambda x: x/float(tail), data)

def make_uniform_labels(data):
    return [1, len(data)]

def make_date_labels(objects, date_field, date_format='%Y-%m'):
    dates = map(lambda d: d.__dict__[date_field], objects)
    return map(lambda date: date.strftime(date_format), dates)

def make_pool_labels(pool_data):
    return ['', pool_data[-1:][0]]

def make_year_labels(years, yearly_data, format='%d (%s)'):
    """
    Combine years with respective yearly data and return list of labels.

    >>> make_year_labels([2005, 2006], [18, 29])
    ['2005 (18)', '2006 (29)']
    >>> make_year_labels([2006, 2007], ['good', 'bad'], '%d was %s')
    ['2006 was good', '2007 was bad']
    """
    return [format % (y, c) for (y, c) in zip(years, yearly_data)]

def date_to_epoch(date):
    """
    Convert datetime to Epoch seconds.
    """
    return time.mktime(date.timetuple())

# TODO Use implementation from standard django template tags
def group_by_year(object_list, date_field):
    """
    Return dictionary of objects grouped by years of creation.
    """
    groups = dict()
    for obj in object_list:
        key = obj.__dict__[date_field].year
        if key not in groups:
            groups[key] = list()
        groups[key].append(obj)
    return groups
