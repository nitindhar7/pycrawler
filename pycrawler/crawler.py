from parser import Parser
from queue import Queue
from dictionary import Dictionary
from urlparse import urlparse, urljoin
import urllib, sys

class Crawler:
    INVALID_EXTENSIONS = ['tif', 'bmp', 'png', 'jpg', 'gif', 'js', 'pdf', 'mp3', 'avi', 'wma', 'raw','lzw', 'eml']
    VALID_MIME_TYPES = ['text/html', 'text/plain', 'text/xml', 'application/xhtml+xml']
    fileno = 0
    total_data_downloaded = 0
        
    def __init__(self, max_links_allowed):
        self.__html_parser = Parser()
        self.__bfs_tree = Queue()
        self.__unique_links = Dictionary(max_links_allowed)
    
    def format_validate_and_save_links(self, links_to_crawl, base_link):
        links_to_crawl = self.__remove_duplicates(links_to_crawl)

        for index in range(len(links_to_crawl)):
            links_to_crawl[index] = self.__fix_relative_link(links_to_crawl[index], base_link)
            links_to_crawl[index] = self.__get_redirection_link(links_to_crawl[index])
            links_to_crawl[index] = self.__remove_duplicate_link(links_to_crawl[index])
            links_to_crawl[index] = self.__remove_invalid_link(links_to_crawl[index])
            self.__save_link(links_to_crawl[index])
        
        return [link for link in links_to_crawl if link is not None]       
    
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
            return str(urllib.urlopen(link).geturl())
        except IOError:
            return link
    
    def __remove_duplicate_link(self, link):
        if link is None: return link
        
        normalized_link = self.__normalize_link(link)
        if self.__unique_links.link_already_exists(normalized_link):
            return None
        else:
            return link
    
    def __remove_invalid_link(self, link):
        if link is None: return link

        if link[-4:].lower() in self.INVALID_EXTENSIONS:
            return None
        elif self.__html_parser.get_mime_type(link) not in self.VALID_MIME_TYPES:
            return None
        else:
            return link
    
    def __save_link(self, link):
        if link is not None:
            insert_status = self.__unique_links.insert(self.__normalize_link(link), link)
            self.__bfs_tree.enqueue(link)
    
            if insert_status == 1:
                self.__display_stats()
                sys.exit()
            if insert_status == 3:
                self.__save_page(link)
                self.__save_url(link)

    def __normalize_link(self, link):
        return urllib.quote_plus(link)

    def __save_page(self, link):
        new_file = open("data/pages/" + str(self.fileno) + ".html", "w")
        page_html = self.__html_parser.get_html(link)

        if page_html is None:
            new_file.write("Link [" + link + "]: HTML not retrieved")
        else:
            new_file.write(link + "\n\n" + page_html)
        
        self.fileno += 1
        self.total_data_downloaded += new_file.tell()
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