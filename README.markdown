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
Pycrawler queries Google using its ajax API to retrieve the top 8 results. The API allows more than
8 results to be obtained granted an API Token is used.

The crawler module retrieves URLs that are crawled and stored pages are locally. The data structure
used to store urls is a simple queue using the Python dictionary structure. URLs are normalized before
they are stored to ensure consistency and uniqueness.

Bugs
----
