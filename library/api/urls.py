from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    (r'^search-serie/$', search_serie),
    (r'^search-serie/(\w+)$', search_serie),
)