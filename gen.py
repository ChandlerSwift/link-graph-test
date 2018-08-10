#!/usr/bin/python3

import string # gen page names
import random # gen page names
import os # create directories

NUM_PAGES=int(input('how many pages to generate: '))
directory='./html'


def rand_str(length):
    return ''.join([random.choice(string.ascii_letters) for n in range(length)])

# generate pages
pages = [rand_str(12) for n in range(NUM_PAGES)]

if not os.path.exists(directory):
    os.makedirs(directory)
else:
    print('Warning: html directory already exists.')

for page in pages:
    print('Generating %s/%s.html' % (directory, page))
    linked_pages = random.sample(pages, random.randrange(NUM_PAGES))
    page_content = "<!DOCTYPE html><html><head><title>" + page + "</title></head><body>"
    for linked_page in linked_pages:
        page_content += "<a href=\"%s.html\">%s</a><br>" % (linked_page, linked_page)
    page_content += "</body></html>"
    with open(directory+'/'+page+'.html', 'w') as f:
        f.write(page_content)

# generate index page
print('Generating %s/index.html' % directory)
page_content = "<!DOCTYPE html><html><head><title>" + page + "</title></head><body>"
for page in pages:
    page_content += "<a href=\"%s.html\">%s</a><br>" % (page, page)
page_content += "</body></html>"
with open(directory+'/index.html', 'w') as f:
    f.write(page_content)
