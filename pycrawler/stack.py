class Stack:
    
    def __init__(self):
        self.stack = []
        
    def push(self, object):
        self.stack.append(object)
        
    def pop(self):
        tmp = self.stack[-1]
        del self.stack[-1]
        return tmp
    
    def size(self):
        return len(self.stack)