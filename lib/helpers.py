import sys, json, urllib

def usage():
    if (len(sys.argv) > 3):
        print "\nUSAGE: pycrawler.py n 'query'\n"
        print "       n         => number of pages to crawl"
        print "       query     => query to search (enclosed in quotes)\n"
        sys.exit()
        
def set_crawl_params():
    return { 'num_pages_to_crawl': sys.argv[1], 'query': sys.argv[2] }

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