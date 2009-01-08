# This file defines `dev_media_url` pattern, which is used in Django
# `urls.py` with development server

from site_settings import SITE_PREFIX
from site_helpers import at_dev

if at_dev():
    from django.conf.urls.defaults import *
    from django.views.static import serve
    dev_media_url =  patterns('',
                              (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': SITE_PREFIX + '/media'}))
else:
    dev_media_url = []
