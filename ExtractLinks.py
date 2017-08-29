from bs4 import BeautifulSoup
from urlparse import urlparse
from urlparse import urljoin
import tldextract
import requests

class ExtractLinks():

    def __init__(self, url):
        self.u_parse = urlparse(url)
        self.url = url
        self.links = []
        self.urls_set = set()
        self.domain = self.u_parse.netloc
        self.scheme = self.u_parse.scheme
        self.hostname = tldextract.extract(url).domain

    def check_is_duplicate(self, test_url):
        if(test_url not in self.urls_set):
            self.urls_set.add(test_url)
            return True

        return False

    def check_is_same_domain(self, test_url):
        test_domain = tldextract.extract(test_url).domain

        if(self.hostname == test_domain):
            return True

        return False

    def enqueue(self, url):
        #if(self.check_is_same_domain(url) and self.check_is_duplicate(url)):
        if(self.check_is_same_domain(url)):
            self.links.append(url)
            print url

    def get_link(self, url):
        u_parse = urlparse(url)
        url = u_parse.path + u_parse.query
        try:
            data  = requests.get(('%s://%s%s' % (self.scheme, self.domain, url)))
            soup = BeautifulSoup(data.text, 'lxml')

            for tag in soup.findAll('a', href=True):
                absolute_url = urljoin(self.domain, tag['href'])
                self.enqueue(absolute_url)

        except Exception:
            pass

        return self.links