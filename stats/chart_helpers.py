"""
Helper functions used in `views.py`
"""

import time
import datetime

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
