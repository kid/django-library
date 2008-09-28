import os, sys
sys.path.append('/opt/django/django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'library.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()