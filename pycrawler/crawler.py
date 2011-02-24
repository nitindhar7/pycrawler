from parser import Parser
from queue import Queue
from dictionary import Dictionary
from urlparse import urlparse, urljoin
import lib, urllib, sys, zlib

class Crawler:
    INVALID_EXTENSIONS = ['tif', 'bmp', 'png', 'jpg', 'gif', 'js', 'pdf', 'mp3', 'avi', 'wma', 'raw','lzw', 'eml', 'cgi']
    VALID_MIME_TYPES = ['text/html', 'text/plain', 'text/xml', 'application/xhtml+xml']
    fileno = 0
    total_data_downloaded = 0

    def __init__(self, max_links_allowed, compress_status):
        self.__html_parser = Parser()
        self.__bfs_tree = Queue()
        self.__unique_links = Dictionary(max_links_allowed)
        self.__compress = compress_status
        self.__pyurlopener = lib.PyURLOpener()

    def format_validate_and_save_links(self, links_to_crawl, base_link):
        links_to_crawl = self.__remove_duplicates(links_to_crawl)

        for link in links_to_crawl:
            link                         = self.__fix_relative_link(link, base_link)
            link_info                    = self.__get_redirection_link(link)
            link_info['redirected_link'] = self.__remove_duplicate_link(link_info)
            link_info['redirected_link'] = self.__remove_invalid_link(link_info)
            self.__save_link(link_info)

    def crawl(self):
        next_link = self.__next_url()
        links_to_crawl = self.__html_parser.get_links(next_link)
        return {'links_to_crawl': links_to_crawl, 'next_link': next_link}

    def clear(self):
        self.__html_parser.clear()

    def display(self):
        print self.__unique_links.all()

    def get_num_links_saved(self):
        return self.__unique_links.size()

    # PRIVATE

    def __remove_duplicates(self, links_to_crawl):
        return list(set(links_to_crawl))

    def __fix_relative_link(self, link, base_link):
        if urlparse(link).netloc == '' and base_link is not None:
            return urljoin(base_link, link)
        else:
            return link

    def __get_redirection_link(self, link):
        try:
            opened_link = self.__pyurlopener.open(link)
            return {'opened_link': opened_link, 'redirected_link': str(opened_link.geturl()), 'normalized_link': self.__normalize_link(link)}
        except IOError:
            return {'opened_link': None, 'redirected_link': None, 'normalized_link': None}

    def __remove_duplicate_link(self, link_info):
        if link_info['redirected_link'] is not None:
            if self.__unique_links.link_already_exists(link_info['normalized_link']):
                return None
            else:
                return link_info['redirected_link']

    def __remove_invalid_link(self, link_info):
        if link_info['redirected_link'] is not None:
            if link_info['redirected_link'][-4:].lower() in self.INVALID_EXTENSIONS:
                return None
            elif self.__get_mime_type(link_info['opened_link']) not in self.VALID_MIME_TYPES:
                return None
            else:
                return link_info['redirected_link']

    def __save_link(self, link_info):
        if link_info['redirected_link'] is not None:
            insert_status = self.__unique_links.insert(link_info['normalized_link'], link_info['redirected_link'])
            self.__bfs_tree.enqueue(link_info['redirected_link'])
    
            if insert_status:
                self.__save_url(link_info['redirected_link'])
                self.__save_page(link_info['redirected_link'], link_info['opened_link'])
            else:
                self.__display_stats()
                sys.exit()

    def __normalize_link(self, link):
        return urllib.quote_plus(link)

    def __save_page(self, link, opened_link):
        new_file = open("data/pages/" + str(self.fileno) + ".html", "w")
        page_html = opened_link.read()

        if page_html is None:
            page_html = "Link [" + link + "]: HTML not retrieved"
        else:
            page_html = link + "\n\n" + page_html
        
        if self.__compress:
            new_file.write(zlib.compress(page_html))
        else:
            new_file.write(page_html)
        
        self.fileno += 1
        self.total_data_downloaded += new_file.tell()
        
        opened_link.close()
        new_file.close

    def __save_url(self, link):
        new_file = open("data/crawled_urls.txt", "a+")
        new_file.write(link + "\n")
        new_file.close

    def __next_url(self):
        return self.__bfs_tree.dequeue()

    def __display_stats(self):
        print "\nCrawl Stats:"
        print "-------------------------------------"
        print "- Pages crawled:   " + str(self.__unique_links.size()) + " pages"
        print "- Data downloaded: " + self.__to_mb(self.total_data_downloaded) + " MB"

    def __to_mb(self, bytes):
        return '%.2f' % (float(bytes) / 1048576)

    def __get_mime_type(self, opened_link):
        # http://en.wikipedia.org/wiki/Internet_media_type
        try:
            return opened_link.info().gettype()
        except IOError:
            return None