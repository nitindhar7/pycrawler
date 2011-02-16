from htmllib import HTMLParser
from urlparse import urlparse
import urllib, formatter

class Parser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self, formatter.NullFormatter())
        self.__links = []
        self.__markup = ''

    def start_a(self, attrs):
        if len(attrs) > 0:
            for attr in attrs:
                if attr[0] == "href":
                    self.__links.append(attr[1])
    
    def start_area(self, attrs):
        if len(attrs) > 0:
            for attr in attrs:
                if attr[0] == "href":
                    self.__links.append(attr[1])
    
    def get_links(self, url):
        self.__get_markup(url)
        self.__format_links(url)
        return self.__links

    def get_mime_type(self, url):
        return urllib.urlopen(url).info().gettype()
    
    def get_html(self, url):
        self.markup = urllib.urlopen(url)
        self.close()
        return self.markup.read()
    
    # PRIVATE

    def __get_markup(self, url):
        self.markup = urllib.urlopen(url)
        self.feed(self.markup.read())
        self.close()

    def __format_links(self, base_url):
        parsed_base_url = urlparse(base_url)

        for index in range(len(self.__links)):
            tmp_parsed_link = urlparse(self.__links[index])
            if tmp_parsed_link.netloc == '':
                self.__links[index] = parsed_base_url.scheme + '://' + parsed_base_url.netloc + self.__links[index]