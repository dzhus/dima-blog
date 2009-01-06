# -*- coding: utf-8 -*-
#
# Description
# ===========
#
# This module provides several functions which use pygooglechart API
# to produce charts containing certain statistics about sets of
# objects.
#
# How to use
# ==========
#
# You'll want to use the following 4 charting functions provided by
# this module:
#
# 1. `make_pool_date_chart()`
# 
# 2. `make_pool_uniform_chart()`
# 
# 3. `make_q_piechart()`
# 
# 4. `make_l_piechart()`
#
# Requirements for objects
# ========================
# 
# *All* charting functions assume the following about their arguments:
# 
# - `object_list` has `count()` method which returns total amount of
#   objects in set;
#
# - `object_list` objects are measurable in sense of `len()`;
#
# - multiply of `width` and `height` does not exceed 300 000 with each
#   dimension being less than or equal to 1000.
#
# For every charting function *but* `make_pool_uniform_chart()`, each
# object in `object_list()` must have a datetime field, named
# according to `date_field` argument of the functions. Object creation
# dates are retrieved from that field.
#
# Several functions imply more requirements for `object_list`.

import time
import datetime

from pygooglechart import XYLineChart
from pygooglechart import PieChart2D
from pygooglechart import Axis

from prob_utils import raw_prob_function

def date_to_epoch(date):
    """
    Convert datetime to Epoch seconds.
    """
    return time.mktime(date.timetuple())

def make_pool_chart(object_list, width, height, x_values):
    """
    Return object pool size graph with `x_values` used for X axis
    values.
    """
    chart = XYLineChart(width, height)
    chart.add_data(x_values)
    
    r = raw_prob_function(object_list)
    chart.add_data([y for y in r])
    return chart

def make_pool_date_chart(object_list, width, height, date_field='add_date',
                         labels=True, label_format='%Y-%m', color=None):
    """
    Return object pool size graph with objects distributed along X
    axis using their creation dates.
    """
    chart =  make_pool_chart(object_list, width, height,
                             map(lambda o: date_to_epoch(o.__dict__[date_field]),
                                 object_list))

    if labels:
        [first_date, last_date] = map(lambda x:datetime.datetime.fromtimestamp(int(x)),
                                      chart.data_x_range())
        half_date = first_date + (last_date - first_date)/2

        chart.set_axis_labels(Axis.LEFT, ['', chart.data[1][-1:][0]])
        chart.set_axis_labels(Axis.BOTTOM, map(lambda d: d.strftime(label_format),
                                               [first_date, half_date, last_date]))
    
    if color is not None:
        chart.set_colours([color])

    return chart

def make_pool_uniform_chart(object_list, width, height,
                            labels=True, color=None):
    """
    The same as `make_pool_date_chart`, but without any regard to
    objects creation dates, so that pool sizes are uniformly
    distributed along *X* axis.
    """
    chart =  make_pool_chart(object_list, width, height,
                             range(len(object_list)))

    if labels:
        chart.set_axis_labels(Axis.LEFT, ['', chart.data[1][-1:][0]])
        chart.set_axis_labels(Axis.BOTTOM, ['1', len(object_list)/2, len(object_list)])
    
    if not color is None:
        chart.set_colours([color])

    return chart

# TODO Use implementation from standard django template tags
def group_by_year(object_list, date_field='add_date', ):
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

def make_piechart(groups, width, height,
                  labels=True, colors=None):
    """
    Make piechart from dictionary.

    Dictionary items set pie chart data, while dictionary keys are
    used for labels.

    `colors` is a list of colors for each pie piece.
    """
    chart = PieChart2D(width, height)

    # Enforce sorting by keys
    sorted_keys = groups.keys()
    sorted_keys.sort()

    chart.add_data([groups[k] for k in sorted_keys])

    if labels:
        chart.set_pie_labels(map(lambda y:str(y)+' '+str(groups[y]), sorted_keys))

    if not colors is None:
        chart.set_colours(colors)

    return chart

def dict_transform_values(orig_dict, transform):
    """
    Apply `transform` to every value of `orig_dict` and return new
    dictionary.

    Keys are unchanged.
    
    >>> dict_transform_values({'a': 5.1, 'b': 6.31}, int)
    {'a': 5, 'b': 26}
    """
    new_dict = dict()
    for (k, i) in orig_dict.items():
        new_dict[k] = transform(i)
    return new_dict

def make_q_piechart(object_list, width, height,
                    labels=True, colors=None):
    """
    Group objects by years of creation and return PieChart2D with
    amount of objects created each year.
    """
    pie_dict = dict_transform_values(group_by_year(object_list), len)
    chart = make_piechart(pie_dict, width, height)
    
    return chart

def make_l_piechart(object_list, width, height,
                    labels=True, colors=None):
    """
    Group objects by years of creation and return PieChart2D with
    total measure of objects created each year.
    """
    pie_dict = dict_transform_values(group_by_year(object_list),
                                     lambda objects: sum(map(lambda object: len(object), objects)))
    chart = make_piechart(pie_dict, width, height)

    return chart