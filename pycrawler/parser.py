from htmllib import HTMLParser
import urllib, formatter, httplib

class Parser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self, formatter.NullFormatter())
        self.__links = []
        self.__markup = ''

    def start_a(self, attrs):
        if len(attrs) > 0:
            for attr in attrs:
                if attr[0] == "href" and attr[1] != '#':
                    self.__links.append(attr[1])
    
    def start_area(self, attrs):
        if len(attrs) > 0:
            for attr in attrs:
                if attr[0] == "href" and attr[0] != '#':
                    self.__links.append(attr[1])
    
    def get_links(self, url):
        self.__get_markup(url)
        return self.__links

    def get_mime_type(self, url):
        # http://en.wikipedia.org/wiki/Internet_media_type
        try:
            file_type = urllib.urlopen(url).info().gettype()
        except IOError:
            return None
        except httplib.InvalidURL:
            return None
        else:
            return file_type
    
    def get_html(self, url):
        try:
            self.markup = urllib.urlopen(url)
            self.close()
        except IOError:
            return None
        else:
            return self.markup.read()
        
    def clear(self):
        del self.__links[:]
    
    # PRIVATE

    def __get_markup(self, url):
        try:
            self.markup = urllib.urlopen(url)
            self.feed(self.markup.read())
        except IOError:
            return None
        else:
            return self.close()