#!/usr/bin/python3

try:
    from bs4 import BeautifulSoup
except:
    print('sudo apt install python3-bs4')

from urllib.request import urlopen
from urllib.parse import urljoin

# GENERATE LINK MAP

START_URL="http://link-graph-test.test/"

# Links are represented by tuples: (src, dst)
links = []

pages_to_parse = [START_URL]
pages_already_parsed = []

while len(pages_to_parse) > 0:
    page_to_parse = pages_to_parse.pop(0)
    pages_already_parsed.append(page_to_parse)
    #print('parsing: ' + page_to_parse)

    html_page = urlopen(page_to_parse)
    soup = BeautifulSoup(html_page, "lxml")
    for link in soup.findAll('a'):
        href = link.get('href')
        full_href = urljoin(page_to_parse, href)
        links.append((page_to_parse, full_href))
        if not (full_href in pages_to_parse or full_href in pages_already_parsed):
            pages_to_parse.append(full_href)

for link in links:
    print("%s => %s" % link)
