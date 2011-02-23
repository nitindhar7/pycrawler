from pycrawler import Crawler
import lib

# Boot pycrawler
crawl_params = lib.boot()
prev_link = None

# Initialize crawler
pycrawler = Crawler() 

# Retrieve initial links from Google Web Search
links_to_crawl = lib.get_google_results(crawl_params['query'])

# crawl
while True:

    # Remove any duplicate links that were provided
    links_to_crawl = pycrawler.remove_duplicates(links_to_crawl)

    # Format links to ensure proper URL format
    links_to_crawl = pycrawler.format_links(links_to_crawl, prev_link)

    # Check if link was already stored
    # Ensure that the link is a html page and/or has acceptable MIME types
    links_to_crawl = pycrawler.remove_nonunique_and_invalid_links(links_to_crawl)
    
    # Convert all urls to their respective redirected urls
    links_to_crawl = pycrawler.convert_to_redirected_urls(links_to_crawl)

    # Save links to BFS Tree for crawling. Stop when # of URLs saved > 'num_pages_to_crawl'
    pycrawler.save_links(links_to_crawl, int(crawl_params['num_pages_to_crawl']))
      
    # Crawl new link in BFS manner
    crawl_results = pycrawler.crawl()
    
    # Collect new list of links to crawl. Retrieve previous link that was crawled
    links_to_crawl = crawl_results['links_to_crawl'][:]
    prev_link = crawl_results['next_link']

    # Clear temp internal storage
    pycrawler.clear()