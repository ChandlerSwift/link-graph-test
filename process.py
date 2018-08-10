#!/usr/bin/python3

try:
    from bs4 import BeautifulSoup
except:
    print('sudo apt install python3-bs4')

from urllib.request import urlopen
from urllib.parse import urljoin
import urllib, socket, time

start_time = time.time()

# GENERATE LINK MAP

START_URL="https://chandlerswift.com/"
SITE_RESTRICTION = "chandlerswift.com"


# Links are represented by tuples: (src, dst)
links = []

pages_to_parse = [START_URL]
pages_already_parsed = []

while len(pages_to_parse) > 0:
    page_to_parse = pages_to_parse.pop(0)
    pages_already_parsed.append(page_to_parse)
    print('parsing: ' + page_to_parse)
    try:
        html_page = urlopen(page_to_parse, timeout=.2)
        soup = BeautifulSoup(html_page, "lxml")
        for link in soup.findAll('a'):
            href = link.get('href')
            full_href = urljoin(page_to_parse, href)
            # Ensure we don't have any links outside the site we're digging through
            if SITE_RESTRICTION in full_href and SITE_RESTRICTION in page_to_parse:
                print('[%03d parsed, %05d in queue]: %s => %s' % (len(pages_already_parsed), len(pages_to_parse), page_to_parse, full_href))
                links.append((page_to_parse, full_href))
                if not (full_href in pages_to_parse or full_href in pages_already_parsed):
                    
                    pages_to_parse.append(full_href)
    # We should figure out why socket.timeout happens because it seems to be random and could skip import pages
    except (urllib.error.URLError, socket.timeout):
        print("***** COULD NOT OPEN", page_to_parse, ".***** Moving on to next page.")
        
print("Completed page parsing in", time.time() - start_time, " seconds.")
floyd_warshall_start_time = time.time()
print("Completed page parsing. Now running Floyd-Warshall")
#for link in links:
#    print("%s => %s" % link)



# This is an implementation of the Floyd-Warshall algorithm
# the result is that dist holds the shorest path between all pairs of vertices
# it's O(n^3)

num_pages = len(pages_already_parsed)

# make a N x N list of infinity
dist = [[float("infinity") for _ in range(num_pages)] for _ in range(num_pages)]
next_node = [[None for _ in range(num_pages)] for _ in range(num_pages)]

def path(start_, end_):
    start = start_
    end = end_
    if next_node[start][end] == None:
        return []
    path = [start]
    while start != end:
        start = next_node[start][end]
        path.append(start)

    return path

def find_min_and_index(nested_list):
    minimum = float("infinity")
    index = (None, None)
    for i, single_list in enumerate(nested_list):
        for j, value in enumerate(single_list):
            if value < minimum:
                minimum = value
                index = (i,j)
    
    return (minimum, index)


for link in links:
    u = pages_already_parsed.index(link[0])
    v = pages_already_parsed.index(link[1])
    dist[u][v] = -1
    next_node[u][v] = v



for x in range(num_pages):
    dist[x][x] = 0

#print("Node:",next_node)
for k in range(num_pages):
    for i in range(num_pages):
        for j in range(num_pages):
            if i != j:
                #print("Path:",k,i,j,path(i,j)),
                i_to_k = set(path(i,k))
                k_to_j = set(path(k,j))
                # We remove k because we know it is always in both lists
                # so we can properly test for non-disjointness
                if len(i_to_k) != 0:
                    i_to_k.remove(k)
                if dist[i][j] > dist[i][k] + dist[k][j] and i_to_k.isdisjoint(k_to_j):
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]
                    #print("Node:",next_node,"Dist:",dist)



#print("Pages:",pages_already_parsed)
#print("Next_node:",next_node)
minimum, indices = find_min_and_index(dist)
longest_path = path(indices[0],indices[1])
print("Longest path:",[pages_already_parsed[page_index] for page_index in longest_path])
#print("Dist:",dist)
print("Completed floyd-warshall in",time.time() - floyd_warshall_start_time, "seconds.")
print("Total time:", time.time() - start_time)





