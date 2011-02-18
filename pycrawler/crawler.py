import urllib

class Crawler:
    fileno = 0

    def __init__(self, parser, queue):
        self.__html_parser = parser
        self.__bfs_queue = queue
        
    def crawl(self, links):
        for link in links:
            # VALIDATE LINK
            
            # UNIQUENESS - dict
            
            # SAVE PAGES
            
            # SAVE LINKS
            link_queue_status = self.__bfs_queue.enqueue(self.__normalize_link(link), link)
            if link_queue_status is True:
                self.__save_page(link)

    def next_url(self):
        return self.__bfs_queue.dequeue()
    
    def display(self):
        for link in self.__bfs_queue.all():
            print link
    
    def get_queue_length(self):
        return self.__bfs_queue.size()

    # PRIVATE

    def __save_page(self, link):
        # TODO: use queue size to name files instead of fileno
        new_file = open("data/pages/" + str(self.fileno) + ".html", "w")
        page_html = self.__html_parser.get_html(link)

        if page_html is None:
            new_file.write("Link [" + link + "]: Markup not retrieved")
        else:
            new_file.write(page_html)
        
        new_file.close
        self.fileno += 1
    
    def __normalize_link(self, link):
        urllib.quote_plus(link)