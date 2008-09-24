from django.contrib import admin

from models import *

class SerieAdmin(admin.ModelAdmin):
    pass

class EpisodeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Serie, SerieAdmin)
admin.site.register(Episode, EpisodeAdmin)