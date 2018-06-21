import threading
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen


class Episode:
    def __init__(self, title, views):
        self.title = title
        self.views = views

    def __str__(self):
        return "Title: {}, Views:{}".format(self.title, self.views)


class Season:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.episodes = []

    @property
    def season_total(self):
        return sum([e.views for e in self.episodes])

    def __str__(self):
        return "{} has {} episodes with {} total views".format(self.name, len(self.episodes), self.season_total)


def get_seasons():
    base_url = 'https://en.wikipedia.org'
    adaptation_url = 'https://en.wikipedia.org/wiki/Game_of_Thrones'
    resp = urlopen(adaptation_url).read()
    soup = BeautifulSoup(resp)
    table = soup.find("table", attrs={"class": "wikitable plainrowheaders"})
    ths = table.findAll('th', attrs={"scope": "row"})

    all_seasons = []
    for l in ths:
        season_name = str(l.find('a')['href'])
        season_url = base_url + str(l.find('a')['href'])
        all_seasons.append(Season(season_name, season_url))
    return all_seasons


def get_episode_data(got_season):
    response = urlopen(got_season.url)
    episode_soup = BeautifulSoup(response)

    table = episode_soup.find("table", attrs={"class": "wikitable plainrowheaders wikiepisodetable"})
    trs = table.findAll('tr', attrs={"class": "vevent"})
    for tr in trs:
        tds = tr.findAll('td')
        epi_name = str(tds[1].a.string)
        epi_views = float(tds[-1].contents[0])
        got_season.episodes.append(Episode(epi_name, epi_views))


seasons = get_seasons()

threads = []
for season in seasons[:-1]:
    t = threading.Thread(target=get_episode_data, args=(season,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

for s in seasons:
    print(s)

print "Total views for all seasons", sum(s.season_total for s in seasons)
