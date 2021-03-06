This is a simple blog engine by Dmitry Dzhus.

# Installation notes

For this blog to operate properly, define `SECRET_KEY` variable in
`secret.py` in the same directory as `settings.py`.

Default database name is `django.db`.

`site_settings.py` contains site-specific settings.

# Requirements

This blog is being successfully used with the following software:

- Django SVN 18-03-2011 with patches from tickets #7005 (orphans), (#8968)

- django-tagging, SVN r149 <http://code.google.com/p/django-tagging/>

- googlecharts for Django, <http://github.com/jacobian/django-googlecharts>

- pytils-0.2.3, <http://pypi.python.org/pypi/pytils/>

- flup

- python-markdown-2.0.3, <http://www.freewisdom.org/projects/python-markdown/>

# Copying permissions

All Python sources and Django templates under `blog/`,
`nerdcomments/`, `stats/` and `templates/` directories are subject to
GNU GENERAL PUBLIC LICENSE Version 3, as can be read on
http://www.gnu.org/licenses/gpl-3.0.html.

All files under `media/` are released under Creative Commons
Attribution 3.0 Unported license, as can be read on
http://creativecommons.org/licenses/by/3.0/.
