'''
tvonline.tw source plugin
@natko1412, 2015

'''

import re
import urllib
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult



class tvonlineScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='tvonline'
		self.name = 'tvonline.tw'
		self.referrer = 'http://tvonline.tw'
		self.base_url = 'http://tvonline.tw'

	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'],args['year'])
		if uri:
			html = self.request(uri)
			results = self.process_results(html)
		return self.get_response(results)
	

	def process_results(self, html):
		results = []
		pattern = "go_to\(\d+,'([^']+)"
		for match in re.finditer(pattern, html, re.DOTALL):
			href = match.group(1)
			host_name = self.get_domain_from_url(href)
			if self.filter_host(host_name):
				url = "%s://%s" % (self.service, href)
				result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
				result.quality = QUALITY.UNKNOWN
				results += [result]

		return results
	
		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			showname = self.url_friendly(args[0])
			uri = "/%s-%s/season-%s-episode-%s/" % (showname, args[3], args[1], args[2])
			return uri
		else:
			return False
