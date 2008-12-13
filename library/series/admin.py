from django.contrib import admin

from common.admin import FileAdminInline
from common.models import File

from series.models import Episode, Serie

class SerieAdmin(admin.ModelAdmin):
    pass

class EpisodeAdmin(admin.ModelAdmin):
    inlines = (FileAdminInline,)
    list_display = ('serie', 'full_ep_number', 'title',)
    list_filter = ('serie', 'season_number',)
    list_select_related = True
    search_fields = ('serie__title', 'season_number',)

admin.site.register(Serie, SerieAdmin)
admin.site.register(Episode, EpisodeAdmin)