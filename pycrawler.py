from pycrawler import parser
from urlparse import urlparse

html_parser = parser.Parser()

for link in html_parser.get_links("http://cis.poly.edu/index.htm"):
    o = urlparse(link)
    print o.netloc + ' | ' + o.path + ' | ' + html_parser.get_mime_type(link)