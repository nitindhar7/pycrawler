PYCRAWLER - A simple BFS crawler in Python
==========================================

Overview
--------
Pycrawler is a python library designed to crawl the web in a breadth-first manner.

Running
-------
python pycrawler.py n 'query'

- n: Number of pages to crawl
- 'query': Query to search. (NOTE: query has to be enclosed in quotes)

File Types
----------
Pycrawler does not parse all types of URLs. Here is the blacklist of URLs extensions that Pycrawler does not deal with:

1. tif/bmp/png/jpg/gif
2. js
3. pdf
4. mp3/avi/wma

Here is a list of URLs that Pycrawler *can* handle:

1.  cis.poly.edu
2.  cis.poly.edu/
3.  cis.poly.edu/index.html OR cis.poly.edu/default.html
4.  /
5.  /webmaster
6.  /webmaster/index.asp
7.  ../webmaster/index.html
8.  cis.poly.edu/poly.jpg
9.  index.html
10. *.php/*.asp/*.cgi
         
MIME TYPE is also used to determine whether a page is allowed or not.

Server Requests
---------------
Pycrawler handles I/O socket exceptions when opening a page that was requested.
The error is handled on the microlevel and no delegation occurs. This helps speed up
the process of crawling/requesting the next page. 

Data
----
Pycrawler queries Google using its ajax API to retrieve the *top 8 results*. The API allows more than
8 results to be obtained granted an API Token is used.

The crawler module retrieves URLs that are crawled and stored pages are locally. The data structure
used to store urls is a simple queue using the Python dictionary structure. URLs are normalized before
they are stored to ensure consistency and uniqueness.

Shortcomings
------------
Here is a brief list of identified features that are lacking in the current version of Pycrawler:

1. URLs with fragments like "http://www.site.com/search#cars" are being treated as unique compared to the same URLs with the
   fragments removed even though they both point to the same webpage.
2. The Google ajax API only retrieves the top 8 results. We need to add functionality so that an API token can be used to retrieve
   over 8 top results. 
3. Serious performance improvements need to be made:
	- Loops could potentially be combined.
	- URLs may be opened once and HTML may passed around instead of opening the page up twice.
	- Potentially retrieve the MIME TYPE when opening a URL instead of making a separate call.

Bugs
----

* Number of pages being saved is more than number of pages to crawl requested.