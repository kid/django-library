import os, sys
sys.path = ['/opt/django/django', '/opt/django-library/library'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'library.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()