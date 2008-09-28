import os, re

from django import forms
from django.forms.util import ErrorList

from common.models import File

import settings

def get_file_choices(path, match=None):
    choices = [('', '--------')]
    if match is not None:
        match_re = re.compile(match)
    try:
        for f in os.listdir(path):
            full_file = os.path.join(path, f)
            if os.path.isfile(full_file) and (match is None or match_re.search(f)):
                choices.append((full_file, f))
    except OSError:
        pass
    return choices

class FileForm(forms.ModelForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
        super(FileForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance)
        file_path = self.fields['file_path']
        if not instance:
            file_path.widget = forms.Select(choices=get_file_choices(settings.LIBRARY_ROOT, match=r'^[^\.]'))

    class Meta:
        model = File