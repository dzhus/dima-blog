# -*- coding: utf-8 -*-

import time

from pygooglechart import XYLineChart
from pygooglechart import Axis

from django.shortcuts import render_to_response
from django.conf import settings

from ws.blog.models import Entry
from ws.blog.views import make_filter_kwargs

WIDTH=500
HEIGHT=50

def date_to_epoch(date):
    """
    Convert datetime to Epoch seconds.
    """
    return time.mktime(date.timetuple())

def make_model_prob_chart(object_list, width, height):
    """
    Return a chart of «probability function» for given objects of any
    model which has length and add_date field.
    """
    chart = XYLineChart(width, height)

    # Dates when objects were created, in seconds since Epoch
    dates = [date_to_epoch(o.add_date) for o in object_list]
    chart.add_data(dates)
    
    # Overall object pool size after every addition
    r = raw_prob_function([len(o) for o in object_list])
    chart.add_data([x for x in r])
    
    return chart

def raw_prob_function(list):
    x = 0
    yield x
    for entry in list:
        x += entry
        yield x

def blog_stats(request, queryset, template_name="blog_stats.html",
               width=600, height=300, label_format="%Y-%m"):
    def make_label(date):
        return date.strftime(label_format)
    
    entry_list = queryset.filter(**make_filter_kwargs(request))

    # Create probability chart
    chart = make_model_prob_chart(entry_list, width, height)
    
    chart.set_colours(['666666'])

    # Set chart labels

    first_date = entry_list[0].add_date
    last_date = entry_list.reverse()[0].add_date
    
    chart.set_axis_labels(Axis.LEFT, ['', chart.data[1][-1:][0]])
    chart.set_axis_labels(Axis.BOTTOM, map(make_label,
                                           [first_date, last_date]))
    chart.set_title('Рост количества информации в бложике с течением времени')
    
    context = {'chart_url': chart.get_url(),
               'chart_width': width,
               'chart_height': height}
    
    return render_to_response(template_name, context)
