from site_settings import *
from secret import SECRET_KEY

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Dmitry Dzhus', 'dima@dzhus.org'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'ru-ru'

DATE_FORMAT = 'd.m.Y'

DATETIME_FORMAT = 'd.m.y @ G:i'

DEFAULT_CONTENT_TYPE = 'application/xhtml+xml'

SITE_ID = 1

APPEND_SLASH = True

ADMIN_MEDIA_PREFIX = '/media/admin/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',)

# Needed for admin shortcuts on index page and links in comments
#
# DO NOT remove the trailing comma!
TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.auth',)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.markup',
    'django.contrib.flatpages',
    'blog',
    'nerdcomments',
    'pytils',
    'stats',
    'tagging',
    'django-googlecharts')

COMMENTS_APP = 'nerdcomments'

LOGIN_REDIRECT_URL = '/'

FORCE_SCRIPT_NAME = ''
