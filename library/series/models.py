from os import path
from tvdb_api import *

from django.db import models

from common.models import *

class Serie(DatedItem):
    title = models.CharField(max_length=1024)
    tvdb_id = models.PositiveIntegerField(blank=True, null=True)
    short_title = models.CharField(max_length=40, blank=True)

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        if not self.tvdb_id:
            t = Tvdb()
            self.tvdb_id = t[self.title].data['id']
        super(Serie, self).save(force_insert, force_update)
        
    def get_path(self):
        return path.join('Series', self.title)

class Episode(DatedItem):
    serie = models.ForeignKey(Serie)
    season_number = models.PositiveSmallIntegerField()
    episode_number = models.PositiveSmallIntegerField()
    last_episode_number = models.PositiveSmallIntegerField(blank=True, null=True)
    title = models.CharField(blank=True, max_length=1024)
    tvdb_id = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('serie', 'season_number', 'episode_number', 'last_episode_number'),)

    def __unicode__(self):
        return self.get_canonical_tite()

    def save(self, force_insert=False, force_update=False):
        if not self.title or not self.tvdb_id:
            t = Tvdb()
            e = t[self.serie.title][self.season_number][self.episode_number]
            if not self.title:
                self.title = e['episodename']
            if not self.tvdb_id:
                try:
                    self.tvdb_id = e['id']
                except tvdb_episodenotfound:
                    pass
        super(Episode, self).save(force_insert, force_update)

    def full_ep_number(self):
        if self.last_episode_number:
            return u'S%02dE%02d-%02d' % (self.season_number, self.episode_number, self.last_episode_number)
        return u'S%02dE%02d' % (self.season_number, self.episode_number)

    def get_canonical_tite(self):
        return u'%s - %s - %s' % (self.serie.short_title or self.serie.title, self.full_ep_number(), self.title)

    def get_path(self):
        return path.join(self.serie.get_path(), u'Season %d' % self.season_number, self.get_canonical_tite())