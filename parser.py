from htmllib import HTMLParser
import urllib

class Parser(HTMLParser):

    def __init__(self, formatter):
        HTMLParser.__init__(self, formatter.NullFormatter())
        self.__links = []
        self.markup = ''

    def start_a(self, attrs):
        print len(attrs)
        if len(attrs) > 0:
            for attr in attrs:
                if attr[0] == "href":
                    self.links.append(attr[1])

    def get_links(self, url):
        self.__get_markup(self, url)
        return self.links
    
    # PRIVATE
    
    def __get_markup(self, url):
        self.markup = urllib.urlopen(url)
        self.feed(self.markup.read())
        self.close()