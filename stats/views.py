# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

from ws.blog.views import make_filter_kwargs

from chart_helpers import make_pool_date_chart, make_pool_uniform_chart
from chart_helpers import make_q_piechart, make_l_piechart
        
def queryset_stats(request, queryset, template_name,
                   width=600, height=300, color=None):
    entry_list = queryset.filter(**make_filter_kwargs(request))

    # Create probability chart
    date_chart = make_pool_date_chart(entry_list, width, height, color=color)
    uni_chart = make_pool_uniform_chart(entry_list, width, height, color=color)

    context = {'date_chart': date_chart,
               'uni_chart': uni_chart,
               'uni_pie': make_q_piechart(entry_list, width, height),
               # How cute, a date pie :-)
               'date_pie': make_l_piechart(entry_list, width, height)}
    
    return render_to_response(template_name, context)

