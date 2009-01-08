# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

from prob_utils import pool_size_function
from chart_helpers import *

# TODO Reorganize this view
def queryset_stats(request, queryset, template_name, date_field='add_date'):
    """
    Context:
        pool_data
            Object pool size data
        pool_x_range
            Uniformly distributed numbers, rescaled
        pool_range_xlabels
            X axis labels with pool sizes
        pool_x_dates
            Creation dates of pool objects, rescaled
        pool_date_xlabels
            X axis labels with pool objects dates
        yearly_count
            List with numbers of objects created each year
        yc_labels
            Labels for yearly object count chart
        yearly_measure
            List with overall measures of objects created each year
        ym_labels
            Labels for yearly objects count chart
    """

    count = queryset.count()

    # Object pool size charts
    pool_data = [x for x in pool_size_function(queryset)]
    pool_size_ylabels = make_pool_labels(pool_data)
    # Rescale pool size data (can't rely on Google Charts)
    pool_data = fit_to_unit(pool_data)
    
    # Produce differently distributed values for X axis
    pool_x_range = fit_to_unit(range(count))
    pool_range_xlabels = make_uniform_labels(pool_x_range)

    pool_x_dates = fit_to_unit(map(lambda o: date_to_epoch(o.__dict__[date_field]),
                                   queryset))
    pool_date_xlabels = make_date_labels([queryset[0], queryset.reverse()[0]], date_field)

    # Pie charts with yearly data
    year_groups = group_by_year(queryset, date_field)
    years = year_groups.keys()

    # We manually sort year groups by keys
    years.sort()

    yearly_objects = [year_groups[y] for y in years]
    yearly_count = map(len, yearly_objects)
    yearly_measure = map(lambda year: sum(map(lambda object: len(object), year)), yearly_objects)

    yc_labels = make_year_labels(years, yearly_count)
    ym_labels = make_year_labels(years, yearly_measure)

    context = dict([(x, locals()[x]) for x in ['pool_data',
                                               'pool_x_range',
                                               'pool_x_dates',
                                               'pool_range_xlabels',
                                               'pool_date_xlabels',
                                               'pool_size_ylabels',
                                               'yearly_count',
                                               'yearly_measure',
                                               'yc_labels',
                                               'ym_labels']])
    
    return render_to_response(template_name, context)

