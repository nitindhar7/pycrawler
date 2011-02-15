from pycrawler import Parser
from pycrawler import Crawler
from pycrawler import Queue 
import sys
import lib

crawl_params = lib.boot()

'''
html_parser = Parser()
init_links = html_parser.get_links("http://cis.poly.edu/index.htm/")
__no_of_links = len(init_links)

while __no_of_links < 160:
    pycrawler = Crawler(html_parser, Queue())
    pycrawler.crawl(init_links)
    pycrawler.display()
    url_name = pycrawler.extract()
    init_links = html_parser.get_links(url_name)
    __no_of_links += len(init_links);
    print init_links 
    print __no_of_links;
'''