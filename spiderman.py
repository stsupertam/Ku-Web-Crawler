from bs4 import BeautifulSoup
from urlparse import urlparse
from urlparse import urljoin
import requests

class LinkParser():

    def __init__(self, url, hostname):
        self.url = url
        self.hostname = hostname
        self.links = []

    def check_duplicate(self):
        pass

    def enqueue(self):
        pass

    def get_link(self):
        data  = requests.get("http://" + self.url)
        soup = BeautifulSoup(data.text, 'lxml')
        for tag in soup.findAll('a', href=True):
            absolute_url = urljoin(self.hostname, tag['href'])
            enqueue(absolute_url)
    

linkParser = LinkParser('ku.ac.th/web2012/index.php?c=adms&m=mainpage1', 'www.ku.ac.th')
linkParser.get_link()

#def check(url):
#    t = urlparse(url).hostname
#    return t
#
#ku_domain = check(ku)
#cpe_domain = check(cpe)
#
#ku_domain = ku_domain.rsplit('.', 3)[1:]
#cpe_domain = cpe_domain.rsplit('.', 3)[1:]
#if ku_domain == cpe_domain:
#    print('fucking work eiei')
