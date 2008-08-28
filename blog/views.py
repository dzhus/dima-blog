# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, InvalidPage

from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.template.loader import get_template

from django.views.generic.list_detail import object_list as object_list_view
from django.views.generic.list_detail import object_detail as object_detail_view

from blog.models import Entry

# import settings

# import captcha
# from md5 import md5 as md5hash
# from random import shuffle

def filter_inappropriate(request, queryset):
    """
    Take queryset and filter out objects inappropriate for current
    user (e. g. private entries shouldn't be seen by guests).
    """
    if not (request.user.is_authenticated() and \
            request.user.has_perm('blog.can_see_private')):
        return queryset.filter(private=0)
    else:
        return queryset    

def entry_list(request, tag=None, page='last', **kwargs):
    objects = Entry.objects

    queryset = filter_inappropriate(request, objects.order_by('add_date'))

    return object_list_view(request, queryset,
                            extra_context={'tag': tag,
                                           'tag_chunk' : tag and "tag/%s/" % tag or ''},
                            page=page,
                            **kwargs)
        
def entry_detail(request, queryset, **kwargs):
    queryset = filter_inappropriate(request, queryset)
    
    return object_detail_view(request, queryset, **kwargs)

def tag_list(request, template_name="entry_detail.xhtml"):
    pass
