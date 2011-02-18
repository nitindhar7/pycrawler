from urlparse import urlparse
import urllib

class Crawler:
    VALID_EXTENTIONS = ['htm', 'html']
    VALID_MIME_TYPES = ['text/html', 'text/plain', 'text/xml', 'application/xhtml+xml']
    fileno = 0
        
    def __init__(self, parser, queue):
        self.__html_parser = parser
        self.__bfs_queue = queue
        self.__dictionary = {} 
    
    def crawl(self, links):
        for link in links:
            # VALIDATE LINK
            if self.validate(link) is False:
                continue
            
            # UNIQUENESS - dict
           # keys = self.__normalize_link(link)
           # if self.__dictionary.has_key(keys):
            #    continue
            #else:
                #print keys
             #   self.__dictionary[keys] = link;
                               
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
    
    def __validate(self, link):
        '''
         TYPES OF LINKS:
         1.  cis.poly.edu
         2.  cis.poly.edu/
         3.  cis.poly.edu/index.html OR cis.poly.edu/default.html
         4.  /
         5.  /webmaster
         6.  /webmaster/index.asp
         7.  ../webmaster/index.html
         8.  cis.poly.edu/poly.jpg
         9.  index.html
         10. *.php/*.asp/*.cgi
         
         PLAN: whitelist extentions/mime_types and only allow the extentions/mime_types that are allowed to be used.
        '''
        parsed_link = urlparse(link)
        extention = parsed_link.path.split('.').pop()
        mime_type = self.__html_parser.get_mime_type(link)
        
        # CHECK EXTENTIONS
        if extention not in self.VALID_EXTENTIONS:
            return False
        
        # CHECK MIME TYPES
        if mime_type not in self.VALID_MIME_TYPES:
            return False
        
        # FORMAT LINKS
        
        
        return True
