from htmllib import HTMLParser
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

    def get_links(self, url):
        self.__get_markup(url)
        return self.__links
    
    def get_mime_type(self, url):
        return urllib.urlopen(url).info().gettype()
    
    # PRIVATE
    
    def __get_markup(self, url):
        self.markup = urllib.urlopen(url)
        
        self.feed(self.markup.read())
        self.close()