from ExtractLinks import ExtractLinks
import tldextract

class Spider():

    def __init__(self, extractLinks, max_depth = 2):
        self.max_depth = max_depth
        self.extractor = extractLinks
        self.crawl([self.extractor.u_parse.path], self.max_depth)

    def crawl(self, urls, max_depth):
        #urls = self.extractor.get_link(crawl_url)
        #self.url_set.union(urls)
        n_urls = set()
        if(max_depth >= 0):
            for url in urls:
                print('DEPTH : %d URL : %s' % (max_depth, url))
                link = self.extractor.get_link(url)
                n_urls = n_urls.union(link)
            self.crawl(n_urls, max_depth - 1)

extractLinks = ExtractLinks('http://ku.ac.th/web2012/index.php?c=adms&m=changepage&page=home&lang=eng')
spider = Spider(extractLinks)
#spider = Spider('http://www.gconhub.com/?page=home', extractLinks)
print('Crawl KU Successful')