import os
import hashlib
import time
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
        self.total_file = 0
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
        if(split_domain[0] == 'www'):
            split_domain = split_domain[1:]
            domain = str.join('.', split_domain)

        if(tldextract.extract(self.domain).domain == tldextract.extract(domain).domain):
            #print('[Domain] [%s][%s]' % (domain, u_path))
            try:
                req_header  = requests.head(('%s://%s%s' % (self.scheme, domain, url)), timeout=5)
                content_type = req_header.headers['content-type'].split(';')[0]

                if(content_type not in self.accept_file):
                    self.pages -= 1
                    print('Retrieving [Failed] [Content-type isn\'t in Accept file]')
                    return links

                else:
                    data = requests.get(('%s://%s%s' % (self.scheme, domain, url)), timeout=5)
                    status_code = data.status_code

                    if(status_code != requests.codes.ok):
                        self.pages -= 1
                        print('Retrieving [Failed] [Code : %d]' % status_code)
                        return links

                    soup = BeautifulSoup(data.text, 'lxml')
                    self.writeToFile(domain, u_path, soup)
                    print('Retrieving [Success] [%s] %s' % (domain, url))

                    for tag in soup.findAll('a', href=True):
                        absolute_url = urljoin(self.domain, tag['href'])
                        if(absolute_url not in self.url_sets):
                            if(self.pages <= self.total_pages):
                                self.url_sets.add(absolute_url)
                                links.append(absolute_url)
                                self.pages += 1

            except Exception:
                self.pages -= 1
                print('Retrieving [Failed] [Error Exception : %s]' % sys.exc_info()[0])

        return links

    def writeToFile(self, domain, path, soup):
        directory = self.createDirectory(domain, path)
        html = soup.prettify('utf-8')
        h = hashlib.md5(html).hexdigest()
        fileName = directory + '/' + h + '.html'
        self.total_file += 1
        print('Create file [%d] : [%s]' % (self.total_file, h))
        with open(fileName, "wb") as file:
            file.write(html)
    
    def createDirectory(self, domain, path):
        directory = 'html/' + domain
        if(not os.path.exists(directory)):
            #print('Create directory : [%s]' % domain)
            os.makedirs(directory)

        if(len(path) != 0 and len(path) != 1):
            path_split = path.split('/')
            if(path_split[0] == ''):
                path_split.pop(0)
            path_split.pop(-1)
            for item in path_split:
                directory = directory + '/' + item
                if(not os.path.exists(directory)):
                    os.makedirs(directory)
        return directory



start_time = time.time()
site = 'http://www.ku.ac.th/web2012/index.php?c=adms&m=mainpage1'
spider = Spider(site, 10, 10000)
spider.startCrawl()
#print('Crawl [%s] Successful' % urlparse(site).netloc)
#print("--- %s seconds ---" % (time.time() - start_time))%