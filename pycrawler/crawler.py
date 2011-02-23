from parser import Parser
from queue import Queue
from dictionary import Dictionary
from urlparse import urlparse
import urllib, sys

class Crawler:
    INVALID_EXTENSIONS = ['tif', 'bmp', 'png', 'jpg', 'gif', 'js', 'pdf', 'mp3', 'avi', 'wma']
    VALID_MIME_TYPES = ['text/html', 'text/plain', 'text/xml', 'application/xhtml+xml']
    fileno = 0
    total_data_downloaded = 0
        
    def __init__(self):
        self.__html_parser = Parser()
        self.__bfs_tree = Queue()
        self.__unique_links = Dictionary()
        
    def convert_to_redirected_urls(self, links_to_crawl):
        for index in range(len(links_to_crawl)):
            links_to_crawl[index] = self.__get_redirection_url(links_to_crawl[index])
            
        return links_to_crawl

    def remove_duplicates(self, links_to_crawl):
        return list(set(links_to_crawl))

    def format_links(self, links_to_crawl, base_link):
        if base_link is not None:
            parsed_base_link = urlparse(base_link)
        
        for index in range(len(links_to_crawl)):
            parsed_link = urlparse(links_to_crawl[index])
            if parsed_link.netloc == '':
                links_to_crawl[index] = parsed_base_link.scheme + '://' + parsed_base_link.netloc + links_to_crawl[index]
        
        return links_to_crawl
    
    def remove_nonunique_links(self, links_to_crawl):
        for index in range(len(links_to_crawl)):
            normalized_link = self.__normalize_link(links_to_crawl[index])
            if self.__unique_links.link_already_exists(normalized_link):
                links_to_crawl[index] = None

        return [link for link in links_to_crawl if link is not None]

    def validate_links(self, links_to_crawl):
        for index in range(len(links_to_crawl)):
            extension = links_to_crawl[index][-4:]
            mime_type = self.__html_parser.get_mime_type(links_to_crawl[index])
            
            if extension in self.INVALID_EXTENSIONS:
                links_to_crawl[index] = None

            if mime_type not in self.VALID_MIME_TYPES:
                links_to_crawl[index] = None
               
        return [link for link in links_to_crawl if link is not None]
    
    def save_links(self, links_to_crawl, num_pages_to_crawl):
        for link in links_to_crawl:
            insert_status = self.__unique_links.insert(self.__normalize_link(link), link, num_pages_to_crawl)
                        
            if insert_status == 1:
                self.__display_stats()
                sys.exit()
            if insert_status == 3:
                self.__bfs_tree.enqueue(link)
                self.__save_page(link)
                self.__save_url(link)       
    
    def crawl(self):
        next_link = self.__next_url()
        links_to_crawl = self.__html_parser.get_links(next_link)
        return {'links_to_crawl': links_to_crawl, 'next_link': next_link}
    
    def clear(self):
        self.__html_parser.clear()

    def display(self):
        #print self.__unique_links.all()
        for link in self.__bfs_tree.all(): print link + "\n\n"
        
    def get_num_links_saved(self):
        return self.__unique_links.size()

    # PRIVATE

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
    
    def __normalize_link(self, link):
        return urllib.quote_plus(link)
    
    def __display_stats(self):
        print "\nCrawl Stats:"
        print "-------------------------------------"
        print "- Pages crawled:   " + str(self.__unique_links.size()) + " pages"
        print "- Data downloaded: " + self.__to_mb(self.total_data_downloaded) + " MB"
    
    def __to_mb(self, bytes):
        return '%.2f' % (float(bytes) / 1048576)
    
    def __get_redirection_url(self, link):
        return str(urllib.urlopen(link).geturl())