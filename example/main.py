#!/usr/bin/python
# filename: run.py
import re
from crawler import Crawler

if __name__ == "__main__": 
    # Using SQLite as a cache to avoid pulling twice
    crawler = Crawler()
    crawler.crawl('http://www.ku.ac.th/web2012/index.php?c=adms&m=changepage&page=home&lang=eng')