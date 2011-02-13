from pycrawler import Parser
from pycrawler import Crawler
from pycrawler import Queue

html_parser = Parser()
init_links = html_parser.get_links("http://cis.poly.edu/index.htm")

pycrawler = Crawler(html_parser, Queue())
pycrawler.crawl(init_links)
pycrawler.display()

#html_parser.get_mime_type(link)