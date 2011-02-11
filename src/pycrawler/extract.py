import urllib

def extract(url):
    html = urllib.urlopen(url)
    return html