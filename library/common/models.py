import os, re

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import settings

def clean_filename(filename):
    return filename.replace(' : ', ' ').replace(': ', ' ').replace(':', ' ')

FORMATS = (
    (0, 'SD'),
    (1, '720p'),
    (2, '1080i'),
    (3, '1080p'),
)

SOUND = (
    (0, 'VF'),
    (1, 'VFC'),
    (2, 'VO'),
    (3, 'VF+VO'),
    (4, 'VFV+VO'),
)

class DatedItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ImdbItem(models.Model):
    title = models.CharField(max_length=1024)
    year = models.PositiveIntegerField(blank=True, null=True)
    imdb_id = models.CharField(max_length=40, blank=True)

    def get_canonical_tite(self):
        return u'%s (%d)' % (self.title, self.year)

    def __unicode__(self):
        return self.get_canonical_tite()

    class Meta:
        abstract = True

class File(DatedItem):
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    file_path = models.CharField(max_length=1024)

    def __unicode__(self):
        return u'%s' % self.file_path

    def get_new_name(self):
        ext = re.match(r'^.+\.([^.]+)$', self.file_path).group(1)
        return u'%s.%s' % (self.content_object.get_path(), ext)

    def _move(self):
        new_name = clean_filename(self.get_new_name())
        if os.access(os.path.join(settings.LIBRARY_ROOT, new_name), os.F_OK):
            raise OSError
        os.renames(
            os.path.join(settings.LIBRARY_ROOT, self.file_path),
            os.path.join(settings.LIBRARY_ROOT, new_name)
        )
        self.file_path = new_name

    def save(self, force_insert=False, force_update=False):
        if not self.pk:
            self._move()
        super(File, self).save(force_insert, force_update)