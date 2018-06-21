from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen

url = 'http://quotes.yourdictionary.com/theme/marriage/'
resp = urlopen(url).read()
soup = BeautifulSoup(resp)


class Quote(object):
    def __init__(self, author, quote):
        self.author = author.strip().title()
        self.quote = quote.strip().title()

    def __str__(self):
        return "'{}' - {}".format(self.quote, self.author)


quotes = soup.findAll('p', attrs={"class": "quoteContent"})
authors = soup.findAll('a', attrs={"class": "author_link_tag"})

results = [Quote(a.string, q.string) for a, q in zip(authors[:5], quotes[:5])]

for index, r in enumerate(results, start=1):
    print("{}) {}".format(index, r))
    print("")
