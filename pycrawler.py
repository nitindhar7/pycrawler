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
init_links = parser.get_links("http://cis.poly.edu/index.htm/")
pycrawler.crawl(init_links)

# crawl
while pycrawler.get_queue_length() < int(crawl_params['num_pages_to_crawl']):
    next_url = pycrawler.next_url()
    init_links = parser.get_links(next_url)
    pycrawler.crawl(init_links)
    
    print str(pycrawler.get_queue_length()) + "\n"