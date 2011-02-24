import urllib

class PyURLOpener(urllib.FancyURLopener):
    
    def http_error_401(self, url, fp, errcode, errmsg, headers, data = None):
        return None