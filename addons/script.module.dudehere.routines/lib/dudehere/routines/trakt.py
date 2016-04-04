import urllib2, urllib
import socket
from urllib2 import URLError, HTTPError
from datetime import datetime
import re, time
import json
import hashlib
import base64
import traceback
import xbmcgui, xbmc
from dudehere.routines import *
from dudehere.routines.omdbapi import OMDBapi
from dudehere.routines.constants import WINDOW_ACTIONS
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
BASE_URL = "http://api-v2launch.trakt.tv"
CLIENT_ID = ADDON.get_setting('trakt_client_id')
SECRET_ID = ADDON.get_setting('trakt_secret')
PIN_URL = ADDON.get_setting('trakt_pin_url')
DAYS_TO_GET = 21
DECAY = 2
from dudehere.routines import *
from dudehere.routines.vfs import VFSClass
from dudehere.routines.database import SQLiteDatabase as DatabaseAPI
vfs = VFSClass()
omdb = OMDBapi()

class MyDatabaseAPI(DatabaseAPI):
	def _initialize(self):
		import xbmcaddon
		root = xbmcaddon.Addon('script.module.dudehere.routines').getAddonInfo('path')
		schema_file = vfs.join(root, 'resources/database/trakt.schema.sql')
		if self.run_script(schema_file, commit=False):
			self.execute('DELETE FROM version WHERE 1')
			self.execute('INSERT INTO version(db_version) VALUES(?)', [self.db_version])
			self.commit()

	def do_init(self):
		do_init = True
		try:
			test = self.query("SELECT 1 FROM version WHERE db_version >= ?", [self.db_version], silent=True)
			if test:
				do_init = False
		except:
			do_init = True
		return do_init

		
DB_LOCATION = vfs.join('special://userdata', 'addon_data/script.module.dudehere.routines')
if not vfs.exists(DB_LOCATION):
	vfs.mkdir(DB_LOCATION)
DB_FILE = vfs.join('special://userdata', 'addon_data/script.module.dudehere.routines/trakt.db')
DB = MyDatabaseAPI(DB_FILE, version=7, connect=True)


class TraktError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		try:
			s = self.value
		except Exception,e:
			print "-----",type(e),e
		return s
	
class TraktTempError(Exception):
	pass

class AuthWindow(xbmcgui.WindowXMLDialog):
		message = False
		def __init__(self, *args, **kwargs):
				xbmcgui.WindowXML.__init__(self)
			
		def onInit(self):
			self.response = False
			self.getControl(82004).setVisible(False)
			if self.message:
				self.getControl(82002).setLabel(self.message)

		def onAction(self, action):
			action = action.getId()
			if action in [WINDOW_ACTIONS.ACTION_PREVIOUS_MENU, WINDOW_ACTIONS.ACTION_NAV_BACK]:
				self.close()
			
			try:
				if action in [WINDOW_ACTIONS.ACTION_SHOW_INFO, WINDOW_ACTIONS.ACTION_CONTEXT_MENU]:
					controlID = self.getFocus().getId()
			except:
				pass
			
		def onClick(self, controlID):
			trakt = TraktAPI()
			if controlID in [82000]:
				trakt.set_property('Abort', "true")
				self.close()
			if controlID == 82001:
				trakt.set_property('Abort', "false")
				self.getControl(82004).setVisible(True)
				self.response = trakt._authorize(window=self)
				if self.response:
					self.close()

		def onFocus(self, controlID):
			pass


