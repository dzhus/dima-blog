from site_helpers import at_dev

if at_dev():
    SITE_PREFIX = '/home/sphinx/projects/dima-blog'
else:
    SITE_PREFIX = '/var/www/localhost/htdocs'

DEBUG = at_dev()

TEMPLATE_DIRS = (SITE_PREFIX + '/templates')
MEDIA_ROOT = SITE_PREFIX + '/media/'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  SITE_PREFIX + '/django.db'
    }
}
