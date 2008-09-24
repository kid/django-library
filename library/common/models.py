from django.db import models

FORMATS = (
    (0, 'SD'),
    (1, '720p'),
    (2, '1080i'),
    (3, '1080p'),
)

SOUND = (
    (0, 'VF'),
    (3, 'VFC'),
    (1, 'VO'),
    (2, 'VF+VO'),
    (4, 'VFV+VO'),
)

class ImdbItem(models.Model):
    title = models.CharField(max_length=1024)
    imdb_id = models.CharField(max_length=40)

    class Meta:
        abstract = True

class File(models.Model):
    pass