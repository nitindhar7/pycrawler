from pycrawler import Parser
from pycrawler import Crawler
from pycrawler import Queue 
from pycrawler import Dictionary
import lib

# Boot pycrawler
crawl_params = lib.boot()

# Create resources
parser = Parser()
queue = Queue()
dictionary = Dictionary()
pycrawler = Crawler(parser, queue, dictionary) 

# initial settings
pycrawler.crawl(lib.get_google_results(crawl_params['query']))

# crawl
while pycrawler.get_queue_length() < int(crawl_params['num_pages_to_crawl']):
    links_to_crawl = parser.get_links(pycrawler.next_url())
    pycrawler.crawl(links_to_crawl)
    parser.clear()