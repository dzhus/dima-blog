"""
Helper functions used in `views.py`
"""

import datetime

def fit_to_unit(data):
    """
    Shift and rescale `data` to fit unit interval.

    >>> rescale_x([5, 10, 15])
    [0.0, 0.5, 1.0]
    """
    head = data[0]
    data = [x - head for x in data]
    tail = data[-1:][0]
    return [x/float(tail) for x in data]

def make_uniform_labels(data):
    total = len(data)
    return [1, total/4, total/2, total*3/4, total]

def make_date_labels(objects, date_field, spans=4, date_format='%Y-%m'):
    "Make X axis labels given a pair of first and last objects."
    [beg, end] = [o.__dict__[date_field] for o in objects]
    span = (end - beg) / spans
    dates = [beg + d * span for d in range(spans + 1)]
    return [d.strftime(date_format) for d in dates]

def make_pool_labels(pool_data, spans=4):
    total_pool = pool_data[-1:][0]
    span = total_pool / spans
    return [''] + [x * span for x in range(spans + 1)][1:]

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
    return int(date.strftime('%s'))

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
