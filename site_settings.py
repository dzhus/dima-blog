from socket import gethostname

hostname = gethostname()

if hostname == 'blizzard':
    TEMPLATE_DIRS = (
        "/home/sphinx/projects/python/ws/templates",
        "/home/sphinx/projects/python/ws/blog/templates")
    MEDIA_ROOT = '/home/sphinx/projects/python/ws/media/'
elif hostname == 'sphinx.net.ru':
    TEMPLATE_DIRS = (
        "/var/www/localhost/htdocs/templates",
        "/var/www/localhost/htdocs/blog/templates")
    MEDIA_ROOT = '/var/www/localhost/htdocs/media/'

