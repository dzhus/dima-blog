# Django settings for WS project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'django.db'             # Or path to database file if using sqlite3.


# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'ru-ru'

DATE_FORMAT = 'd.m.Y'

DATETIME_FORMAT = 'd.m.y @ G:i'

SITE_ID = 1

APPEND_SLASH = True

ADMIN_MEDIA_PREFIX = '/media/admin/'
#MEDIA_ROOT = '/var/www/localhost/htdocs/media/'
MEDIA_ROOT = '/home/sphinx/projects/python/ws/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k&2d**^=n!y9$5$kx$^6iw_kq0=uih47w=lqb@t(+bt-k=8z%q'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.auth',
        )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Always use forward slashes, even on Windows.
#    "/var/www/localhost/htdocs/templates",
#    "/var/www/localhost/htdocs/blog/templates"
    "/home/sphinx/projects/python/ws/templates",
    "/home/sphinx/projects/python/ws/blog/templates"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.markup',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'blog',
    'tags',
    'pytils'
)
