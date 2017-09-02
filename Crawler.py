# -*- coding: utf-8 -*-

import os
import hashlib
import time
import sys
import requests
import tldextract
from bs4 import BeautifulSoup
from urllib import robotparser
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.parse import unquote

class Spider():

    def __init__(self, url, max_depth = 2, total_pages = 100):
        self.max_depth = max_depth
        self.url = url
        self.total_pages = total_pages
        self.pages = 0
        self.files = 0
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
        if(split_domain[0] == 'www'):
            split_domain = split_domain[1:]
            domain = str.join('.', split_domain)
        
        if(domain not in self.domain_sets):
            self.domain_sets.add(domain)
            try: 
                robot = requests.get(('%s://%s/robots.txt' % (self.scheme, domain)), timeout=5)
                robot_code = robot.status_code
                if(robot_code == requests.codes.ok):
                    print('Robots.txt Found [%s]' % (domain))
                    self.domain_robots[domain] = True
                    with open('./robotlists.txt', 'a') as file:
                        file.write(domain + '\n')
            except Exception:
                print('Cannot Get Robots.txt [Error Exception : %s] [%s]' % (sys.exc_info()[0], domain, ))
            
        if(tldextract.extract(self.domain).domain == tldextract.extract(domain).domain):
            #print('[Domain] [%s][%s]' % (domain, u_path))
            if(domain in self.domain_robots):
                rp = robotparser.RobotFileParser()
                rp.set_url('%s://%s/robots.txt' % (self.scheme, domain))
                rp.read()
                if(not rp.can_fetch('*', ('%s://%s%s' % (self.scheme, domain, url)))):
                    return links
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
                        print('Retrieving [Failed] [Code : %d] [%s] %s' % (status_code, domain, url))
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
                print('Retrieving [Failed] [Error Exception : %s] [%s] %s' % (sys.exc_info()[0], domain, url))

        return links

    def writeToFile(self, domain, path, soup):
        directory = self.createDirectory(domain, path)
        html = soup.prettify('utf-8')
        h = hashlib.md5(html).hexdigest()
        fileName = directory + '/' + h + '.html'
        self.files += 1
        print('Create file [%d] : [%s]' % (self.files, h))
        with open(fileName, "wb") as file:
            file.write(html)
    
    def createDirectory(self, domain, path):
        directory = 'html/' + domain
        path = unquote(path)
        os.makedirs(directory, exist_ok=True)

        if(len(path) != 0 and len(path) != 1):
            path_split = path.split('/')
            if(path_split[0] == ''):
                path_split.pop(0)
            path_split.pop(-1)
            path = str.join('/', path_split)
            directory = directory + '/' + path
            os.makedirs(directory, exist_ok=True)
        return directory

start_time = time.time()
site = 'http://www.ku.ac.th/web2012/index.php?c=adms&m=mainpage1'
spider = Spider(site, 30, 10000)
spider.startCrawl()
print('Crawl [%s] Successful' % urlparse(site).netloc)
print("--- %s seconds ---" % (time.time() - start_time))