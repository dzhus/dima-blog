# -*- coding: utf-8 -*-
import django.views.generic.date_based

from django.views.static import serve
from django.conf.urls.defaults import *

from blog.models import Entry, File
from tags.models import Tag
from feeds import BlogFeed, BlogTagFeed

# Index page
urlpatterns = patterns('django.views.generic.date_based',
                       (r'^$', 'archive_index', {'queryset' : Entry.objects.filter(private=0),
                                                 'date_field' : "add_date",
                                                 'num_latest' : 5,
                                                 'template_name' : 'index.xhtml', 
                                                 'allow_empty' : False}
                        ),
                       )

# Generic blog views
urlpatterns += patterns('blog.views',
                        (r'^blog/page-(?P<page>\d+)/$', 'entry_list',     ),
                        (r'^blog/$', 'entry_list',     ),

                        (r'^blog/tag/(?P<tag>.+)/page-(?P<page>\d+)/$', 'entry_list',     ),
                        (r'^blog/tag/(?P<tag>.+)/$', 'entry_list',     ),

                        (r'^blog/tag/$', 'tag_list', {'queryset' : Tag.objects,
                                                      'template_name' : 'tags.xhtml',
                                                      'sort' : False,
                                                      }
                         )
                        )
                     
# Entry detail view
urlpatterns += patterns('',
                        (r'^blog/entry/(?P<entry_id>\d+)/$', 'blog.views.entry_detail',       ),
                        (r'^blog/entry/(?P<entry_slug>[\w-]+)/$', 'blog.views.entry_detail',       ),
                        )

# REMOVE AT REAL SERVER DEPLOYMENT
# @RRSD
urlpatterns += patterns('',
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/sphinx/projects/python/ws/media'})
                        )

# Archive views
urlpatterns += patterns('django.views.generic.date_based',
                        (r'^blog/archive/(?P<year>\d+)/$', 
                         'archive_year', 
                         {'queryset' : Entry.objects.order_by('add_date'),
                          'date_field' : "add_date",
                          'template_name' : 'blog_archive.xhtml',
                          'template_object_name' : 'entry',
                          'make_object_list' : True}
                         ),
                        
                        (r'^blog/archive/(?P<year>\d+)/(?P<month>\d+)/$',
                         'archive_month',
                         {'queryset' : Entry.objects.order_by('add_date'),
                          'date_field' : "add_date",
                          'template_name' : 'blog_archive.xhtml',
                          'template_object_name' : 'entry',
                          'month_format' : "%m"}
                         ),
                        )

# More archive views
urlpatterns += patterns('django.views.generic.list_detail',
                        (r'^blog/entry/$', 'object_list', {'queryset':Entry.objects.order_by("add_date"),
                                                           'template_name' : 'blog_archive.xhtml',
                                                           'template_object_name' : 'entry'}
                         ),
                        (r'^blog/archive/$', 'object_list', {'queryset' : Entry.objects.order_by("add_date"),
                                                             'template_name' : 'blog_archive.xhtml',
                                                             'template_object_name' : 'entry',
                                                             'extra_context' : {'archive_selection' : True}}
                         ),

                        (r'^files/$', 'object_list', {'queryset' : File.objects.order_by("add_date"),
                                                      'allow_empty' : True,
                                                      'template_name' : 'file_list.xhtml',
                                                      'template_object_name' : 'file'}
                         ),
                        )
        
# Auth views
urlpatterns += patterns('',
                        (r'^accounts/login/$','django.contrib.auth.views.login', {'template_name': 'login.xhtml'}),
                        (r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url':'/'}),
                        (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
                        )

# Feeds
urlpatterns += patterns('django.contrib.syndication.views',
                        (r'^feeds/(?P<url>.+)/$', 'feed', {'feed_dict' : {'blog':BlogFeed, 'blogtag':BlogTagFeed} }),
                        )

# Admin pages view
urlpatterns += patterns('',
                        (r'^admin/', include('django.contrib.admin.urls')),
                        )

