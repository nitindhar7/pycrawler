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
Pycrawler does not parse URLs with the following suffixes:

1. tif/bmp/png/jpg/gif
2. js
3. pdf
4. mp3/avi/wma

Server Requests
---------------
Pycrawler handles I/O socket exceptions when opening a page that was requested.
The error is handled on the microlevel and no delegation occurs. This helps speed up
the process of crawling/requesting the next page. 

Data
----
The crawler module retrieves URLs that are crawled and stored pages are locally. The data structure
used to store urls is a simple queue using the Python dictionary structure. URLs are normalized before
they are stored to ensure consistency and uniqueness.

Bugs
----
