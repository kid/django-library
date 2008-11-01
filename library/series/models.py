from os import path

from django.db import models

from common.models import *

class Serie(ImdbItem):
    short_title = models.CharField(max_length=40, blank=True)
    tvdb_id = models.PositiveIntegerField(blank=True, null=True)

    def get_canonical_tite(self):
        return '%s (%d)' % (self.title, self.year)

    def get_path(self):
        return path.join('Series', self.get_canonical_tite().replace('/', ' '))

class Episode(ImdbItem, DatedItem):
    serie = models.ForeignKey(Serie)
    tvdb_id = models.PositiveIntegerField(blank=True, null=True)
    season_number = models.PositiveSmallIntegerField()
    episode_number = models.PositiveSmallIntegerField()
    last_episode_number = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('serie', 'season_number', 'episode_number', 'last_episode_number'),)

    def __unicode__(self):
        return self.get_canonical_tite()

    def full_ep_number(self):
        if self.last_episode_number:
            return u'S%02dE%02d-%02d' % (self.season_number, self.episode_number, self.last_episode_number)
        return u'S%02dE%02d' % (self.season_number, self.episode_number)

    def get_canonical_tite(self):
        return u'%s - %s - %s' % (self.serie.short_title or self.serie.title, self.full_ep_number(), self.title)

    def get_path(self):
        return path.join(self.serie.get_path(), u'Season %d' % self.season_number, self.get_canonical_tite().replace('/', ' '))