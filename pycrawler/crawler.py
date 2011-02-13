class Crawler:
    fileno = 0
    
    def __init__(self, parser, queue):
        self.__html_parser = parser
        self.__bfs_queue = queue
        
    def crawl(self, links):
        for link in links:
            self.__save_page(link)
            self.__bfs_queue.enqueue(link)
    
    def display(self):
        for link in self.__bfs_queue.all():
            print link

    # PRIVATE

    def __save_page(self, link):
        new_file = open("data/pages/" + str(self.fileno) + ".html", "w")
        new_file.write(self.__html_parser.get_html(link))
        new_file.close
        self.fileno += 1