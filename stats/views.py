# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

from prob_utils import pool_size_function
from chart_helpers import date_to_epoch, group_by_year, make_year_labels, fit_to_unit

def queryset_stats(request, queryset, template_name, date_field='add_date'):
    """
    Context:
        pool_data
            Object pool size data
        pool_x_range
            Uniformly distributed numbers, rescaled
        pool_x_dates
            Creation dates of pool objects, rescaled
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

    # Rescale pool size data (can't rely on Google Charts)
    pool_data = [x for x in pool_size_function(queryset)]
    pool_data = map(lambda x: float(x)/pool_data[-1:][0], pool_data)

    pool_x_range = fit_to_unit(range(count))
    pool_x_dates = fit_to_unit(map(lambda o: date_to_epoch(o.__dict__[date_field]),
                                   queryset))

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
                                               'yearly_count',
                                               'yearly_measure',
                                               'yc_labels',
                                               'ym_labels']])
    
    return render_to_response(template_name, context)

