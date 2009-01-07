# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

from ws.blog.views import make_filter_kwargs

from chart_helpers import make_pool_date_chart, make_pool_uniform_chart
from chart_helpers import make_q_piechart, make_l_piechart
        
def queryset_stats(request, queryset, template_name,
                   width=500, height=325, graph_color=None, pie_colors=None):
    """
    Provide charts with statistics for objects in `queryset`.

    `graph_color` is a string which sets color for object pool graphs.
    `pie_colors` argument sets colors used for pie charts. See
    `chart_helpers.py` docs for more information about colors.

    Integer `width` and `height` are chart image dimensions.
    
    Context:
        uni_chart
            Object pool size graph with object numbers used for X axis values
        date_chart
            Object pool size graph with creation dates used for X
        quantity_pie
            Pie chart with amount of objects created each year
        measure_pie
            Pie chart with total measures of objects created each year

    To get image URLs for charts, `get_url` method should be used in
    the template (like `uni_chart.get_url`), as well as their `width`
    and `height` fields.
    """
    # Create probability chart
    date_chart = make_pool_date_chart(queryset, width, height, color=graph_color)
    uni_chart = make_pool_uniform_chart(queryset, width, height, color=graph_color)

    context = {'date_chart': date_chart,
               'uni_chart': uni_chart,
               'quantity_pie': make_q_piechart(queryset, width, height, colors=pie_colors),
               'measure_pie': make_l_piechart(queryset, width, height, colors=pie_colors)}
    
    return render_to_response(template_name, context)

