from bs4 import BeautifulSoup
from urlparse import urlparse
from urlparse import urljoin
import tldextract
import requests

class LinkParser():

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

        data  = requests.get("http://" + self.url)
        soup = BeautifulSoup(data.text, 'lxml')

        for tag in soup.findAll('a', href=True):
            absolute_url = urljoin(self.hostname, tag['href'])
            self.enqueue(absolute_url)
        return self.links
    
linkParser = LinkParser('ku.ac.th/web2012/index.php?c=adms&m=mainpage1', 'ku')
ku_url = linkParser.get_link()

for item in ku_url:
    print('Url : ' + item)