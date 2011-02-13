from htmllib import HTMLParser

class PyHtmlParser(HTMLParser):

    def __init__(self, formatter):
        HTMLParser.__init__(self, formatter)
        self.links = []

    def start_a(self, attrs):
        if len(attrs) > 0:
            for attr in attrs:
                if attr[0] == "href":
                    self.links.append(attr[1])

    def get_links(self):
        return self.links