from django.contrib import admin

from common.admin import FileAdminInline
from common.models import File

from models import Episode, Serie

class SerieAdmin(admin.ModelAdmin):
    pass

class EpisodeAdmin(admin.ModelAdmin):
    inlines = (FileAdminInline,)

admin.site.register(Serie, SerieAdmin)
admin.site.register(Episode, EpisodeAdmin)