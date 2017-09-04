import sys
import getopt
from Crawler import Spider
from urllib.parse import urlparse

def main():
    site = 'http://www.ku.ac.th/web2012/index.php?c=adms&m=mainpage1'
    spider = Spider(site, 100, 30000)
    spider.startCrawl()
    print('Crawl [%s] Successful' % urlparse(site).netloc)

if __name__ == "__main__":
    main()