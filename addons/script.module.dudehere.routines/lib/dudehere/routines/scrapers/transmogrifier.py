import xbmcaddon
import xbmcgui
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult
from dudehere.routines.vfs import VFSClass
vfs = VFSClass()
def validate_transmogrifier():
	try:
		installed = xbmcaddon.Addon('service.transmogrifier').getSetting('enable_transmogrifier') == "true"
		if installed:
			return ADDON.get_setting('enable_transmogrifier') == "true"
	except:
		return False

class transmogrifierScraper(CommonScraper):
	def __init__(self):
		self.service='transmogrified'
		self.name = 'transmogrified'
		self.referrer = 'http://localhost'
		self.base_url = 'http://localhost'
		self.is_cachable = False
		self.broken = validate_transmogrifier() == False
		try:
			self.working_dir = xbmcaddon.Addon('service.transmogrifier').getSetting('save_directory')
		except:
			self.working_dir = ''
			
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		path = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'])
		if path:
			results = self.process_results(path)
		return self.get_response(results)
	
	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		path = self.prepair_query('movie', args['title'], args['year'])
		if path:
			results = self.process_results(path)
		return self.get_response(results)
	
	def process_results(self, path):
		results = []
		url = "%s://%s" % (self.service, path)
		result = ScraperResult(self.debrid_hosts, self.service, 'transmogrified', url)
		result.quality = QUALITY.LOCAL
		result.size = vfs.get_size(path)
		result.extension = self.extension
		results += [result]
		return results
	
	def get_resolved_url(self, raw_url):
		resolved_url = raw_url
		win = xbmcgui.Window(10000)
		win.setProperty('GenericPlaybackService.Path', resolved_url)
		return resolved_url
		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			for self.extension in ['avi', 'mkv', 'mov', 'mp4', 'flv']:
				path = vfs.join(self.working_dir, "TV Shows/%s S%sE%s.%s" % (args[0], str(args[1]).zfill(2), str(args[2]).zfill(2), self.extension))
				if vfs.exists(path):
					return path
				path = vfs.join(self.working_dir, "TV Shows/%s %sx%s.%s" % (args[0], args[1], args[2], self.extension))
				if vfs.exists(path):
					return path
			return False
		else:
			for self.extension in ['avi', 'mkv', 'mov', 'mp4', 'flv']:
				path = vfs.join(self.working_dir,"Movies/%s (%s).%s" % (args[0], args[0], self.extension))
				if vfs.exists(path):
					return path
			return False
		return path
