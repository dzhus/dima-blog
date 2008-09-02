# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, InvalidPage

from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.template.loader import get_template

from django.views.generic.list_detail import object_list as object_list_view
from django.views.generic.list_detail import object_detail as object_detail_view

from blog.models import Entry

# import settings

# import captcha
# from md5 import md5 as md5hash
# from random import shuffle

def make_filter_kwargs(request):
    """
    Make a set of filter kwargs to hide objects inappropriate for
    current user (e. g. private entries shouldn't be seen by guests).
    """
    if not (request.user.is_authenticated() and \
            request.user.has_perm('blog.can_see_private')):
        return {'private': 0}
    else:
        return {}

def entry_list(request, tag=None, page='last', **kwargs):
    objects = Entry.objects

    queryset = objects.order_by('add_date').filter(**make_filter_kwargs(request))

    return object_list_view(request, queryset,
                            extra_context={'tag': tag,
                                           'tag_chunk' : tag and "tag/%s/" % tag or ''},
                            page=page,
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

def tag_list(request, template_name="entry_detail.xhtml"):
    pass
