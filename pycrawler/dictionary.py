import urllib

class Dictionary:
    def __init__(self):
        self.dictionary = {}
        
    def insert(self, key, value, num_pages_to_crawl):
        if self.size() >= num_pages_to_crawl:
            return 1
        else:
            normalized_link = self.__normalize_link(self.__get_redirection_url(value))

            if self.dictionary.has_key(normalized_link):
                return 2
            else:
                self.dictionary[key] = value
                return 3

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
    
    def __normalize_link(self, link):
        return urllib.quote_plus(link)
    
    def __get_redirection_url(self, link):
        return str(urllib.urlopen(link).geturl())