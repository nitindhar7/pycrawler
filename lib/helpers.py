import sys

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