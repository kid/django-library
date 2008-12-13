from django.conf.urls.defaults import *
from django.contrib import admin, databrowse

from common.models import File
from series.models import Episode, Serie

import settings

databrowse.site.register(Serie)
databrowse.site.register(Episode)
databrowse.site.register(File)

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )