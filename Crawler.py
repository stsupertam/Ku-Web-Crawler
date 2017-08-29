import os
import hashlib
import sys
import requests
import tldextract
from bs4 import BeautifulSoup
from urlparse import urlparse
from urlparse import urljoin

class Spider():

    def __init__(self, url, max_depth = 2, total_pages = 100):
        self.max_depth = max_depth
        self.url = url
        self.total_pages = total_pages
        self.pages = 0

    def startCrawl(self):
        u_parse = urlparse(self.url)
        self.domain = u_parse.netloc
        self.scheme = u_parse.scheme
        self.url_sets = set()
        self.crawl([u_parse.path], self.max_depth)

    def crawl(self, urls, depth):
        n_urls = set()
        print('Depth (%d)' % depth)
        if(depth >= 0):
            for url in urls:
                link = self.get_link(url)
                n_urls = n_urls.union(link)
            self.crawl(n_urls, depth - 1)

    def get_link(self, url):
        links = []
        u_parse = urlparse(url)
        url = u_parse.path + u_parse.query
        domain = u_parse.netloc

        if(not domain):
            domain = self.domain
        
        if(tldextract.extract(self.domain).domain == tldextract.extract(domain).domain):
            try:
                print('Retrieving [%s] %s' % (self.pages, domain, url))
                data  = requests.get(('%s://%s%s' % (self.scheme, domain, url)))
                soup = BeautifulSoup(data.text, 'lxml')

                self.writeToFile(domain, soup)

                for tag in soup.findAll('a', href=True):
                    absolute_url = urljoin(self.domain, tag['href'])
                    if(absolute_url not in self.url_sets):
                        if(self.pages <= self.total_pages):
                            self.url_sets.add(absolute_url)
                            links.append(absolute_url)
                            self.pages += 1

            except Exception:
                print sys.exc_info()[0] 

        return links

    def writeToFile(self, domain, soup):
        directory = 'data/' + domain
        if(not os.path.exists(directory)):
            print('Create [%s] directory' % domain)
            os.makedirs('data/' + domain)
        
        html = soup.prettify('utf-8')
        h = hashlib.md5(html).hexdigest()
        fileName = directory + '/' + h + '.html'
        print('Create [%s] file' % h)
        with open(fileName, "wb") as file:
            file.write(html)



spider = Spider('https://stackoverflow.com/')
spider.startCrawl()
print('Crawl Stackoverflow Successful')                 