class Dictionary:
    
    def __init__(self):
        self.dictionary = {}
        
    def insert(self, key, value):
        self.dictionary[key] = value

    def remove(self, key):
        tmp = self.dictionary[key]
        del self.dictionary[key]
        return tmp
    
    def size(self):
        return len(self.dictionary)
    
    def all(self):
        return self.dictionary