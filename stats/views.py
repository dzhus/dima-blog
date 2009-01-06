# -*- coding: utf-8 -*-

import time

from pygooglechart import XYLineChart
from pygooglechart import Axis

from django.shortcuts import render_to_response

from ws.blog.models import Entry
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
    def make_date_label(date):
        return date.strftime(label_format)
    
    chart =  make_pool_chart(object_list, width, height,
                             map(lambda o: date_to_epoch(o.__dict__[date_field]),
                                 object_list))

    if labels:
        first_object = object_list[0]
        last_object = object_list.reverse()[0]
        
        first_date = first_object.add_date
        last_date = last_object.add_date
        
        chart.set_axis_labels(Axis.LEFT, ['', chart.data[1][-1:][0]])
        chart.set_axis_labels(Axis.BOTTOM, map(make_date_label,
                                               [first_date, last_date]))
        chart.set_axis_labels(Axis.BOTTOM, ['1', len(object_list)])
    
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

def queryset_stats(request, queryset, template_name,
                   width=600, height=300, color=None):
    entry_list = queryset.filter(**make_filter_kwargs(request))

    # Create probability chart
    date_chart = make_pool_date_chart(entry_list, width, height, color=color)
    uni_chart = make_pool_uniform_chart(entry_list, width, height, color=color)

    context = {'date_chart': date_chart,
               'uni_chart': uni_chart}
    
    return render_to_response(template_name, context)
