from urlparse import urlparse, urljoin
import lib, urllib

class Link:

    INVALID_EXTENSIONS = ['tif', 'bmp', 'png', 'jpg', 'gif', 'js', 'pdf', 'mp3', 'avi', 'wma', 'raw','lzw', 'eml', 'cgi']
    VALID_MIME_TYPES = ['text/html', 'text/plain', 'text/xml', 'application/xhtml+xml']

    def __init__(self, link):
        self.depth = 0
        self.original = link
        self.opened = None
        self.redirected = None
        self.normalized = None
        self.__pyurlopener = lib.PyURLOpener()
    
    def fix_relative_link(self, base_link):
        if urlparse(self.original).netloc == '' and base_link is not None:
            self.original = urljoin(base_link, self.original)
    
    def get_redirection_link(self):
        try:
            self.opened = self.__pyurlopener.open(self.original)
            self.redirected = self.opened.geturl()
            self.normalized = urllib.quote_plus(self.redirected)
        except IOError:
            self.opened = None
            self.redirected = None
            self.normalized = None
    
    def remove_duplicate_link(self, unique_links):
        if self.redirected is not None:
            if unique_links.link_already_exists(self.normalized):
                self.opened = None
                self.redirected = None
                self.normalized = None
    
    def remove_invalid_link(self):
        if self.redirected is not None:
            if self.redirected[-4:].lower() in self.INVALID_EXTENSIONS:
                self.opened = None
                self.redirected = None
                self.normalized = None
            if self.__get_mime_type(self.opened) not in self.VALID_MIME_TYPES:
                self.opened = None
                self.redirected = None
                self.normalized = None

    # PRIVATE
    
    def __get_mime_type(self, opened):
        # http://en.wikipedia.org/wiki/Internet_media_type
        try:
            return opened.info().gettype()
        except IOError:
            return None