# -*- coding: utf-8 -*-

import time
import datetime

from pygooglechart import XYLineChart
from pygooglechart import PieChart2D
from pygooglechart import Axis

from django.shortcuts import render_to_response

from ws.blog.views import make_filter_kwargs

from prob_utils import raw_prob_function

def date_to_epoch(date):
    """
    Convert datetime to Epoch seconds.
    """
    return time.mktime(date.timetuple())

def make_pool_chart(object_list, width, height, x_values):
    chart = XYLineChart(width, height)
    chart.add_data(x_values)
    
    # Overall object pool size after every addition
    r = raw_prob_function(object_list)
    chart.add_data([y for y in r])
    return chart

def make_pool_date_chart(object_list, width, height, date_field='add_date',
                         labels=True, label_format='%Y-%m', color=None):
    """
    Return a chart of probability function for given objects with
    length and datetime field named as specified in `date_field`
    string argument.

    `width` and `height` are integers with their multiple being less
    than 300000.
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
    
    if not color is None:
        chart.set_colours([color])

    return chart

def make_pool_uniform_chart(object_list, width, height,
                            labels=True, color=None):
    """
    The same as `make_pool_date_chart`, but without any regard to
    objects creation date, so that pool sizes are uniformly
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
    Return dictionary of objects grouped by years
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
    """
    chart = PieChart2D(width, height)

    # Enforce sorting by keys
    sorted_keys = groups.keys()
    sorted_keys.sort()

    chart.add_data([groups[k] for k in sorted_keys])

    if labels:
        chart.set_pie_labels(map(str, sorted_keys))

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
    pie_dict = dict_transform_values(group_by_year(object_list), len)
    chart = make_piechart(pie_dict, width, height)
    
    return chart

def make_l_piechart(object_list, width, height,
                    labels=True, colors=None):
    pie_dict = dict_transform_values(group_by_year(object_list),
                                     lambda objects: sum(map(lambda object: len(object), objects)))
    chart = make_piechart(pie_dict, width, height)

    return chart
        
def queryset_stats(request, queryset, template_name,
                   width=600, height=300, color=None):
    entry_list = queryset.filter(**make_filter_kwargs(request))

    # Create probability chart
    date_chart = make_pool_date_chart(entry_list, width, height, color=color)
    uni_chart = make_pool_uniform_chart(entry_list, width, height, color=color)

    context = {'date_chart': date_chart,
               'uni_chart': uni_chart,
               'uni_pie': make_q_piechart(entry_list, width*2/3, height),
               # How cute, a date pie :-)
               'date_pie': make_l_piechart(entry_list, width*2/3, height)}
    
    return render_to_response(template_name, context)

