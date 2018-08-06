#!/usr/bin/python3

import string # gen page names
import random # gen page names

NUM_PAGES=int(input('how many pages to generate: '))

def rand_str(length):
    return ''.join([random.choice(string.ascii_letters) for n in range(length)])

# generate pages
pages = [rand_str(12) for n in range(NUM_PAGES)]

for page in pages:
    linked_pages = random.sample(pages, random.randrange(NUM_PAGES))
    page_content = "<!DOCTYPE html><html><head><title>" + page + "</title></head><body>"
    for linked_page in linked_pages:
        page_content += "<a href=\"/%s.html\">%s</a><br>" % (linked_page, linked_page)
    page_content += "</body></html>"
    with open(page+'.html', 'w') as f:
        f.write(page_content)

