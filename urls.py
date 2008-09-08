# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

# Load generic and admin views
import django.views.generic.date_based
import django.views.generic.list_detail
from django.contrib import admin
admin.autodiscover()

# Serve media at development deploy
from django.views.static import serve

# Our stuff
from blog.models import Entry, File
#from tags.models import Tag
from feeds import BlogFeed#, BlogTagFeed
from blog.views import entry_list, entry_detail, tag_cloud

## Index page
urlpatterns = patterns('django.views.generic.date_based',
                       (r'^$', 'archive_index', {'queryset': Entry.objects.filter(private=0),
                                                 'date_field': 'add_date',
                                                 'num_latest': 5,
                                                 'template_name': 'index.xhtml', 
                                                 'allow_empty': False}))

## Entry list views
list_common_kwargs = {'paginate_by': 5,
                      'orphans': 2,
                      'template_name': 'entry_list.xhtml',
                      'template_object_name': 'entry'}
urlpatterns += patterns('',
                        (r'^blog/page-(?P<page>\d+)/$', entry_list, list_common_kwargs),
                        (r'^blog/$', entry_list, list_common_kwargs),

                        (r'^blog/tag/(?P<tag>.+)/page-(?P<page>\d+)/$', entry_list, list_common_kwargs),
                        (r'^blog/tag/(?P<tag>.+)/$', entry_list, list_common_kwargs),
                        (r'^blog/tag/$', tag_cloud))

## Entry detail view
detail_common_kwargs = {'queryset': Entry.objects,
                        'template_name': 'entry_detail.xhtml',
                        'template_object_name': 'entry'}
urlpatterns += patterns('django.views.generic.list_detail',
                        (r'^blog/entry/(?P<object_id>\d+)/$', entry_detail, detail_common_kwargs),
                        (r'^blog/entry/(?P<slug>[\w-]+)/$', entry_detail, detail_common_kwargs))


## REMOVE AT REAL SERVER DEPLOYMENT !!
## @RRSD
urlpatterns += patterns('',
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': '/home/sphinx/projects/python/ws/media'}))

## Archive views
urlpatterns += patterns('django.views.generic.date_based',
                        (r'^blog/archive/(?P<year>\d+)/$',
                         'archive_year', 
                         {'queryset': Entry.objects.order_by('add_date'),
                          'date_field': 'add_date',
                          'template_name': 'blog_archive.xhtml',
                          'template_object_name': 'entry',
                          'make_object_list': True}),
                        (r'^blog/archive/(?P<year>\d+)/(?P<month>\d+)/$',
                         'archive_month',
                         {'queryset': Entry.objects.order_by('add_date'),
                          'date_field': 'add_date',
                          'template_name': 'blog_archive.xhtml',
                          'template_object_name': 'entry',
                          'month_format': '%m'}))

## More archive views
urlpatterns += patterns('django.views.generic.list_detail',
                        (r'^blog/entry/$', 'object_list',
                         {'queryset': Entry.objects.order_by('add_date'),
                          'template_name': 'blog_archive.xhtml',
                          'template_object_name': 'entry'}),
                        (r'^blog/archive/$', 'object_list',
                         {'queryset': Entry.objects.order_by('add_date'),
                          'template_name': 'blog_archive.xhtml',
                          'template_object_name': 'entry',
                          'extra_context': {'archive_selection': True}}),
                        (r'^files/$', 'object_list',
                         {'queryset': File.objects.order_by('add_date'),
                          'allow_empty': True,
                          'template_name': 'file_list.xhtml',
                          'template_object_name': 'file'}) )
        
## Auth views
urlpatterns += patterns('django',
                        (r'^accounts/login/$',
                         'contrib.auth.views.login', {'template_name': 'login.xhtml'}),
                        (r'^accounts/logout/$',
                         'contrib.auth.views.logout', {'next_page': '/'}))

## Feeds
urlpatterns += patterns('django.contrib.syndication.views',
                        (r'^feeds/(?P<url>.+)/$', 'feed',
                         {'feed_dict': {'blog': BlogFeed}}))#, 'blogtag': BlogTagFeed} }))

## Admin pages view
urlpatterns += patterns('',
                        (r'^admin/(.*)', admin.site.root))

urlpatterns += patterns('',
                       (r'^comments/', include('django.contrib.comments.urls')))
