from pycrawler import Crawler
import lib

# Boot pycrawler
crawl_params = lib.boot()

# Initialize crawler
pycrawler = Crawler() 

# Retrieve initial links from Google Web Search
links_to_crawl = lib.get_google_results(crawl_params['query'])

# crawl
while pycrawler.get_num_links_saved() < int(crawl_params['num_pages_to_crawl']):

    # Format links to ensure proper URL format
    links_to_crawl = pycrawler.format_links(links_to_crawl)

    # Check if link was already stored
    links_to_crawl = pycrawler.remove_nonunique_links(links_to_crawl)

    # Ensure that the link is a html page and/or has acceptable MIME types
    links_to_crawl = pycrawler.validate_links(links_to_crawl)

    # Save links to BFS Tree for crawling
    pycrawler.save_links(links_to_crawl, int(crawl_params['num_pages_to_crawl']))

    # Crawl new link in BFS manner
    links_to_crawl = pycrawler.crawl()
    
    pycrawler.display()