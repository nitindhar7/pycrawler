class Queue:
    
    def __init__(self):
        self.queue = []
        
    def enqueue(self, normalized_link, link):
        if normalized_link in dict(self.queue):
            return False
        else:
            self.queue.append( (normalized_link, link) )
            return True

    def dequeue(self):
        tmp = self.queue[0]
        del self.queue[0]
        return tmp[1]
    
    def size(self):
        return len(self.queue)
    
    def all(self):
        return self.queue