from django.http import HttpResponse
from django.utils import simplejson

from tvdb_api import Tvdb

def search_serie(request, serie_title=None):
    data = [
        {'title': 'Knight Rider', 'sid': 77216},
        {'title': 'Knight Rider (2008)', 'sid': 81318},
    ]
    return HttpResponse(simplejson.dumps(data), mimetype='text/json')