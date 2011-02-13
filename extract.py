import urllib, formatter, py_html_parser.PyHtmlParser

def get_html(url):
    return urllib.urlopen(url)

def get_formatter():
    return formatter.NullFormatter()

def get_parser(format):
    return py_html_parser.PyHtmlParser(format)

def get_links(html_parser):
    return html_parser.get_links()

def parse_html(html, html_parser):
    html_parser.feed(html.read())
    html_parser.close()
    return html_parser