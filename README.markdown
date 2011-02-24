PYCRAWLER - A simple BFS crawler in Python
==========================================

Overview
--------
Pycrawler is a python library designed to crawl the web in a breadth-first manner given a search query and the total
number of pages to crawl.

Running
-------
	python pycrawler.py [... OPTIONS ...] n 'query'
- OPTIONS: -c: Save page HTML in compressed format
- 'n': Number of pages to crawl
- 'query': Query to search. (NOTE: query has to be enclosed in quotes)
- Built on Python 2.7

Parsing
-------
Pycrawler does not parse all types of URLs. The URL extension and MIME type is used to determine whether it will be crawled.
The parsing process extracts URLs from anchor tags and image map area tags. Here is the blacklist of URLs extensions that
Pycrawler does not deal with:

1. tif/bmp/png/jpg/gif
2. js/raw/lzw/eml/cgi
3. pdf
4. mp3/avi/wma

Here is are examples of the types of URLs that Pycrawler *can* handle:

1.  cis.poly.edu
2.  cis.poly.edu/
3.  cis.poly.edu/index.html OR cis.poly.edu/default.html
4.  /
5.  /webmaster
6.  /webmaster/index.asp
7.  cis.poly.edu/poly.jpg
8.  index.html
9.  *.php/*.asp/*.cgi
10. ../products

URL Uniqueness
--------------
To save space, Pycrawler removes duplicate links from being parsed or saved. The redirection url and the originally received URLs
are compared to the internal storage structure to prevent duplication. If the redirection url cannot be retrieved, the original
URL is stored.

Server Requests
---------------
Pycrawler handles I/O socket exceptions when opening a page that was requested.
The error is handled on the microlevel and no delegation occurs. This helps speed up
the process of crawling/requesting the next page. HTML parsing errors are handled by skipping that page.

Pages that require authentication are dealt with via a custom url opener class, which is a child class of the
'FancyURLOpener' class from the 'urllib' package. When such an error occurs, Pycrawler returns nothing so that
the page is skipped.

Data
----
Pycrawler queries Google using its ajax API to retrieve the *top 8 results*. The API allows more than
8 results to be obtained granted an API Token is used.

The crawler module retrieves URLs that are crawled and pages are stored locally. The data structure
used to store urls is a combination of a simple queue and a dictionary structure. URLs are normalized before
they are stored to ensure consistency and uniqueness. Each time a link is saved, it is appended to a log file
in the 'data' folder. Crawl statistics are placed at the end of this log file. These include:
- Number of pages crawled
- Total data downloaded
- Total Time Taken (in seconds)
- HTTP return code counts (200, 401, 404 & 500)

When Pycrawler is run the with '-c' option on, page html is saved in compressed format using 'zlib' at compress level 6 (default).

Shortcomings
------------
Here is a brief list of identified features that are lacking in the current version of Pycrawler:

1.  URLs with fragments like "http://www.site.com/search#cars" are being treated as unique compared to the same URLs with the
    fragments removed even though they both point to the same webpage.
2.  The Google ajax API only retrieves 8 results. We need to add functionality so that an API token can be used to retrieve
    more than 8 top results. 
3.  Serious performance improvements need to be made:
	- Loops could potentially be combined.
	- URLs may be opened once and HTML may passed around instead of opening the page up twice.
	- Potentially retrieve the MIME TYPE when opening a URL instead of making a separate call.
4.  Increase the blacklist to include more non-parseable extensions.
5.  Allow parsing of pdfs and javascript files.
6.  Add multithreading.
7.  When a opening a url fails, we are not retrying that url. We just skip it and move on to the next one, hoping that, that page will be
    crawled elsewhere.
8.  Need to create a helper method to decompress html.
9.  Use 'getopt' to parse command line options instead of hardcoding them. Allow compress level to be entered as an argument to the '-c' flag.

Bugs
----

* The Google ajax API is returning 8 results, but not all of them are in the top 8 results. Order of results needs to be preserved.
* Have not dealt with IE relevent HTML declarations like '<..CDATA..>' or '<..!IE..>'
