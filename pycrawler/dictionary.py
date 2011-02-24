class Dictionary:
    def __init__(self, max_links_allowed):
        self.dictionary = {}
        self.max_size = int(max_links_allowed)
        
    def insert(self, key, value):
        if self.size() >= self.max_size:
            return False
        else:
            self.dictionary[key] = value
            return True

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