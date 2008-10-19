API_KEY = '7225616E67F7ABD3'

from urllib import urlopen

from BeautifulSoup import BeautifulStoneSoup

def _get_mirrors_list():
    mirrors = []
    soup = BeautifulStoneSoup(urlopen(u'http://www.thetvdb.com/api/%s/mirrors.xml' % API_KEY).read())
    for mirror in soup.findAll(u'mirror'):
        mask = int(mirror.find(u'typemask').contents[0], 10)
        if mask & 1:
            mirrors.append(mirror.find(u'mirrorpath').contents[0])
    return mirrors

def get_random_mirror():
    import random
    return random.choice(_get_mirrors_list())

def search_series(title):
    series = []
    random_mirror = get_random_mirror()
    soup = BeautifulStoneSoup(urlopen(u'%(random_mirror)s/api/GetSeries.php?seriesname=%(title)s' % locals()))
    for serie in soup.findAll(u'series'):
        series.append({
            u'id': serie.find(u'id').contents[0],
            u'title': serie.find(u'seriesname').contents[0]
        })
    return series

def get_episode(serie_id, season_number, episode_number, language=u'en', order=u'default'):
    if order not in (u'default', u'dvd',):
        raise Error(u'Incorrect order')
    episode = {}
    random_mirror = get_random_mirror()
    api_key = API_KEY
    url = u'%(random_mirror)s/api/%(api_key)s/series/%(serie_id)s/%(order)s/%(season_number)s/%(episode_number)s/%(language)s.xml'
    soup = BeautifulStoneSoup(urlopen(url % locals()))
    for attribute in soup.find(u'episode').findAll():
        if attribute.contents:
            episode[attribute.name] = attribute.contents[0]
    return episode

if __name__ == '__main__':
    print get_episode(search_series(u'Knight Rider (2008)')[0]['id'], 1, 1).values()
    