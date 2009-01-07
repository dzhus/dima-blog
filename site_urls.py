# This file defines `dev_media_url` pattern, which is used in Django
# `urls.py` with development server

from socket import gethostname
import os.path

from django.conf.urls.defaults import *

hostname = gethostname()
cd = os.path.abspath(os.path.curdir)

if hostname == 'blizzard':
    # Not needed with real webserver, development only
    from django.views.static import serve
    dev_media_url =  patterns('',
                              (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': cd + '/media'}))
else:
    dev_media_url = []
