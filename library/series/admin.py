from django.contrib import admin
from django.contrib.contenttypes import generic

from models import *
from common.models import File

class FileInline(generic.GenericTabularInline):
    model = File
    extra = 1

class SerieAdmin(admin.ModelAdmin):
    pass

class EpisodeAdmin(admin.ModelAdmin):
    inlines = (FileInline,)

admin.site.register(Serie, SerieAdmin)
admin.site.register(Episode, EpisodeAdmin)