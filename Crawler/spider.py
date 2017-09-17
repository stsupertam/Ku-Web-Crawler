import sys
import re
import requests
import tldextract
from colorama import init
from colorama import Fore
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
from .writer import Writer
from .robotParser import RobotParser

class Spider:

    def __init__(self, url, max_depth = 2, total_pages = 100):
        init(autoreset=True)
        self.robotParser = RobotParser()
        self.writer = Writer()
        self.max_depth = max_depth
        self.url = url
        self.total_pages = total_pages
        self.pages = 0
        self.domain_sets = set()
        self.domain_robots = {}
        self.accept_file = set(['text/html', 'application/xml', 'application/xhtml+xml'])

    def startCrawl(self):
        u_parse = urlparse(self.url)
        self.domain = u_parse.netloc
        self.scheme = u_parse.scheme
        self.url_sets = set()
        self.crawl([u_parse.path], self.max_depth)

    def crawl(self, urls, depth):
        n_urls = set()
        #print('Depth (%d)' % depth)
        if(depth >= 0):
            for url in urls:
                link = self.get_link(url)
                n_urls = n_urls.union(link)
            self.crawl(n_urls, depth - 1)

    def get_link(self, url):
        links = []
        u_parse = urlparse(url)
        u_query = u_parse.query
        u_path = u_parse.path
        url = u_path + u_query
        domain = u_parse.netloc

        if(not domain):
            domain = self.domain
        split_domain = domain.split('.')
        if(re.match('www.*', split_domain[0])):
            split_domain = split_domain[1:]
            domain = str.join('.', split_domain)

        if(tldextract.extract(self.domain).domain == tldextract.extract(domain).domain):
            #print('[Domain] [%s][%s]' % (domain, u_path))
            if(domain not in self.domain_sets):
                self.domain_sets.add(domain)
                self.domain_robots = self.writer.writeRobotsToFile(domain, self.domain_robots, self.scheme)

            if(domain in self.domain_robots):
                if(not self.robotParser.canFetchUrl(domain, url)):
                    return links

            try:
                req_header  = requests.head(('%s://%s%s' % (self.scheme, domain, url)), timeout=(5,5))
                content_type = req_header.headers['content-type'].split(';')[0]

                if(content_type not in self.accept_file):
                    self.pages -= 1
                    print(Fore.RED + 'Retrieving [Failed] [Content-type isn\'t in Accept file]')
                    return links

                else:
                    data = requests.get(('%s://%s%s' % (self.scheme, domain, url)), timeout=(5,5))
                    status_code = data.status_code

                    if(status_code != requests.codes.ok):
                        self.pages -= 1
                        print(Fore.RED + 'Retrieving [Failed] [Code : %d] [%s] %s' % (status_code, domain, url))
                        return links

                    soup = BeautifulSoup(data.text, 'lxml')
                    self.writer.writeToFile(domain, u_path, url, soup)
                    print(Fore.GREEN + 'Retrieving [Success] [%s] %s' % (domain, url))

                    for tag in soup.findAll('a', href=True):
                        if(tag['href'] != '#'):
                            absolute_url = urljoin(self.domain, tag['href'])
                            if(absolute_url not in self.url_sets):
                                if(self.pages <= self.total_pages):
                                    self.url_sets.add(absolute_url)
                                    links.append(absolute_url)
                                    self.pages += 1

            except Exception:
                self.pages -= 1
                print(Fore.RED + 'Retrieving [Failed] [Error Exception : %s] [%s] %s' % (sys.exc_info()[0], domain, url))

        return links
