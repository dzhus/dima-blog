# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

from prob_utils import pool_size_function
from chart_helpers import *
from blog.views import make_filter_kwargs

def blog_stats(request, queryset, **kwargs):
    """
    Decorate `queryset_stats` view, filtering private entries from
    `queryset` if necessary.

    Accepts the same keyword arguments as `queryset_stats`.
    """
    return queryset_stats(request, queryset.filter(**make_filter_kwargs(request)),
                          **kwargs)

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
            Labels for yearly objects total measure chart
        yd_labels
            Labels for yearly objects density bar chart
        years
            List of years which when objects were created
        density_labels
            List of object densities for every year
    """
    count = queryset.count()

    ## Object pool size charts
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

    ## Pie charts with yearly data
    year_groups = group_by_year(queryset, date_field)
    years = year_groups.keys()

    # We manually sort year groups by keys
    years.sort()

    yearly_objects = [year_groups[y] for y in years]
    yearly_count = map(len, yearly_objects)
    yearly_measure = map(lambda year: sum(map(len, year)), yearly_objects)
    yearly_density = map(lambda (measure, count): measure/count, zip(yearly_measure, yearly_count))

    [yc_labels, ym_labels, yd_labels] = map(lambda d: make_year_labels(years, d),
                                            [yearly_count, yearly_measure, yearly_density])

    density_labels = make_pool_labels([max(yearly_density)])

    ## Context dictionary and rendering

    context = dict([(x, locals()[x]) for x in ['pool_data',
                                               'pool_x_range',
                                               'pool_x_dates',
                                               'pool_range_xlabels',
                                               'pool_date_xlabels',
                                               'pool_size_ylabels',
                                               'yearly_count',
                                               'yearly_measure',
                                               'yearly_density',
                                               'yc_labels',
                                               'ym_labels',
                                               'yd_labels',
                                               'density_labels',
                                               'years']])
    
    return render_to_response(template_name, context)

