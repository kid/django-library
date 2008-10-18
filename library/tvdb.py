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
    for serie in soup.findAll('series'):
        series.append({
            u'id': serie.find(u'id').contents[0],
            u'title': serie.find(u'seriesname').contents[0]
        })
    return series

if __name__ == '__main__':
    print search_series('Knight Rider')
    