from parser import Parser
from queue import Queue
from dictionary import Dictionary
from link import Link
from datetime import datetime
import lib, sys, zlib, time

class Crawler:
    fileno = 0
    total_data_downloaded = 0
    total_status_200 = 0
    total_status_401 = 0
    total_status_404 = 0
    total_status_500 = 0

    def __init__(self, max_links_allowed, compress_status):
        self.__html_parser = Parser()
        self.__bfs_tree = Queue()
        self.__unique_links = Dictionary(max_links_allowed)
        self.__compress = compress_status
        self.__pyurlopener = lib.PyURLOpener()
        self.__start_time = datetime.now()

    def format_validate_and_save_links(self, links_to_crawl, base_link, depth):
        links_to_crawl = self.__remove_duplicates(links_to_crawl)

        for link in links_to_crawl:
            link_to_process = Link(link, depth)
            link_to_process.fix_relative_link(base_link)
            link_to_process.set_link_attrs()
            link_to_process.remove_duplicate_link(self.__unique_links)
            link_to_process.remove_invalid_link()
            link_to_process.remove_uncrawlable_link()
            self.__save_link(link_to_process)

    def crawl(self):
        next_link = self.__next_url()
        links_to_crawl = self.__html_parser.get_links(next_link.redirected)
        return {'links_to_crawl': links_to_crawl, 'next_link': next_link.redirected, 'depth': (next_link.depth + 1)}

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
            self.__bfs_tree.enqueue(link)
    
            crawled_urls = open("data/crawled_urls.txt", "a+")
            
            if insert_status:
                file_size = self.__save_page(link)
                self.__save_url(link, file_size, crawled_urls)
            else:
                crawled_urls.write(self.__stats())
                crawled_urls.close
                sys.exit()
            
            crawled_urls.close

    def __save_page(self, link):
        new_file = open("data/pages/" + str(self.fileno) + ".html", "w")
        page_html = link.opened.read()

        if page_html is None:
            page_html = "Link [" + link.redirected + "]: HTML not retrieved"
        else:
            page_html = link.redirected + "\n\n" + page_html
        
        if self.__compress:
            new_file.write(zlib.compress(page_html))
        else:
            new_file.write(page_html)

        new_file_size = new_file.tell()
        self.__update_stats(new_file_size, link.code)

        link.opened.close()
        new_file.close

        return new_file_size

    def __save_url(self, link, file_size, crawled_urls):
        crawled_urls.write("[" + time.asctime(time.localtime(time.time())) + "][" + self.__to_mb(file_size) + " MB][" + str(link.code) + "][" + str(link.depth) + "] " + link.redirected + "\n")

    def __next_url(self):
        return self.__bfs_tree.dequeue()

    def __stats(self):
        time_taken = datetime.now() - self.__start_time
        
        stats =  "\nCrawl Stats:"
        stats += "-------------------------------------\n"
        stats += "- Pages crawled:   " + str(self.__unique_links.size()) + " pages\n" 
        stats += "- Data downloaded: " + self.__to_mb(self.total_data_downloaded) + " MB\n"
        stats += "- Time Taken:      " + str(time_taken.seconds) + " seconds\n"
        stats += "- HTTP 200 count:  " + str(self.total_status_200) + "\n"
        stats += "- HTTP 401 count:  " + str(self.total_status_401) + "\n"
        stats += "- HTTP 404 count:  " + str(self.total_status_404) + "\n"
        stats += "- HTTP 500 count:  " + str(self.total_status_500)
        return stats
    
    def __update_stats(self, new_file_size, code):
        self.fileno += 1
        self.total_data_downloaded += new_file_size
        
        if code == 200:
            self.total_status_200 += 1
        elif code == 401:
            self.total_status_401 += 1
        elif code == 404:
            self.total_status_404 += 1
        elif code == 500:
            self.total_status_500 += 1

    def __to_mb(self, bytes):
        return '%.3f' % (float(bytes) / 1048576)