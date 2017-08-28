from bs4 import BeautifulSoup
from urlparse import urlparse
from urlparse import urljoin
import tldextract
import requests

class ExtractLinks():

    def __init__(self, url, hostname):
        self.url = url
        self.hostname = hostname
        self.links = []
        self.urls_set = set()

    def check_is_duplicate(self, url):
        if(url not in self.urls_set):
            self.urls_set.add(url)
            return True
        return False


    def check_is_same_domain(self, test_url):
        test_domain = tldextract.extract(test_url).domain
        if(self.hostname == test_domain):
            return True
        return False

    def enqueue(self, url):
        if(self.check_is_same_domain(url) and self.check_is_duplicate(url)):
            self.links.append(url)
            
    def get_link(self):

        if(self.url[0:4].lower() != 'http'):
            self.url = 'http://' + self.url
        data  = requests.get(self.url)
        soup = BeautifulSoup(data.text, 'lxml')

        for tag in soup.findAll('a', href=True):
            absolute_url = urljoin(self.hostname, tag['href'])
            self.enqueue(absolute_url)
        return self.links
    
