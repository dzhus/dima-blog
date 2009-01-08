# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

from prob_utils import pool_size_function
from chart_helpers import date_to_epoch, group_by_year

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
        yearly_measure
            List with overall measures of objects created each year

    To get image URLs for charts, `get_url` method should be used in
    the template (like `uni_chart.get_url`), as well as their `width`
    and `height` fields.
    """
    def rescale_x(data):
        "Shift and rescale `data` to fit unit interval."
        head = data[0]
        data = map(lambda x: x - head, data)
        tail = data[-1:][0]
        return map(lambda x: x/float(tail), data)

    count = queryset.count()

    # Rescale pool size data
    pool_data = [x for x in pool_size_function(queryset)]
    pool_data = map(lambda x: float(x)/pool_data[-1:][0], pool_data)


    pool_x_range = rescale_x(range(count))
    pool_x_dates = rescale_x(map(lambda o: date_to_epoch(o.__dict__[date_field]),
                                 queryset))

    year_groups = group_by_year(queryset, date_field)
    years = year_groups.keys()

    # We manually sort year groups by keys
    years.sort()

    yearly_objects = [year_groups[y] for y in years]
    yearly_count = map(len, yearly_objects)
    yearly_measure = map(lambda year: sum(map(lambda object: len(object), year)), yearly_objects)

    yc_labels = ['%d (%s)' % (y, c) for (c, y) in zip(yearly_count, years)]
    ym_labels = ['%d (%s)' % (y, c) for (c, y) in zip(yearly_measure, years)]

    group_by_year(queryset, date_field).values()

    context = { 'pool_data': pool_data,
                'pool_x_range': pool_x_range,
                'pool_x_dates': pool_x_dates,
                'yearly_count': yearly_count,
                'yearly_measure': yearly_measure,
                'yc_labels': yc_labels,
                'ym_labels': ym_labels}
    
    return render_to_response(template_name, context)

