from htmllib import HTMLParser, HTMLParseError
from urlparse import urlparse
import lib, formatter, robotparser

class Parser(HTMLParser, HTMLParseError):

    def __init__(self):
        self.__links = []
        self.__markup = ''
        self.__parser = HTMLParser.__init__(self, formatter.NullFormatter())
        self.__robotparser = robotparser.RobotFileParser()
        self.__pyurlopener = lib.PyURLOpener()

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
    
    def get_links(self, link):
        self.__get_markup(link)
        return self.__links
        
    def clear(self):
        del self.__links[:]
    
    def can_crawl(self, link):
        parsed_link = urlparse(link)
        robot_file_path = parsed_link.scheme + "://" + parsed_link.netloc + "/robots.txt"
        self.__robotparser.set_url(robot_file_path)
        self.__robotparser.read()
        return self.__robotparser.can_fetch("*", link)

    # PRIVATE

    def __get_markup(self, link):
        try:
            self.feed(self.__pyurlopener.open(link).read())
            self.close()
        except IOError:
            self.close()
        except HTMLParseError:
            self.close()