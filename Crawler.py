from ExtractLinks import ExtractLinks
import tldextract
from bs4 import BeautifulSoup
from urlparse import urlparse
from urlparse import urljoin
import requests



class Spider():

    def __init__(self, url, max_depth = 2, total_pages = 50):
        self.max_depth = max_depth
        self.url = url
        self.total_pages = total_pages
        self.pages = 0
        self.content = {}

    def startCrawl(self):
        u_parse = urlparse(self.url)
        self.domain = u_parse.netloc
        self.content[self.domain] = {}
        self.scheme = u_parse.scheme
        self.url_sets = set()
        self.crawl([u_parse.path], self.max_depth)

    def crawl(self, urls, depth):
        n_urls = set()
        if(depth >= 0):
            for url in urls:
                link = self.get_link(url)
                n_urls = n_urls.union(link)
                print('DEPTH (%d) (%d) URL %s' % (depth, self.pages, url))
            self.crawl(n_urls, depth - 1)

    def get_link(self, url):
        links = []
        u_parse = urlparse(url)
        url = u_parse.path + u_parse.query
        try:
            if(self.pages <= self.total_pages):
                data  = requests.get(('%s://%s%s' % (self.scheme, self.domain, url)))
                soup = BeautifulSoup(data.text, 'lxml')

                for tag in soup.findAll('a', href=True):
                    absolute_url = urljoin(self.domain, tag['href'])
                    if(absolute_url not in self.url_sets):
                        if(self.pages <= self.total_pages):
                            self.url_sets.add(absolute_url)
                            links.append(absolute_url)
                            self.pages += 1
        except Exception:
            pass
        return links


spider = Spider('https://stackoverflow.com/')
spider.startCrawl()
print('Crawl Stackoverflow Successful')                 