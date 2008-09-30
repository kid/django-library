from django.conf.urls.defaults import *
from django.contrib import admin, databrowse

from common.models import File
from series.models import Episode, Serie

databrowse.site.register(Serie)
databrowse.site.register(Episode)
databrowse.site.register(File)

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^databrowse/(.*)', databrowse.site.root),
    (r'^api/', include('api.urls'))
)