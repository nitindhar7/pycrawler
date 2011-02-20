import sys

class Dictionary:
    def __init__(self):
        self.dictionary = {}
        
    def insert(self, key, value, num_pages_to_crawl):
        if self.size() >= num_pages_to_crawl:
            print "\n\nDone Crawling [" + str(num_pages_to_crawl) + "] pages.\n"
            sys.exit()
        
        self.dictionary[key] = value

    def remove(self, key):
        tmp = self.dictionary[key]
        del self.dictionary[key]
        return tmp
    
    def size(self):
        return len(self.dictionary)
    
    def all(self):
        return self.dictionary
    
    def link_already_exists(self, normalized_link):
        return self.dictionary.has_key(normalized_link)