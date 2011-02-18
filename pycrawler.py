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
pycrawler.crawl(lib.get_google_results(crawl_params['query']))

# crawl
while pycrawler.get_queue_length() < int(crawl_params['num_pages_to_crawl']):
    links_to_crawl = parser.get_links(pycrawler.next_url())
    pycrawler.crawl(links_to_crawl)
    # TODO: clear the tmp list in Parser