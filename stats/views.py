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

def make_pool_date_chart(object_list, width, height, date_field='add_date'):
    """
    Return a chart of probability function for given objects with
    length and datetime field named as specified in `date_field`
    string argument.

    `width` and `height` are integers with their multiple being less
    than 300000.
    """
    return make_pool_chart(object_list, width, height,
                           map(lambda o: date_to_epoch(o.__dict__[date_field]),
                               object_list))

def make_pool_uniform_chart(object_list, width, height):
    """
    The same as `make_pool_date_chart`, but without any regard to
    objects creation date, so that pool sizes are uniformly
    distributed along *X* axis.
    """
    return make_pool_chart(object_list, width, height,
                           range(len(object_list)))

def queryset_stats(request, queryset, template_name,
                   width=600, height=300,
                   label_format="%Y-%m", title=None, color=None):
    def make_label(date):
        return date.strftime(label_format)
    
    entry_list = queryset.filter(**make_filter_kwargs(request))

    # Create probability chart
    chart = make_pool_date_chart(entry_list, width, height)

    if not color is None:
        chart.set_colours([color])

    # Set chart labels

    first_date = entry_list[0].add_date
    last_date = entry_list.reverse()[0].add_date
    
    chart.set_axis_labels(Axis.LEFT, ['', chart.data[1][-1:][0]])
    chart.set_axis_labels(Axis.BOTTOM, map(make_label,
                                           [first_date, last_date]))
    if title:
        chart.set_title(title)
    
    context = {'chart_url': chart.get_url(),
               'chart_width': width,
               'chart_height': height}
    
    return render_to_response(template_name, context)
