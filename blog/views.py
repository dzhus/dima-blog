# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, InvalidPage

from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.template.loader import get_template

from django.views.generic.list_detail import object_list as object_list_view

from blog.models import Entry, Tag

#import settings

# import captcha
# from md5 import md5 as md5hash
# from random import shuffle

def entry_list(request, tag=None, **kwargs):
    if tag:
        objects = Tag.objects.get(value=tag).entry_set
    else:
        objects = Entry.objects

    queryset = objects.order_by('add_date')

    if not (request.user.is_authenticated() and \
            request.user.has_perm('blog.can_see_private')):
        queryset = queryset.filter(private=0)
        
    return object_list_view(request, queryset,
                            extra_context={'tag': tag,
                                           'tag_chunk' : tag and "tag/%s/" % tag or ''},
                            **kwargs)
#     p = Paginator(objects, paginate_by)

#     try:
#         # Three in a row combo!
#         page = p.page(page_number)
#     except InvalidPage:
#         raise Http404

#     c = RequestContext(request,
#                        {'entry_list': page.object_list,
#                         'p': page,
#                         'tag': tag,
#                         'tag_chunk' : tag and "tag/%s/" % tag or ''})
#     t = get_template(template_name)
    
#     return HttpResponse(t.render(c))
        
def entry_detail(request, template_name="entry_detail.xhtml"):
    pass

def tag_list(request, template_name="entry_detail.xhtml"):
    pass
