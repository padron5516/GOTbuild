#!/usr/bin/python
# -*- coding: utf-8 -*-
PYTHONIOENCODING="UTF-8"
import re
import json
import urllib
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult



class sezonlukdiziScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='sezonlukdizi'
		self.name = 'sezonlukdizi.com'
		self.referrer = 'http://sezonlukdizi.com/'
		self.base_url = 'http://sezonlukdizi.com/'
		self.timeout = 3

	
	def search_tvshow(self, args):
		results = []
		url = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'],args['year'])
		if url:
			html = self.request(url, append_base=True)
			results = self.process_results(html, url)
		return self.get_response(results)
	
	def process_results(self, html, referer):
		results = []
		for match in re.finditer('"?file"?\s*:\s*"([^"]+)"\s*,\s*"?label"?\s*:\s*"(\d+)p?"', html):
			stream_url, height = match.groups()
			stream_url = stream_url.replace('\\&', '&').replace('\\/', '/')
			if 'v.asp' in stream_url and 'ok.ru' not in html:
				redirect = self.request(stream_url, get_redirect=True, append_base=False)
				url = self.get_embeded_url(stream_url, user_agent=self.get_user_agent(), referer=referer)
				if 'google' in redirect or '' in redirect:
					host_name = 'gvideo'
					quality = self.test_gv_quality(redirect)
				else:
					host_name = self.service
					quality = self.test_height_quality(height)
				result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
				result.quality = self.test_gv_quality(redirect)
				results += [result]
		return results

	def get_resolved_url(self, raw_url):
		return raw_url
		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			uri = '/%s/%s-sezon-%s-bolum.html' % (args[0].replace(' ', '-'),args[1], args[2])
			html = self.request(uri)
			match1 = re.search('var\s+video_id\s*=\s*"([^"]+)', html)
			match2 = re.search('var\s+part_name\s*=\s*"([^"]+)', html)
			if match1 and match2:
				headers = {'X-Requested-With': 'XMLHttpRequest', 'Referer': self.base_url + uri}
				video_id = match1.group(1)
				part_name = match2.group(1)
				uri = '/service/get_video_part'
				data = {'video_id': video_id, 'part_name': part_name, 'page': 0}
				result = self.request(uri, data, headers=headers, return_json=True)
				if 'part_count' in result:
					part_count = result['part_count']
				if 'part' in result and 'code' in result['part']:
					match = re.search('src="([^"]+)', result['part']['code'])
					if match:
						url = match.group(1)
						return url
		return False
