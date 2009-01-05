# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, InvalidPage

from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist

from django.template import RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response

from tagging.views import tagged_object_list as tagged_object_list
from django.views.generic.list_detail import object_detail as object_detail_view
from django.views.generic.list_detail import object_list as object_list_view

from blog.models import Entry
from tagging.models import Tag

def make_filter_kwargs(request):
    """
    Make a set of filter kwargs to hide objects inappropriate for
    current user (e. g. private entries mustn't be seen by guests).
    """
    if not (request.user.is_authenticated() and \
            request.user.has_perm('blog.can_see_private')):
        return {'private': 0}
    else:
        return {}

def entry_list(request, queryset=Entry.objects.order_by('add_date'),
               tag=None, template_object_name='entry', page='last', **kwargs):
    """
    Show all entries with given tag, paginated and filtered.

    This function accepts the same arguments as `tagged_object_list` and
    `object_list` generic views.
    """

    # I want to filter out private entries, so I have to use a
    # queryset based upon request data
    queryset = queryset.filter(**make_filter_kwargs(request))

    if tag is None:
        return object_list_view(request, queryset,
                                template_object_name=template_object_name,
                                page=page, **kwargs)
    else:
        return tagged_object_list(request, queryset,
                                  template_object_name=template_object_name,
                                  tag=tag, page=page,
                                  extra_context={'tag_chunk': "tag/%s/" % tag},
                                  **kwargs)
        
def entry_detail(request, queryset, **kwargs):
    filter_kwargs = make_filter_kwargs(request)
    queryset = queryset.filter(**filter_kwargs)

    # Violate DRY badly as generic detail view doesn't allow to add
    # extra context which uses found object
    assert('object_id' in kwargs.keys() or 'slug' in kwargs.keys())
    if 'object_id' in kwargs.keys():
        queryset = queryset.filter(pk=kwargs['object_id'])
    else:
        queryset = queryset.filter(slug=kwargs['slug'])
    try:
        obj = queryset.get()
    except ObjectDoesNotExist:
        raise Http404

    # Exceptions not necessarily happen at the same time, so use two
    # try..except blocks
    try:
        prev_entry = obj.get_previous_by_add_date(**filter_kwargs)
    except ObjectDoesNotExist:
        prev_entry = None
    try:
        next_entry = obj.get_next_by_add_date(**filter_kwargs)
    except ObjectDoesNotExist:
        next_entry = None
    
    return object_detail_view(request, queryset,
                              extra_context={'full_view': True,
                                             'filter': filter_kwargs,
                                             'prev_entry': prev_entry,
                                             'next_entry': next_entry},
                              **kwargs)

def tag_cloud(request, shuffle=True, template_name="tags.html"):
    filter_kwargs = make_filter_kwargs(request)
    cloud = Tag.objects.cloud_for_model(Entry, steps=6, filters=filter_kwargs)
    if shuffle:
        import random
        random.shuffle(cloud)
    context = {'tags': cloud}
    return render_to_response(template_name, context)

def archive_view(request, view, queryset=Entry.objects.order_by('add_date'),
                 template_name=None, template_object_name=None,
                 date_field='add_date', **kwargs):
    """
    Decorate generic year and month views.

    View to call after decorating is passed with `view` argument.

    Filter private entries if necessary.

    If `template_name` argument is not passed, a default value of
    `<model_name>_<view_func_name>.html` is used.

    If `template_object_name` is none, use `<model_name>`.

    Add `year` to template context (even if using `archive_month`).
    """
    queryset = queryset.filter(**make_filter_kwargs(request))

    model_name = queryset.model._meta.object_name.lower()

    if template_name is None:
        t_n = '%s_%s.html' % (model_name, view.func_name)
    if template_object_name is None:
        t_o_n = model_name

    if not kwargs.has_key('extra_context'):
        kwargs['extra_context'] = {}

    kwargs['extra_context'].update({'year': kwargs['year']})
    
    return view(request, queryset=queryset, date_field=date_field,
                template_name=t_n, template_object_name=t_o_n,
                **kwargs)
