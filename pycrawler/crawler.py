from parser import Parser
from queue import Queue
from dictionary import Dictionary
from link import Link
import lib, sys, zlib

class Crawler:
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
            link_to_process = Link(link)
            link_to_process.fix_relative_link(base_link)
            link_to_process.get_redirection_link()
            link_to_process.remove_duplicate_link(self.__unique_links)
            link_to_process.remove_invalid_link()
            link_to_process.remove_uncrawlable_link()
            self.__save_link(link_to_process)

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

    def __save_link(self, link):
        if link.redirected is not None:
            insert_status = self.__unique_links.insert(link.normalized, link.redirected)
            self.__bfs_tree.enqueue(link.redirected)
    
            if insert_status:
                self.__save_url(link.redirected)
                self.__save_page(link.redirected, link.opened)
            else:
                self.__display_stats()
                sys.exit()

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