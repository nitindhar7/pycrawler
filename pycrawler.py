from pycrawler import Crawler
import lib

# Boot pycrawler
crawl_params = lib.boot()
next_link = None

# Initialize crawler
pycrawler = Crawler(crawl_params['num_pages_to_crawl'], crawl_params['compress'])

# Retrieve initial links from Google Web Search
links_to_crawl = lib.get_google_results(crawl_params['query'])

# Crawl until 'num_pages_to_crawl' are saved
while True:
    # Remove any duplicate links that were provided
    # Format links to ensure proper URL format
    # Convert all urls to their respective redirected urls
    # Check if link was already stored
    # Ensure that the link is a html page and/or has acceptable MIME types
    # Save links to BFS Tree for crawling. Stop when # of URLs saved > 'num_pages_to_crawl'
    pycrawler.format_validate_and_save_links(links_to_crawl, next_link)
      
    # Crawl next link in BFS manner
    crawl_results = pycrawler.crawl()
    
    # Collect new list of links to crawl. Retrieve previous link that was crawled
    links_to_crawl = crawl_results['links_to_crawl'][:]
    next_link = crawl_results['next_link']

    # Clear temp internal storage
    pycrawler.clear()