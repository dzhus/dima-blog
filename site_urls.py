# This file defines `dev_media_url` pattern, which is used in Django
# `urls.py` with development server

from socket import gethostname

from django.conf.urls.defaults import *

hostname = gethostname()

if hostname == 'blizzard':
    # Not needed with real webserver, development only
    from django.views.static import serve
    dev_media_url =  patterns('',
                              (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': '/home/sphinx/projects/python/ws/media'}))
elif hostname == 'sphinx.net.ru':
    dev_media_url = []
