#!/usr/bin/env python
# encoding:utf-8

import os, sys, re

from django.core.management import setup_environ
try:
    import settings # Assumed to be in the same directory.
    setup_environ(settings)
    from series.models import Episode, Serie
    from common.models import File
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

import tvdb

# This part comes from dbr/Ben's tvnamer from http://github.com/dbr/tvdb_api

config = {}

# The format of the renamed files (with and without episode names)
config['with_ep_name'] = '%(seriesname)s - [%(seasno)02dx%(epno)02d] - %(epname)s.%(ext)s'
config['without_ep_name'] = '%(seriesname)s - [%(seasno)02dx%(epno)02d].%(ext)s'
 
config['valid_filename_chars'] = u"""0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@£$%^&*()_+=-[]{}"'.,<>`~? """
config['valid_filename_chars_regex'] = re.escape(config['valid_filename_chars'])
 
# Regex's to parse filenames with. Must have 3 groups, seriesname, season number
# and episode number. Use (?: optional) non-capturing groups if you need others.
config['name_parse'] = [
    # foo_[s01]_[e01]
    re.compile('''^([%s]+?)[ \._\-]\[[Ss]([0-9]+?)\]_\[[Ee]([0-9]+?)\]?[^\\/]*$'''% (config['valid_filename_chars_regex'])),
    # foo.1x09*
    re.compile('''^([%s]+?)[ \._\-]\[?([0-9]+)x([0-9]+)[^\\/]*$''' % (config['valid_filename_chars_regex'])),
    # foo.s01.e01, foo.s01_e01
    re.compile('''^([%s]+?)[ \._\-][Ss]([0-9]+)[\.\- ]?[Ee]([0-9]+)[^\\/]*$''' % (config['valid_filename_chars_regex'])),
    # foo.103*
    re.compile('''^([%s]+)[ \._\-]([0-9]{1})([0-9]{2})[\._ -][^\\/]*$''' % (config['valid_filename_chars_regex'])),
    # foo.0103*
    re.compile('''^([%s]+)[ \._\-]([0-9]{2})([0-9]{2,3})[\._ -][^\\/]*$''' % (config['valid_filename_chars_regex'])),
]

config['verbose'] = True
config['interactive'] = True

def ask(question):
    answer = None
    while answer not in ['y', 'n', 'q', '']:
        print question,
        print '([y]/n/q)',
        try:
            answer = raw_input().strip()
        except KeyboardInterrupt, errormsg:
            print u'\n', errormsg
            sys.exit(1)
    if answer in ['y', '']:
        return True
    elif answer == 'q':
        sys.exit(0)
    else:
        return False

def parse_filename(filename, verbose=False):
    for r in config['name_parse']:
        match = r.match(filename)
        if match:
            serie_name, season_number, episode_number = match.groups()
            serie_name = re.sub("[\._]|\-(?=$)", " ", serie_name).strip()
            if verbose:
                print u'=' * 80
                print u'File name: ', filename
                print u'Serie name: ', serie_name
                print u'Season number: ', int(season_number)
                print u'Episode number: ', int(episode_number)
                print u'=' * 80
            return (serie_name, int(season_number), int(episode_number))
    else:
        print 'Invalid name: ', filename

def process_file(filename, interactive=False):
    ep = parse_filename(filename, True)
    if ep is not None:
        if not interactive or ask(u'Continue?'):
            serie_name, season_number, episode_number = ep
            try:
                serie = Serie.objects.get(title__iexact=serie_name)
            except Serie.DoesNotExist:
                serie = Serie.objects.get(short_title__iexact=serie_name)
            if serie:
                episode = Episode(serie_id=serie.id, season_number=season_number, episode_number=episode_number)
                episode.save()
                file = File(file_path=filename, content_object=episode)
                file.save()
            else:
                print u'Could not find serie in database.'

def process_files(files, interactive=False):
    for file in files:
        if not interactive:
            process_file(file, interactive)
        else:
            if ask(u'Process %s ?' % file):
                process_file(file, interactive)
            else:
                continue

def find_files(path=settings.LIBRARY_ROOT, match=None):
    files = []
    if match is not None:
        match_re = re.compile(match)
    for f in os.listdir(path):
        full_file = os.path.join(path, f)
        if os.path.isfile(full_file) and (match is None or match_re.search(f)):
            files.append(f)
    return files

def main():
    from optparse import OptionParser

    parser = OptionParser(usage="%prog [options]")
    parser.add_option("-i", "--interactive", action="store_true", dest="interactive", default=False,
        help="interactivly select correct show from search results [default]")
    opts, args = parser.parse_args()
    process_files(find_files(match=r'^[^\.]'), interactive=opts.interactive)

if __name__ == '__main__':
    main()