#!/usr/bin/python

import lib

format = lib.get_formatter()
html_parser = lib.get_parser(format)
html = lib.get_html("http://cis.poly.edu/index.htm")
html_parser = lib.parse_html(html, html_parser)
links = html_parser.get_links()
print links