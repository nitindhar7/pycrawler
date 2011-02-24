from urlparse import urlparse, urljoin
import lib, urllib, robotparser

class Link:

    INVALID_EXTENSIONS = ['tif', 'bmp', 'png', 'jpg', 'gif', 'js', 'pdf', 'mp3', 'avi', 'wma', 'raw','lzw', 'eml', 'cgi']
    VALID_MIME_TYPES = ['text/html', 'text/plain', 'text/xml', 'application/xhtml+xml']

    def __init__(self, link):
        self.depth = 0
        self.original = link
        self.__nullify_link()
        self.__pyurlopener = lib.PyURLOpener()
        self.__robotparser = robotparser.RobotFileParser()
    
    def fix_relative_link(self, base_link):
        if urlparse(self.original).netloc == '' and base_link is not None:
            self.original = urljoin(base_link, self.original)
    
    def get_redirection_link(self):
        try:
            self.opened = self.__pyurlopener.open(self.original)
            self.redirected = self.opened.geturl()
            self.normalized = urllib.quote_plus(self.redirected)
        except IOError:
            self.__nullify_link()
    
    def remove_duplicate_link(self, unique_links):
        if self.redirected is not None:
            if unique_links.link_already_exists(self.normalized):
                self.__nullify_link()
    
    def remove_invalid_link(self):
        if self.redirected is not None:
            if self.redirected[-4:].lower() in self.INVALID_EXTENSIONS:
                self.__nullify_link()
            if self.__get_mime_type(self.opened) not in self.VALID_MIME_TYPES:
                self.__nullify_link()
    
    def remove_uncrawlable_link(self):
        if self.redirected is not None:
            parsed_link = urlparse(self.opened.geturl())
            robot_file_path = parsed_link.scheme + "://" + parsed_link.netloc + "/robots.txt"
            self.__robotparser.set_url(robot_file_path)
            self.__robotparser.read()
            
            crawling_allowed = self.__robotparser.can_fetch(self.__pyurlopener.version, self.redirected)
            
            if not crawling_allowed:
                self.__nullify_link()

    # PRIVATE
    
    def __get_mime_type(self, opened):
        # http://en.wikipedia.org/wiki/Internet_media_type
        try:
            return opened.info().gettype()
        except IOError:
            return None

    def __nullify_link(self):
        self.opened = None
        self.redirected = None
        self.normalized = None