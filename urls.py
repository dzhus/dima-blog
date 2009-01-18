# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

# Load generic and admin views
from django.views.generic.date_based import archive_year, archive_month
import django.views.generic.list_detail
from django.contrib import admin
admin.autodiscover()

# Our stuff
from blog.models import Entry, File
from feeds import BlogFeed, BlogTagFeed

from site_urls import dev_media_url

## Index page
urlpatterns = patterns('django.views.generic.date_based',
                       url(r'^$', 'archive_index', {'queryset': Entry.objects.filter(private=0),
                                                    'date_field': 'add_date',
                                                    'num_latest': 5,
                                                    'template_name': 'index.html', 
                                                    'allow_empty': False}))

## Media (development only)
urlpatterns += dev_media_url

blog_entries = Entry.objects.order_by('add_date')

## Entry list views
list_kwargs = {'paginate_by': 5,
               'orphans': 2,
               'queryset': blog_entries,
               'template_name': 'entry_list.html',
               'template_object_name': 'entry'}
urlpatterns += patterns('blog.views',
                        (r'^blog/page-(?P<page>\d+)/$', 'entry_list', list_kwargs),
                        (r'^blog/$', 'entry_list', list_kwargs),

                        (r'^blog/tag/(?P<tag>.+)/page-(?P<page>\d+)/$', 'entry_list', list_kwargs),
                        (r'^blog/tag/(?P<tag>.+)/$', 'entry_list', list_kwargs),
                        (r'^blog/tag/$', 'tag_cloud', {'shuffle': False}))

urlpatterns += patterns('stats.views',
                        (r'^blog/stats/$', 'blog_stats',
                         {'queryset': blog_entries,
                          'template_name': 'blog_stats.html'}))
                          
## Entry detail view
detail_kwargs = {'queryset': Entry.objects,
                 'template_name': 'entry_detail.html',
                 'template_object_name': 'entry'}
urlpatterns += patterns('blog.views',
                        url(r'^blog/entry/(?P<object_id>\d+)/$',
                            'entry_detail',
                            detail_kwargs,
                            'entry_by_id'),
                        url(r'^blog/entry/(?P<slug>[\w-]+)/$',
                            'entry_detail',
                            detail_kwargs,
                            'entry_by_slug'))


## Archive views
urlpatterns += patterns('blog.views',
                        url(r'^blog/archive/(?P<year>\d+)/$',
                            'archive_view',
                            {'view': archive_year,
                             'make_object_list': True},
                            'archive_year'),
                        url(r'^blog/archive/(?P<year>\d+)/(?P<month>\d+)/$',
                            'archive_view',
                            {'view': archive_month,
                             'month_format': '%m'},
                            'archive_month'),
                        url(r'^blog/entry/$',
                            'entry_list',
                            {'template_name': 'blog_archive_biglist.html',
                             'template_object_name': 'entry'},
                            'archive_biglist'),
                        url(r'^blog/archive/$',
                            'entry_list',
                            {'template_name': 'blog_archive.html',
                             'template_object_name': 'entry',
                             'extra_context': {'overview': True,
                                               'twelve': range(1, 13)}},
                            'archive_overview'))
## Files list
urlpatterns += patterns('django.views.generic.list_detail',
                        (r'^files/$', 'object_list',
                         {'queryset': File.objects.order_by('add_date'),
                          'allow_empty': True,
                          'template_name': 'file_list.html',
                          'template_object_name': 'file'}))
        
## Auth views
urlpatterns += patterns('django',
                        (r'^accounts/login/$',
                         'contrib.auth.views.login', {'template_name': 'login.html'}),
                        (r'^accounts/logout/$',
                         'contrib.auth.views.logout', {'next_page': '/'}))

## Feeds
urlpatterns += patterns('django.contrib.syndication.views',
                        (r'^feeds/(?P<url>.+)/$', 'feed',
                         {'feed_dict': {'blog': BlogFeed, 'blogtag': BlogTagFeed}}))

## Admin pages view
urlpatterns += patterns('',
                        (r'^admin/(.*)', admin.site.root))

urlpatterns += patterns('',
                       (r'^comments/', include('django.contrib.comments.urls')))