class TraktAPI():
	def __init__(self):
		self.token = None
		self.timeout = 30
		self.limit = 100
	
	def get_property(self, k):
		p = xbmcgui.Window(10000).getProperty('GenericPlaybackService.' + k)
		if p == 'false': return False
		if p == 'true': return True
		return p
	
	def set_property(self, k, v):
		xbmcgui.Window(10000).setProperty('GenericPlaybackService.' + k, v)
	
	def clear_property(self, k):
		xbmcgui.Window(10000).clearProperty('GenericPlaybackService.' + k)
	
	def authorize(self, window):
		response = self._authorize(window=window)
		return response
	
	def get_settings(self):
		uri = '/users/settings'
		settings = self._call(uri, auth=True)
		if not settings: return False
		return settings
	
	def get_object_id(self, trakt_id = None, imdb_id=None, tmdb_id=None, id_type='trakt'):
		if trakt_id is not None: return trakt_id
		if imdb_id is not None: return imdb_id
		uri = '/search'
		result = self._call(uri, params={"id_type": 'tmdb_id', "id": tmdb_id})
		if not result: return False
		type = result[0]['type']
		return result[0][type]['ids']['id_type']
	
	def resolve_imdb_id(self, title, year, media, tmdb_id='', trakt_id=''):
		imdb_id = None
		try:
			id = DB.query("SELECT imdb_id FROM id_cache WHERE title=? AND media=? AND year=?", [title, media, year])
			if id:
				imdb_id = id[0]
			else:
				imdb_id = omdb.query_id(title, year, media)
				if imdb_id is not None:
					DB.execute("INSERT INTO id_cache(title, year, media, imdb_id, tmdb_id, trakt_id) VALUES(?,?,?,?,?,?)", [title, year, media, imdb_id, tmdb_id, trakt_id])
					DB.commit()
		except Exception, e:
			ADDON.log(e)
		return imdb_id
	

		
	def query_id(self, id_type, id):
		uri = '/search'
		result = self._call(uri, params={"id_type": id_type, "id": id})
		if not result: return False
		type = result[0]['type']
		return result[0][type]['ids']['imdb']
	
	def query_slug(self, id_type, id):
		uri = '/search'
		result = self._call(uri, params={"id_type": id_type, "id": id})
		if not result: return False
		type = result[0]['type']
		return result[0][type]['ids']['slug']
	
	def lookup(self, media, id, id_type='imdb'):
		uri = '/search'
		record = self._call(uri, params={"id_type": id_type, "id": id, 'extended': 'full,images'})
		if not record: return False
		metadata = self.process_record(record, media)
		return metadata
	
	def get_episode_details(self, id, season, episode, params={'extended': 'full,images'}):
		uri = '/shows/%s/seasons/%s/episodes/%s' % (id, season, episode)
		episode = self._call(uri, params=params, auth=False, cache_limit=0)
		show = self.get_show_details(id)
		record = {"episode": episode, "show": show}
		return self.process_record(record, media='episode')
	
	def get_show_details(self, id):
		uri = '/shows/%s' % id
		record = self._call(uri, params={'extended': 'full,images'}, auth=False, cache_limit=0)
		return record
	
	def get_movie_details(self, id):
		uri = '/movies/%s' % (id)	
		record = self._call(uri, params={'extended': 'full,images'}, auth=False, cache_limit=0)
		if not record: return False
		return self.process_record(record, media='movie')
	
	def get_metadata(self, media, imdb_id, tmdb_id, trakt_id, slug, season=None, episode=None):
		metadata = None
		if media == 'episode':
			return self.get_episode_metadata(imdb_id, tmdb_id, trakt_id, slug, season, episode)
		elif media == 'tvshow':
			return self.get_show_metadata(imdb_id, tmdb_id, trakt_id, slug)
		else:
			return self.get_movie_metadata(imdb_id, tmdb_id, trakt_id, slug)
	
	def get_episode_metadata(self, imdb_id, tmdb_id, trakt_id, slug, season, episode):
		metadata = None
		cached = False
			
		if imdb_id != 'None' and imdb_id != '':
			SQL = "SELECT cache FROM episode_cache WHERE imdb_id=? AND season=? AND episode=? LIMIT 1"
			cached = DB.query(SQL, [imdb_id, season, episode])
		elif tmdb_id != 'None' and tmdb_id != '':
			SQL = "SELECT cache FROM episode_cache WHERE tmdb_id=? AND season=? AND episode=? LIMIT 1"
			cached = DB.query(SQL, [tmdb_id, season, episode])
		elif slug != 'None' and slug != '':
			SQL = "SELECT cache FROM episode_cache WHERE slug=? AND season=? AND episode=? LIMIT 1"
			cached = DB.query(SQL, [slug, season, episode])
		elif trakt_id != 'None' and trakt_id != '':
			SQL = "SELECT cache FROM episode_cache WHERE trakt_id=? AND season=? AND episode=? LIMIT 1"
			cached = DB.query(SQL, [trakt_id, season, episode])	

		if cached:
			cached = json.loads(cached[0])
			cached['cast'] = []
			ADDON.log('Loading cached metadata')
			return cached
		
		ADDON.log('Requesting metadata')
		if slug:
			return self.get_episode_details(slug, season, episode)
		if trakt_id:
			return self.get_episode_details(trakt_id, season, episode)
		if imdb_id:
			return self.get_episode_details(imdb_id, season, episode)
		if tmdb_id:
			imdb_id = self.query_id('tmdb', tmdb_id)
			return self.get_episode_details(imdb_id, season, episode)
		return metadata
	
	def get_show_metadata(self, imdb_id, tmdb_id, trakt_id, slug):
		metadata = None
		cached = False
		
		if imdb_id != 'None' and imdb_id != '':
			SQL = "SELECT cache FROM show_cache WHERE imdb_id=? LIMIT 1"
			cached = DB.query(SQL, [imdb_id])
		elif tmdb_id != 'None' and tmdb_id != '':
			SQL = "SELECT cache FROM show_cache WHERE tmdb_id=? LIMIT 1"
			cached = DB.query(SQL, [tmdb_id])
		elif slug != 'None' and slug != '':
			SQL = "SELECT cache FROM show_cache WHERE slug=? LIMIT 1"
			cached = DB.query(SQL, [slug])
		elif trakt_id != 'None' and trakt_id != '':
			SQL = "SELECT cache FROM show_cache WHERE trakt_id=? LIMIT 1"
			cached = DB.query(SQL, [trakt_id])
			
		if cached:
			cached = json.loads(cached[0])
			cached['cast'] = []
			ADDON.log('Loading cached metadata')
			return cached
		ADDON.log('Requesting metadata')
		if slug:
			return self.get_show_details(slug)
		if imdb_id:
			return self.get_show_details(imdb_id)
		if tmdb_id:
			imdb_id = self.query_id('tmdb', tmdb_id)
			return self.get_show_details(imdb_id)
		if trakt_id:
			return self.get_show_details(trakt_id)
		return metadata
	
	def get_movie_metadata(self, imdb_id, tmdb_id, trakt_id, slug):
		metadata = None
		cached = False
		
		if imdb_id != 'None' and imdb_id != '':
			SQL = "SELECT cache FROM movie_cache WHERE imdb_id=? LIMIT 1"
			cached = DB.query(SQL, [imdb_id])
		elif tmdb_id != 'None' and tmdb_id != '':
			SQL = "SELECT cache FROM movie_cache WHERE tmdb_id=? LIMIT 1"
			cached = DB.query(SQL, [tmdb_id])
		elif slug != 'None' and slug != '':
			SQL = "SELECT cache FROM movie_cache WHERE slug=? LIMIT 1"
			cached = DB.query(SQL, [slug])
		elif trakt_id != 'None' and trakt_id != '':
			SQL = "SELECT cache FROM movie_cache WHERE trakt_id=? LIMIT 1"
			cached = DB.query(SQL, [trakt_id])
			
		if cached:
			cached = json.loads(cached[0])
			cached['cast'] = []
			ADDON.log('Loading cached metadata')
			return cached
		ADDON.log('Requesting metadata')
		if slug:
			return self.get_movie_details(slug)
		if imdb_id:
			return self.get_movie_details(imdb_id)
		if tmdb_id:
			imdb_id = self.query_id('tmdb', tmdb_id)
			return self.get_movie_details(imdb_id)
		if trakt_id:
			return self.get_movie_details(trakt_id)
		return metadata
		
	def search(self, query, media='show'):
		uri = '/search'
		return self._call(uri, params={'query': query, 'type': media, 'extended': 'full,images'}, cache_limit=86600)
		
	def get_calendar_shows(self):
		from datetime import date, timedelta
		d = date.today() - timedelta(days=(DAYS_TO_GET - 1)) 
		today = d.strftime("%Y-%m-%d")
		uri = '/calendars/my/shows/%s/%s' % (today, DAYS_TO_GET)
		media='episode'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=60, auth=True)
	
	def get_calendar_daily_shows(self, delta=0, number=1):
		from datetime import date, timedelta
		d = date.today() - timedelta(days=delta)
		start_date = d.strftime("%Y-%m-%d")
		uri = '/calendars/my/shows/%s/%s' % (start_date, number)
		media='episode'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=60, auth=True)
	
	def get_calendar_episodes(self, delta=0, number=1):
		from datetime import date, timedelta
		d = date.today() - timedelta(days=delta)
		start_date = d.strftime("%Y-%m-%d")
		uri = '/calendars/all/shows/%s/%s' % (start_date, number)
		media='episode'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=60, auth=False)
	
	def get_calendar(self, calendar, delta=0, number=1):
		from datetime import date, timedelta
		d = date.today() - timedelta(days=delta)
		start_date = d.strftime("%Y-%m-%d")
		uri = '/calendars/%s/%s/%s' % (calendar, start_date, number)
		media='episode'
		auth = calendar.startswith("my")
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=60, auth=auth)
		
	def get_similar_tvshows(self, id):
		uri = '/shows/%s/related' % id
		media = 'show'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=86600, auth=False)
	
	def get_collected_tvshows(self):
		uri = '/sync/collection/shows'
		media='show'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=60, auth=True)
	
	def get_trending_tvshows(self):
		uri = '/shows/trending'
		media='show'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=60, auth=False)
	
	def get_anticipated_tvshows(self):
		uri = '/shows/anticipated'
		media='show'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=60, auth=False)
	
	def get_popular_tvshows(self):
		uri = '/shows/popular'
		media='show'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=60, auth=False)
	
	def get_recommended_tvshows(self):
		uri = '/recommendations/shows'
		media='show'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=60, auth=True)
	
	def get_show_seasons(self, id):
		uri = '/shows/%s/seasons' % id
		media='season'
		return self._call(uri, params={'extended': 'images'}, cache_limit=86600)
	
	def get_show_episodes(self, id, season):
		uri = '/shows/%s/seasons/%s' % (id, season)
		media='episode'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=86600)
	
	def get_episodes_ondeck(self, slug=None):
		ondeck = []
		shows = False
		if slug is None or slug=='watchlist':
			shows = self.get_watchlist_tvshows()
		else:
			shows = self.get_custom_list(slug, 'tvshows',  params={'extended': ''})
		if not shows: return []
		
		for show in shows:
			slug = show['show']['ids']['slug']
			imdb_id = show['show']['ids']['imdb']
			tmdb_id = show['show']['ids']['tmdb']
			trakt_id = show['show']['ids']['trakt']
			next = self.get_next_episode(slug)
			if next:
				season = next['season']
				episode = next['number']
				if season == 0 or episode == 0: continue
				episode = self.get_episode_metadata(imdb_id, tmdb_id, trakt_id, slug, season, episode)
				ondeck.append( episode )
		return ondeck

	
	
	def get_next_episode(self, slug):
		uri = '/shows/%s/progress/watched' % slug
		result = self._call(uri, params={"hidden": "false", "specials":"false"}, auth=True)
		if result['next_episode'] is None:
			return False
		return result['next_episode']

	
	def get_watchlist_tvshows(self, extended='full,images', simple=False, id_type='imdb'):
		uri = '/users/me/watchlist/shows'
		a = self.check_activities()
		if simple:
			records = self.cache_request(a['shows']['watchlisted_at'], 'shows_watchlisted_at_simple', uri, auth=True)
			if not records: return {id_type: []}
			return [record['show']['ids'][id_type] for record in records] + [record['show']['ids']['slug'] for record in records]
		else:
			results = self.cache_request(a['shows']['watchlisted_at'], 'shows_watchlisted_at', uri, params={'extended': extended}, auth=True)
			return results
	
	def get_watchlist_movies(self, extended='full,images', simple=False, id_type='imdb'):
		uri = '/users/me/watchlist/movies'
		a = self.check_activities()
		if simple:
			records = self.cache_request(a['movies']['watchlisted_at'], 'movies_watchlisted_at_simple', uri, auth=True)
			if not records: return {id_type: []}
			return [record['movie']['ids'][id_type] for record in records]  + [record['movie']['ids']['slug'] for record in records]
		else:
			results = self.cache_request(a['movies']['watchlisted_at'], 'movies_watchlisted_at', uri, params={'extended': extended}, auth=True)
			return results
			
	def get_collected_movies(self):
		uri = '/sync/collection/movies'
		media='movie'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=60, auth=True)
	
	def get_trending_movies(self):
		uri = '/movies/trending'
		media='movie'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=60, auth=False)
	
	def get_popular_movies(self):
		uri = '/movies/popular'
		media = 'movie'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=60, auth=False)
	
	def get_recommended_movies(self):
		uri = '/recommendations/movies'
		media = 'movie'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=60, auth=True)
	
	def get_similar_movies(self, id):
		uri = '/movies/%s/related' % id
		media = 'movie'
		return self._call(uri, params={'extended': 'full,images'}, cache_limit=86600, auth=False)
	
	def get_show_info(self, id, episodes=False):
		if episodes:
			uri = '/shows/%s/seasons' % id
			return self._call(uri, params={'extended': 'episodes,full'}, cache_limit=86600)
		else:
			uri = '/shows/%s' % id
			return self._call(uri, cache_limit=86600)
	
	def get_custom_lists(self):
		uri = '/users/me/lists'
		results = self._call(uri, params={}, auth=True)
		if not results: return False
		return sorted(results)
	
	def get_liked_lists(self):
		uri = '/users/likes/lists'
		return sorted(self._call(uri, params={}, auth=True))
	
	def get_custom_list(self, slug, media, username=None, params={'extended': 'full,images'}):
		if media=='tvshows': media = 'show'
		if media=='tv': media = 'show'
		if username is None:	
			uri = '/users/me/lists/%s/items' % slug 
			auth = True
		else:
			uri = '/users/%s/lists/%s/items' % (username.replace('.', '-'), slug)
			auth = False
		temp = self._call(uri, params=params, auth=auth)
		results = []
		if not temp: return results
		for r in temp:
			if r['type'] == media:
				results.append(r)
		return results		
	
	def create_custom_list(self, title):
		uri = '/users/me/lists'
		post_dict = {
			"name": title,
			"description": "Created by %s" % ADDON_NAME,
			"privacy": "public",
			"display_numbers": True,
			"allow_comments": True
		}
		return self._call(uri, data=post_dict, auth=True)
	
	def add_to_watchlist(self, media, id, id_type='imdb'):
		uri = '/sync/watchlist'
		data = {media:  [{'ids': {id_type: id}}]}
		return self._call(uri, data, auth=True)
	
	def delete_from_watchlist(self, media, id, id_type='imdb'):
		uri = '/sync/watchlist/remove'
		data = {media:  [{'ids': {id_type: id}}]}
		return self._call(uri, data, auth=True)
		
	def add_to_custom_list(self, media, slug, id, id_type='imdb'):
		if media=='movie':
			post_dict = {'movies': [{'ids': {id_type: id}}]}
		else:
			post_dict = {'shows': [{'ids': {id_type: id}}]}
		uri = '/users/me/lists/%s/items' % slug
		return self._call(uri, data=post_dict, auth=True)
	
	def delete_from_custom_list(self, media, slug, id, id_type='imdb'):
		if media=='movie':
			post_dict = {'movies': [{'ids': {id_type: id}}]}
		else:
			post_dict = {'shows': [{'ids': {id_type: id}}]}
		uri = '/users/me/lists/%s/items/remove' % slug
		return self._call(uri, post_dict, auth=True)
	
	def delete_custom_list(self, slug):
		uri = '/users/me/lists/%s' % slug
		return self._delete(uri)
	
	def toggle_sync_state(self, name, slug):
		test = DB.query("SELECT 1 FROM sync_states WHERE slug=?", [slug])
		if test:
			DB.execute("UPDATE sync_states SET sync=ABS(sync - 1) WHERE slug=?", [slug])
		else:
			DB.execute("INSERT INTO sync_states(name, slug) VALUES (?,?)", [name, slug])
		DB.commit()
	
	def get_sync_state(self, slug):
		test = DB.query("SELECT sync FROM sync_states WHERE slug=?", [slug])
		if test and test[0] == 1:
			return True
		else:
			return False
	
	def get_sync_lists(self):
		return DB.query_assoc("SELECT name, slug FROM sync_states WHERE sync=1", force_double_array=True)
		
	def set_watched_state(self, media, id, watched, season=None, id_type='imdb'):
		uri = '/sync/history' if watched else '/sync/history/remove'
		if media == 'episode':
			post_dict = {'episodes': [{"ids": {"trakt": id}}]}
		elif media == 'movie':
			post_dict = {'movies': [{"ids": {id_type: id}}]}
		elif media == 'season':
			post_dict = {'shows': [{'seasons': [{'number': int(season)}], 'ids': {id_type: id}}]}
		return self._call(uri, post_dict, auth=True)
	
	def get_watched_history(self, media):
		uri = '/sync/watched/%s' % media
		if media == 'shows':
			results = {}
			response = self._call(uri, auth=True)
			if not response: return False
			for r in response:
				imdb_id =  r['show']['ids']['imdb']
				results[imdb_id] = {}
				seasons = r['seasons']
				for season in seasons:
					results[imdb_id][season['number']] = []
					for episode in season['episodes']: results[imdb_id][season['number']].append(episode['number'])
			return results
		else:
			results = {"imdb": [], "tmdb": [], "trakt": []}
			response = self._call(uri, auth=True)
			if not response: return False
			for r in response:
				results['trakt'].append(r['movie']['ids']['trakt'])
				results['imdb'].append(r['movie']['ids']['imdb'])
				results['tmdb'].append(r['movie']['ids']['tmdb'])
			return results	
	
	def get_next_episodes(self):
		uri = '/sync/history/episodes'
		response = self._call(uri, auth=True)
		if not response: return False
		for r in response:
			ADDON.log(r)
		#ADDON.log(response)
	
	def get_watched_episodes(self, id):
		a = self.check_activities()
		uri = '/sync/history/seasons/%s' % id
		results = self.cache_request(a['episodes']['watched_at'], 'episodes_watched_at_%s' % id , uri, auth=True)
		return results
	
	def get_bookmark(self, media, id, id_type = 'imdb', season=None, episode=None):
		bookmarks = self.get_bookmarks(media)
		for bookmark in bookmarks:
			if media == 'episodes':
				if id== bookmark['show']['ids'][id_type] and bookmark['episode']['season'] == int(season) and bookmark['episode']['number'] == int(episode):
					return bookmark['progress']
			else:
				if id == bookmark['movie']['ids'][id_type]:
					return bookmark['progress']
		return None
	def get_bookmarks(self, media):
		uri = '/sync/playback/%s' % media
		return self._call(uri, auth=True)
		
	
	def process_record(self, record, media=None, watched=None, show=None):
		if media=='movie':
			meta = self.process_movie(record)
			return meta
		elif media=='episode':
			meta = self.process_episode(record, watched=watched, show=show)
			return meta
		elif media=='tvshow':
			meta = self.process_show(record)
			return meta
	
	def meta_map(self, path, object, default=''):
		try:
			if isinstance(path, list):
				for k in path:
					object = object[k]
			else:
				object = object[path]
				object = object if object is not None else default
			return object
		except:
			return default
	
	def format_trailer(self, trailer_url):
		if not trailer_url: return trailer_url
		match = re.search('\?v=(.*)', trailer_url)
		if match:
			return 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (match.group(1))	
	
	def process_show(self, record):
		try:
			show = record['show']
		except:
			show = record
		meta = {}

		meta['imdb_id'] = self.meta_map(['ids', 'imdb'], show)
		meta['tvdb_id'] = self.meta_map(['ids', 'tvdb'], show)
		meta['tmdb_id'] = self.meta_map(['ids', 'tmdb'], show)
		meta['trakt_id'] = self.meta_map(['ids', 'trakt'], show)
		meta['slug'] = self.meta_map(['ids', 'slug'], show)
		meta['title'] = self.meta_map('title', show)
		meta['TVShowTitle'] = self.meta_map('title', show)
		meta['tvshowtitle'] = self.meta_map('title', show)
		meta['rating'] = self.meta_map('rating', show)
		meta['duration'] = self.meta_map('runtime', show)
		meta['plot'] = self.meta_map('overview', show)
		meta['mpaa'] = self.meta_map('certification', show)
		meta['premiered'] = self.meta_map('first_aired', show)
		meta['year'] = int(self.meta_map('year', show, default=0))
		meta['trailer'] = self.format_trailer(self.meta_map('trailer', show))
		meta['genre'] = self.meta_map('genres', show)
		meta['studio'] = self.meta_map('network', show)
		meta['status'] = self.meta_map('status', show)
		meta['cast'] = []
		meta['banner_url'] = self.meta_map(['images', 'thumb', 'full'], show)
		meta['cover_url'] = self.meta_map(['images', 'poster', 'full'], show)
		meta['backdrop_url'] = self.meta_map(['images', 'fanart', 'full'], show)
		meta['overlay'] = 6
		meta['playcount'] = 0
		if meta['imdb_id'] is None or meta['imdb_id']=='':
			imdb_id = self.resolve_imdb_id(meta['TVShowTitle'], meta['year'], 'series', meta['tmdb_id'], meta['trakt_id'])
			meta['imdb_id'] = imdb_id
		SQL = 'INSERT OR REPLACE ' if DB.db_type =='sqlite' else 'REPLACE '
		SQL += 'INTO show_cache(title, imdb_id, tmdb_id, trakt_id, slug, cache) VALUES(?,?,?,?,?,?)'
		DB.execute(SQL, [meta['title'], meta['imdb_id'], meta['tmdb_id'], meta['trakt_id'], meta['slug'], json.dumps(meta)])
		DB.commit(True)
		return meta
		
	def process_movie(self, record):
		try:
			movie = record['movie']
		except:
			movie = record
		meta = {}
		meta['imdb_id'] = self.meta_map(['ids', 'imdb'], movie)
		meta['tmdb_id'] = self.meta_map(['ids', 'tmdb'], movie)
		meta['trakt_id'] = self.meta_map(['ids', 'trakt'], movie)
		meta['slug'] = self.meta_map(['ids', 'slug'], movie)
		meta['title'] = self.meta_map('title', movie)
		meta['year'] = int(self.meta_map('year', movie, default=0))
		meta['writer'] = ''
		meta['director'] = ''
		meta['tagline'] = self.meta_map('tagline', movie)
		meta['cast'] = []
		meta['rating'] = self.meta_map('rating', movie)
		meta['votes'] = self.meta_map('votes', movie)
		meta['duration'] = self.meta_map('runtime', movie)
		meta['plot'] = self.meta_map('overview', movie)
		meta['mpaa'] = self.meta_map('certification', movie)
		meta['premiered'] = self.meta_map('released', movie)
		meta['trailer'] = self.format_trailer(self.meta_map('trailer', movie))
		meta['genre'] = self.meta_map('genres', movie)
		meta['studio'] = ''
		meta['thumb_url'] = self.meta_map(['images', 'thumb', 'full'], movie)
		meta['cover_url'] = self.meta_map(['images', 'poster', 'full'], movie)
		meta['backdrop_url'] = self.meta_map(['images', 'fanart', 'full'], movie)
		meta['overlay'] = 6
		meta['playcount'] = 0
		if meta['imdb_id'] is None or meta['imdb_id'] =='None':
			imdb_id = self.resolve_imdb_id(meta['title'], meta['year'], 'movie', meta['tmdb_id'], meta['trakt_id'])
			meta['imdb_id'] = imdb_id
		print meta
		SQL = 'INSERT OR REPLACE ' if DB.db_type =='sqlite' else 'REPLACE '
		SQL += 'INTO movie_cache(title, imdb_id, tmdb_id, trakt_id, slug, cache) VALUES(?,?,?,?,?,?)'
		DB.execute(SQL, [meta['title'], meta['imdb_id'], meta['tmdb_id'], meta['trakt_id'], meta['slug'], json.dumps(meta)])
		DB.commit(True)
		return meta
	
	def process_episode(self, record, watched=None, show=None):

		if 'show' in record.keys():
			show = record['show']
			episode = record['episode']
			meta = {}
			meta['imdb_id']= self.meta_map(['ids', 'imdb'], show) 				# show['ids']['imdb']
			meta['tvdb_id']= self.meta_map(['ids', 'tvdb'], show) 				# show['ids']['tvdb']
			meta['tmdb_id']= self.meta_map(['ids', 'tmdb'], show) 				# show['ids']['tmdb']
			meta['slug']= self.meta_map(['ids', 'slug'], show) 				# show['ids']['tmdb']
			meta['trakt_id']= self.meta_map(['ids', 'trakt'], episode) 			# episode['ids']['trakt']
			meta['year'] = int(self.meta_map('year', show, default=0)) 			# int(show['year'])
			meta['episode_id'] = ''
			meta['season']= int(self.meta_map('season', episode, default=0)) 	# int(episode['season'])
			meta['episode']= int(self.meta_map('number', episode, default=0)) 	# int(episode['number'])
			meta['title']= self.meta_map('title', episode) 						# episode['title']
			meta['showtitle'] = self.meta_map('title', show) 					# #show['title']
			meta['tvshowtitle'] = self.meta_map('title', show) 					# #show['title']
			meta['director'] = ''
			meta['writer'] = ''
			meta['plot'] = self.meta_map('overview', episode) 					# episode['overview']
			meta['rating'] = self.meta_map('rating', episode) 					# episode['rating']
			meta['premiered'] = self.meta_map('first_aired', episode) 			# episode['first_aired']
			meta['poster'] = self.meta_map(['images', 'poster', 'full'], show) 	# show['images']['poster']['full']
			meta['cover_url']= self.meta_map(['images', 'screenshot', 'full'], episode) 	# episode['images']['screenshot']['full']
			meta['trailer']=''
			meta['backdrop_url'] = self.meta_map(['images', 'fanart', 'full'], show) 	# show['images']['fanart']['full']
			meta['overlay'] = 6
			meta['playcount'] = 0
			if watched:
				for w in watched:
					if w['episode']['number'] == meta['episode']:
						meta['overlay'] = 7
						meta['playcount'] = 1
						break
			if meta['imdb_id'] is None:
				imdb_id = self.resolve_imdb_id(meta['showtitle'], meta['year'], 'series', meta['tmdb_id'], meta['trakt_id'])
				meta['imdb_id'] = imdb_id
			if meta['season'] != 0 and meta['episode'] != 0:
				SQL = 'INSERT OR REPLACE ' if DB.db_type =='sqlite' else 'REPLACE '
				SQL += 'INTO episode_cache(season, episode, imdb_id, tmdb_id, trakt_id, slug, cache) VALUES(?,?,?,?,?,?,?)'
				DB.execute(SQL, [meta['season'], meta['episode'], meta['imdb_id'], meta['tmdb_id'], meta['trakt_id'], meta['slug'], json.dumps(meta)])
				DB.commit(True)
			return meta
		else:
			meta = {}
			episode = record
			meta['premiered'] = self.meta_map('first_aired', episode)
			tmp = re.match('^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.000Z', meta['premiered'])
			if tmp:
				year = tmp.group(1)
				aired = datetime(int(tmp.group(1)), int(tmp.group(2)),int(tmp.group(3)),int(tmp.group(4)),int(tmp.group(5)),int(tmp.group(6)))
				aired = time.mktime(aired.timetuple())
				now = time.mktime(datetime.now().timetuple())
			else:
				return False
			if aired < now:
				meta['imdb_id']= self.meta_map(['ids', 'imdb'], show) 			# episode['ids']['imdb']
				meta['tvdb_id']= self.meta_map(['ids', 'tvdb'], show) 			# episode['ids']['tvdb']
				meta['tmdb_id']= self.meta_map(['ids', 'tmdb'], show) 			# episode['ids']['tmdb']
				meta['trakt_id']= self.meta_map(['ids', 'trakt'], show) 			# episode['ids']['trakt']
				meta['slug']= self.meta_map(['ids', 'slug'], show) 			# episode['ids']['trakt']
				meta['year'] = year
				meta['episode_id'] = ''
				meta['season']= int(self.meta_map('season', episode, default=0))		# int(episode['season'])
				meta['episode']= int(self.meta_map('number', episode, default=0))	#int(episode['number'])
				meta['title']= self.meta_map('title', episode)						# episode['title']
				meta['showtitle'] = self.meta_map('title', show) 
				meta['tvshowtitle'] = self.meta_map('title', show) 					# #show['title']
				meta['director'] = ''
				meta['writer'] = ''
				meta['plot'] = self.meta_map('overview', episode) 					#episode['overview']
				meta['rating'] = self.meta_map('rating', episode) 					#episode['rating']
				meta['premiered'] = self.meta_map('first_aired', episode) 			#episode['first_aired']
				meta['poster'] = ''
				meta['cover_url']= self.meta_map(['images', 'screenshot', 'full'], episode)
				meta['trailer_url']=''
				meta['backdrop_url'] = ''
				meta['overlay'] = 6
				meta['playcount'] = 0
				if watched:
					for w in watched:
						if w['episode']['number'] == meta['episode']:
							meta['overlay'] = 7
							meta['playcount'] = 1
							break
				SQL = 'INSERT OR REPLACE ' if DB.db_type =='sqlite' else 'REPLACE '
				SQL += 'INTO episode_cache(season, episode, imdb_id, tmdb_id, trakt_id, slug, cache) VALUES(?,?,?,?,?,?,?)'
				DB.execute(SQL, [meta['season'], meta['episode'], meta['imdb_id'], meta['tmdb_id'], meta['trakt_id'], meta['slug'], json.dumps(meta)])
				DB.commit(True)
				return meta
			return False

	def raise_error(self, code, title, message):
		if code in [500, 502, 503, 504, 520, 521, 522, 524]:
			message = "Temporary " + message
		from dudehere.routines.plugin import Plugin
		image = vfs.join(ARTWORK, 'trakt_error.png')
		if vfs.exists(image) is False:
			image = vfs.join(ROOT_PATH, 'icon.png')
		Plugin().error_message(title, message, image=image)

	def notify(self, title, message):
		from dudehere.routines.plugin import Plugin
		image = vfs.join(ROOT_PATH, 'icon.png')
		Plugin().error_message(title, message, image=image)
	
	def _cache_result(self, result, url, cache_limit=15):
		hash_id = hashlib.md5(url).hexdigest()
		if cache_limit > 0:
			DB.execute("DELETE FROM cache WHERE strftime('%s','now') -  strftime('%s',ts) > (60 * ?)", [cache_limit])
		SQL = "INSERT INTO cache(hash_id, url, results) VALUES(?,?,?)"
		DB.execute(SQL, [hash_id, url, json.dumps(result)])
		DB.commit()
		
	def _clear_watchlist_cache(self):
		DB.execute("DELETE FROM cache WHERE media='watchlist'")
		DB.commit()
	
	def _get_cached_result(self, url, cache_limit=15):
		result = False
		if cache_limit > 0:
			DB.execute("DELETE FROM cache WHERE strftime('%s','now') -  strftime('%s',ts) > (60 * ?)", [cache_limit])
		hash_id = hashlib.md5(url).hexdigest()
		cache = DB.query("SELECT results FROM cache WHERE hash_id=?", [hash_id])
		if cache:
			result = json.loads(cache[0])
		DB.commit()
		return result

	def check_activities(self):
		results = {}
		uri = '/sync/last_activities'
		response = self._call(uri, auth=True)
		for media in ['movies', 'shows', 'seasons', 'episodes', 'lists']:
			results[media] = {}
			for activity in ['watched_at', 'watchlisted_at', 'updated_at']:
				if not response: return results
				if activity in response[media]:
					ts = response[media][activity]
					SQL = "SELECT activity FROM activities WHERE activity=? AND ts >= strftime('%s',?)"
					check = "%s_%s" % (media, activity)
					test = DB.query(SQL, [check, ts])
					if test:
						results[media][activity] = [True, ts]
					else:
						results[media][activity] = [False, ts]
		return results
	
	def check_activity(self, media, activity):
		activities = self.check_activities()
		if media in activities:
			if activity in activities[media]:
				return activities[media]
		return False
	
	def cache_request(self, fresh, activity, uri, data=None, params=None, auth=False):
		if fresh[0]:
			results = DB.query("SELECT cache FROM activity_cache WHERE activity=?", [activity])
			if results:
				ADDON.log('return cached activity: %s' % activity)
				return json.loads(results[0])
		ADDON.log('request remote activity: %s, %s' % (activity, uri))
		results = self._call(uri, params=params, data=data, auth=auth)
		if results:
			DB.execute("INSERT OR REPLACE INTO activity_cache(activity, cache) VALUES (?,?)", [activity, json.dumps(results)])
		if activity.endswith('_at') is False:
			activity = re.sub('_[a-zA-Z0-9]+$', '', activity)
			
		DB.execute("INSERT OR REPLACE INTO activities(activity, ts) VALUES (?, strftime('%s',?))", [activity, fresh[1]])
		DB.commit()
		return results
	

	def do_authorization(self, message=None):
		a = AuthWindow("trakt_auth.xml", ROOT_PATH)
		if message is not None:
			a.message = message
		a.doModal()
		response = a.response
		del a
		return response

	def get_db_connection(self):
		return DB
	
	def generate_code(self):
		uri = '/oauth/device/code'
		data = {'client_id': CLIENT_ID}
		return self._call(uri, data=data, auth=False)

	def request_device_token(self, code):
		uri = '/oauth/device/token'
		data = {'client_id': CLIENT_ID, 'client_secret': SECRET_ID, 'code': code}
		return self._call(uri, data=data, auth=False)
	
	def refresh_token(self, refresh_token):
		uri = '/oauth/token'
		data = {'client_id': CLIENT_ID, 'client_secret': SECRET_ID, 'redirect_uri': REDIRECT_URI}
		data['refresh_token'] = refresh_token
		data['grant_type'] = 'refresh_token'
		return self._call(uri, data=data, auth=False, method='post')
	
	def _authorize(self, window=None):
		if window is not None:
			import xbmc
			response = self.generate_code()
			window.getControl(82005).setLabel("[B]%s[/B]" % response['user_code'])
			delay = 0
			delta = response['expires_in']
			while delay < response['expires_in'] and self.get_property('Abort') == False:
				window.getControl(82003).setLabel("Code expires in %s seconds" % delta)
				percent = int(delta / float(response['expires_in']) * 480 )
				window.getControl(82004).setWidth(percent)
				delay += 1
				delta -= 1
				if delay % response['interval'] == 0:
					token_response = self.request_device_token(response['device_code'])
					if token_response:
						ADDON.set_setting('trakt_oauth_token', token_response['access_token'])
						ADDON.set_setting('trakt_refresh_token', token_response['refresh_token'])
						ADDON.set_setting('trakt_authorized', "true")
						self.token = token_response['access_token']
						settings = self.get_settings()
						if settings:
							ADDON.set_setting('trakt_account', settings['user']['username'])
						return True
				xbmc.sleep(1000)
			return False
		else:
			refresh_token = ADDON.get_setting('trakt_refresh_token')
			response = self.refresh_token(refresh_token)
			if not response: return False
			if 'access_token' in response and 'refresh_token' in response:
				ADDON.set_setting('trakt_oauth_token', response['access_token'])
				ADDON.set_setting('trakt_refresh_token', response['refresh_token'])
				ADDON.set_setting('trakt_authorized', "true")
				self.token = response['access_token']
				return True
				
			return False
		
	def _call(self, uri, data=None, params=None, auth=False, cache_limit=False, timeout=None, quiet=False, method=None):
		if timeout is not None: self.timetout = timeout
		json_data = json.dumps(data) if data else None
		headers = {'Content-Type': 'application/json', 'trakt-api-key': CLIENT_ID, 'trakt-api-version': 2}
		url = '%s%s' % (BASE_URL, uri)
		if params:
			params['limit'] = self.limit
			url += '?' + urllib.urlencode(params)
		elif not uri in ['/oauth/device/code', '/oauth/token', '/oauth/device/token']:
			params = {'limit': self.limit}
			url += '?' + urllib.urlencode(params)
		
		if cache_limit is not False and not uri in ['/oauth/device/code', '/oauth/token', '/oauth/device/token']:
			result = self._get_cached_result(url, cache_limit)
			if result:
				response = json.loads(result)
				ADDON.log("Returning cached results")
				return response
				
		if auth: 
			self.token = ADDON.get_setting('trakt_oauth_token')
			headers.update({'Authorization': 'Bearer %s' % (self.token)})
			retry_attempt = False
		else:
			retry_attempt = True
		while True:	
			try:
				request = urllib2.Request(url, data=json_data, headers=headers)
				if method is not None:
					request.get_method = lambda: method.upper()
				f = urllib2.urlopen(request, timeout=self.timeout)
				result = f.read()
				response = json.loads(result)
				break
			except HTTPError as e:
				if e.code in [401,405]:
					if uri in ['/oauth/device/code', '/oauth/token', '/oauth/device/token'] is False or retry_attempt:
						ADDON.set_setting('trakt_oauth_token', '')
						ADDON.set_setting('trakt_refresh_token', '')
						ADDON.set_setting('trakt_authorized', "false")
						self.raise_error(-1, ADDON_ID, 'Trakt Authorization Required: %s' % e.code)
						raise TraktError('Trakt Authorization Required: %s' % e.code)
						return False
					else:
						self._authorize()
						second_attempt = True
				else:
					if uri in ['/oauth/device/code', '/oauth/token', '/oauth/device/token'] is False:
						ADDON.log("%s: %s" % (e,url), LOG_LEVEL.VERBOSE)
						self.raise_error(e.code, "Trakt error", e)
					return False
			except URLError as e:
				ADDON.log("%s: %s" % (e,url), LOG_LEVEL.VERBOSE)
				self.raise_error(e.code, "Trakt error", e)
				return False
			except socket.timeout as e:
				ADDON.log("%s %s" % (e,url), LOG_LEVEL.VERBOSE)
				self.raise_error(e, "Trakt error", e)
				return False
			if cache_limit is not False:
				self._cache_result(result, url, cache_limit)
		return response

	
	def _delete(self, uri, data=None, params=None, auth=True):
		json_data = json.dumps(data) if data else None
		url = '%s%s' % (BASE_URL, uri)
		opener = urllib2.build_opener(urllib2.HTTPHandler)
		headers = {'Content-Type': 'application/json', 'trakt-api-key': CLIENT_ID, 'trakt-api-version': 2}
		if auth: headers.update({'Authorization': 'Bearer %s' % (self.token)})
		try:
			request = urllib2.Request(url, data=json_data, headers=headers)
			request.get_method = lambda: 'DELETE'
			response = opener.open(request)
		except HTTPError as e:
			ADDON.log("%s: %s" % (e,url), LOG_LEVEL.VERBOSE)
			self.raise_error(e.code, "Trakt error", 'HTTP ERROR: %s' % e)
			return False
		except URLError as e:
			ADDON.log("%s: %s" % (e,url), LOG_LEVEL.VERBOSE)
			self.raise_error(e.code, "Trakt error", 'HTTP ERROR: %s' % e)
			return False
		except socket.timeout as e:
			ADDON.log("%s: %s" % (e,url), LOG_LEVEL.VERBOSE)
			self.raise_error(-1, "Trakt error", 'Socket Timeout: %s' % e)
			return False
		else:
			return response
		