from django.db import models

from common.models import ImdbItem

class Serie(ImdbItem):
    short_title = models.CharField(max_length=40)

class Episode(ImdbItem):
    serie = models.ForeignKey(Serie)
    season_number = models.PositiveSmallIntegerField()
    episode_number = models.PositiveSmallIntegerField()
    last_episode_number = models.PositiveSmallIntegerField()