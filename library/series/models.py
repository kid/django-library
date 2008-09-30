from os import path
from tvdb_api import Tvdb

from django.db import models

from common.models import *

class TvdbItem(DatedItem):
    title = models.CharField(max_length=1024)
    tvdb_id = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        abstract = True

class Serie(TvdbItem):
    short_title = models.CharField(max_length=40, blank=True)

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        if not self.tvdb_id:
            t = Tvdb()
            self.id = t[self.title].data['sid']
        super(Serie, self).save(force_insert, force_update)
        
    def get_path(self):
        return path.join('Series', self.title)

class Episode(TvdbItem):
    serie = models.ForeignKey(Serie)
    season_number = models.PositiveSmallIntegerField()
    episode_number = models.PositiveSmallIntegerField()
    last_episode_number = models.PositiveSmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.get_canonical_tite()

    def save(self, force_insert=False, force_update=False):
        if not self.tvdb_id:
            pass
        super(Episode, self).save(force_insert, force_update)

    def get_episode_number(self):
        if self.last_episode_number:
            return u'S%02dE%02d-%02d' % (self.season_number, self.episode_number, self.last_episode_number)
        return u'S%02dE%02d' % (self.season_number, self.episode_number)

    def get_canonical_tite(self):
        return u'%s - %s - %s' % (self.serie.short_title or self.serie.title, self.get_episode_number(), self.title)

    def get_path(self):
        return path.join(self.serie.get_path(), u'Season %d' % self.season_number, self.get_canonical_tite())