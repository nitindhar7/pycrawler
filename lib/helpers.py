import sys, json, urllib

def usage():
    if len(sys.argv) > 4:
        print "\nUSAGE: pycrawler.py [OPTIONS] n 'query'\n"
        print "       [OPTIONS] => -c: save page HTML as compressed"
        print "       n         => number of pages to crawl"
        print "       query     => query to search (enclosed in quotes)\n"
        sys.exit()
        
def set_crawl_params():
    if '-c' in sys.argv or '-C' in sys.argv:
        return { 'num_pages_to_crawl': sys.argv[2], 'query': sys.argv[3], 'compress': True}
    else:
        return { 'num_pages_to_crawl': sys.argv[2], 'query': sys.argv[3], 'compress': False}

def boot():
    usage()
    return set_crawl_params()

def get_google_results(query):
    google_results = []
    query = urllib.urlencode({'q': query})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=8&%s' % query
    results = json.loads(urllib.urlopen(url).read())
    for result in results['responseData']['results']: google_results.append(str(result['url']))
    return google_results