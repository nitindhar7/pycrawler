from pycrawler import Parser
from pycrawler import Crawler
from pycrawler import Queue 
import lib

# Boot pycrawler
crawl_params = lib.boot()

# Create resources
parser = Parser()
queue = Queue()
pycrawler = Crawler(parser, queue)

# initial settings
links_to_crawl = parser.get_links("http://cis.poly.edu/index.htm/")
pycrawler.crawl(links_to_crawl)

# crawl
while pycrawler.get_queue_length() < int(crawl_params['num_pages_to_crawl']):
    links_to_crawl = parser.get_links(pycrawler.next_url())
    pycrawler.crawl(links_to_crawl)