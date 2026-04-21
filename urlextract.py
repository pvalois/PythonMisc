#!/usr/bin/python3 

import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-i","--stdin",action="store_true", default=False)
parser.add_argument("--url", type=str, default=None)
args = parser.parse_args()

url = args.url

if args.stdin:
    response = sys.stdin.read()
else:
    http = httplib2.Http()
    user_agent = {'User-agent': 'Mozilla/5.0'}

    url = args.url if ("http") in args.url else f"http://{url}"
    status, response = http.request(url, headers=user_agent)

soup = BeautifulSoup(response,"html.parser")

anchors={'a':{'href'},
         'area':{'href'},
         'base':{'href'},
         'img':{'src','href'},
         'body':{'background'},
         'frame':{'src'},
         'iframe':{'src'},
         'overlay':{'src'},
         'scrpts':{'src'},
         'embed':{'src'},
         'bgsound':{'src'},
         'applet':{'code'}}

glob=[]

for ank in anchors:
  for line in soup.find_all(ank):
    for key in anchors[ank]:
      if line.get(key):
        link=line.get(key)
        if link not in glob:
          glob.append(link)

for link in sorted(glob):
    if (args.url and not link.startswith("http")):
        link=f"{url}{link}"
    print (link)
