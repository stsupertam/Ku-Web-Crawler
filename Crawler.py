from ExtractLinks import ExtractLinks
import tldextract

class Spider():

    def __init__(self, seed_url, extractLinks, max_depth = 2):
        self.seed_url = seed_url
        self.max_depth = max_depth
        self.extractor = extractLinks
        self.crawl([self.seed_url], self.max_depth)

    def crawl(self, urls, max_depth):
        #urls = self.extractor.get_link(crawl_url)
        #self.url_set.union(urls)
        n_urls = set()
        if(max_depth >= 0):
            for url in urls:
                link = self.extractor.get_link(url)
                n_urls = n_urls.union(link)
                print('URL DEPTH %d : %s' % (max_depth, url))
            self.crawl(n_urls, max_depth - 1)

extractLinks = ExtractLinks('https://www.cpe.ku.ac.th/')
links = extractLinks.get_link('/')
#spider = Spider('http://www.ku.ac.th/web2012/index.php?c=adms&m=changepage&page=home&lang=eng', extractLinks)
#spider = Spider('http://www.gconhub.com/?page=home', extractLinks)
print('Crawl KU Successful')