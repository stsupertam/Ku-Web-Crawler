from bs4 import BeautifulSoup
from urlparse import urlparse
from urlparse import urljoin
import requests

class LinkParser():

    def __init__(self, url, hostname):
        self.url = url
        self.hostname = hostname
        self.links = []

    def check_duplicate(self, url):
        pass

    def check_is_same_domain(self, test_url):
        host_url = urlparse('http://' + self.hostname).hostname
        host_domain = host_url.rsplit('.', 3)[1:]

        test_url = urlparse(test_url).hostname
        test_domain = host_url.rsplit('.', 3)[1:]

        if(host_domain == test_domain):
            return True
        return False

    def enqueue(self, url):
        if(self.check_is_same_domain(url) and self.check_duplicate(url)):
            self.links.append(url)
            
    def get_link(self):
        data  = requests.get("http://" + self.url)
        soup = BeautifulSoup(data.text, 'lxml')
        for tag in soup.findAll('a', href=True):
            absolute_url = urljoin(self.hostname, tag['href'])
            self.enqueue(absolute_url)
    

linkParser = LinkParser('ku.ac.th/web2012/index.php?c=adms&m=mainpage1', 'www.ku.ac.th')
linkParser.get_link()