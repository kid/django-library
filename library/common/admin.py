from django.contrib.contenttypes import generic
from django.contrib.contenttypes.generic import generic_inlineformset_factory

from common.forms import FileForm
from common.models import File

class FileAdminInline(generic.GenericStackedInline):
    form = FileForm
    extra = 1
    model = File