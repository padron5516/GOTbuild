'''
thewatchseries.to source plugin
@natko1412, 2015

'''

import re
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult



class watchseriesScraper(CommonScraper):
	broken = True
	def __init__(self):
		self._settings = {}
		self.service='watchseries'
		self.name = 'watchseries.to'
		self.referrer = 'http://thewatchseries.to'
		self.base_url = 'http://thewatchseries.to'

	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'],args['year'])
		#soup = self.request(uri, return_soup=True)
		#if soup:
		#	results = self.process_results(soup)
		return self.get_response(results)
	
	

	def process_results(self, soup):
		results = []
		rows=soup.find('div',{'id':'linktable'}).findAll('tr')		
		for i in range(0,len(rows)):
			try:
				row=rows[i]
				infos=row.findAll('td')
				domain=infos[0].getText().lower()
				link=infos[1].find('a')['href']
				host_name = domain
				if self.filter_host(host_name):
					url = "%s://%s" % (self.service, link)
					result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
					result.quality = QUALITY.UNKNOWN
					results.append(result)	
			except:
				pass
		return results
		
	

	def get_resolved_url(self, raw_url):
		url=raw_url.replace(self.base_url,'').replace('/cale.html?r=','')
		import base64
		raw_url=base64.b64decode(url)	
		return self.do_urlresolver(raw_url)
		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			showname = args[0]
			translation = [' ', '.', ]
			#showname=re.sub(r'[^\w\s]','',showname).lower().replace(" ", "_")
			#season = str(args[1]).lstrip('0')
			#episode = str(args[2]).lstrip('0')

			url='/episode/%s_s%s_e%s.html'%(showname,season,episode)
			return url
		