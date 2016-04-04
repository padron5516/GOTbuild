# coding: utf-8

import requests
import base64
import json

browser = requests.session()
headers = {'Content-Type': 'application/json',
           'trakt-api-version': '2',
           'trakt-api-key': base64.urlsafe_b64decode(
               'ZWI0MWU5NTI0M2Q4Yzk1MTUyZWQ3MmExZmMwMzk0YzkzY2I3ODVjYjMzYWVkNjA5ZmRkZTFhMDc0NTQ1ODRiNA==')}

response = browser.get('https://api-v2launch.trakt.tv/movies/trending', headers=headers)

data = response.json()

print data

# from urllib2 import Request, urlopen
# request = Request('https://api-v2launch.trakt.tv/movies/trending', headers=headers)
# response_body = urlopen(request).read()
#
# print response_body
