# -*- coding: utf-8 -*-

###########################
# Rating Update           #
# by Max (m4x1m) Headroom #
###########################

import re, sys, HTMLParser, datetime
import xbmc, xbmcgui, xbmcvfs
if sys.version_info >= (2, 7): import json as jSon
else: import simplejson as jSon
from ruCommon import *

class Top250:
     def __init__( self ):
	  self.Today = datetime.datetime.now()
	  if xbmcvfs.exists( MissingTop250 ): xbmcvfs.delete( MissingTop250 )
	  file( MissingTop250, "w" ).write( str( "Missing Top250 generated on " + self.Today.strftime( Local ) + "\n\n" ) )
	  self.MissingTop250 = []; self.Aborted = False;
	  self.Top250 = self.getTop250()
	  if len( self.Top250 ) <= 0:
	       defaultLog( addonLanguage(32605) )
	       if BackgroundRun == "0" and HideProgress == "false": dialogOK( addonLanguage(32601), addonLanguage(32605), "", "" )
	       else: doNotify( addonLanguage(32605), 15000 )
	  else:
	       self.getMovies()
	       if self.Aborted != True:
		    if len( self.Movies ) <= 0:
			 defaultLog( addonLanguage(32607) )
			 if BackgroundRun == "0" and HideProgress == "false": dialogOK( addonLanguage(32601), addonLanguage(32607), "", "" )
			 else: doNotify( addonLanguage(32607), 15000 )
		    else:
			 getResponse = self.doScan()
			 if self.Aborted != True:
			      ruDatabase.Execute( 'UPDATE latest SET top250 = "%s"' % self.Today.strftime( Local ) )
			      ruDatabase.Execute( 'UPDATE resume SET top250 = "32251"' )
			      if BackgroundRun == "0" and HideProgress == "false":
				   getResponse = getResponse.split("|")
				   Question = dialogQuestion( addonLanguage(32600), addonLanguage(32400), getResponse[0], getResponse[1], addonLanguage(32104), addonLanguage(32105) )
				   if Question == 1:
					import ruTop250Gui
					ruTop250Gui.ruTop250Gui( "script_rating_update-lists.xml", addonSettings.getAddonInfo( "path" ), "Default", forceFallback = False, parent = self )
			      else: doNotify( getResponse, 15000 )
			 else: doNotify( getResponse, 15000 )

     def getTop250( self ):
	  Top250 = []; Titles = []; IDs = []; jXmlData = "";
	  defaultLog( addonLanguage(32250) )
	  doNotify( addonLanguage(32250), 3000 )
	  jXmlData = getTop250()
	  xmlTitles = re.findall( "<Title>(.*?)</Title>", jXmlData, re.DOTALL )
	  xmlIDs = re.findall( "<ID>(.*?)</ID>", jXmlData, re.DOTALL )
	  for Title in xmlTitles: Titles.append( Title )
	  for ID in xmlIDs: IDs.append( ID )
	  Top250 = [ [IDs[i] + '', '' + Titles[i] ] for i in range( len( IDs ) ) ]
	  return Top250

     def getDBMovies( self ):
	  jSonQuery = '{"jsonrpc":"2.0","method":"VideoLibrary.GetMovies","params":{"properties":["imdbnumber","top250"]},"id":1}'
	  debugLog( "JSON Query: " + jSonQuery )
	  jSonResponse = xbmc.executeJSONRPC( jSonQuery )
	  jSonResponse = unicode( jSonResponse, 'utf-8', errors='ignore' )
	  debugLog( "JSON Response: " + jSonResponse )
	  jSonResponse = jSon.loads( jSonResponse )
	  try:
	       if jSonResponse['result'].has_key( 'movies' ):
		    for item in jSonResponse['result']['movies']:
			 MovieID = item.get('movieid'); IMDb = item.get('imdbnumber'); Title  = item.get('label'); Top250 = item.get('top250');
			 self.AllMovies.append( ( MovieID, IMDb, Title, Top250 ) )
	  except: pass

     def doScrape( self, IMDb, Title ):
	  html = HTMLParser.HTMLParser(); Found = False;
	  for Movie in self.AllMovies:
	       if Movie[1] == IMDb:
		    Found = True
		    self.Movies.append( ( Movie[0], Movie[1], Movie[2], Movie[3], self.Count ) )
	  if Found == False:
	       self.MissingTop250.append( ( str( self.Count ).zfill(3) + " - " + str( Title ), IMDb ) )
	       file( MissingTop250, "a" ).write( str( self.Count ).zfill(3) + " - " + str( doNormalize( html.unescape( Title ) ) + " - [" + IMDb + "]\n" ) )

     def getMovies( self ):
	  self.AllMovies = []; self.getDBMovies();
	  self.Count = 0;  self.Movies = [];
	  defaultLog( addonLanguage(32300) )
	  if BackgroundRun == "0" and HideProgress == "false":
	       Progress = xbmcgui.DialogProgress(); Progress.create( addonName );
	  for Top250 in self.Top250:
	       self.Count = self.Count + 1
	       if BackgroundRun == "0" and HideProgress == "false":
		    Progress.update( (self.Count*100)/250, addonLanguage(32300) )
		    if Progress.iscanceled():
			 Progress.close(); self.Aborted = True;
			 ruDatabase.Execute( 'UPDATE resume SET top250 = "30252"' )
			 defaultLog( addonLanguage(32603) )
			 dialogOK( addonLanguage(32602), addonLanguage(32603), "", "" )
			 break
	       self.doScrape( Top250[0], Top250[1] )

     def doUpdate( self, Movie ):
	  oldTop = int( Movie[3] ); newTop = int( Movie[4] );
	  if oldTop != newTop:
	       if RawQueries == "true":
		    RawXBMC.Execute( 'UPDATE movie SET c13="%s" WHERE idMovie="%s"' % ( str( Movie[4] ), Movie[0] ) )
		    if oldTop == 0:
			 defaultLog( addonLanguage(32301) % ( Movie[2], newTop ) ); self.Added = self.Added + 1;
		    else:
			 defaultLog( addonLanguage(32302) % ( Movie[2], oldTop, newTop ) ); self.Updated = self.Updated + 1;
	       else:
		    jSonQuery = '{"jsonrpc":"2.0","method":"VideoLibrary.SetMovieDetails","params":{"movieid":' + str( Movie[0] ) + ',"top250":' + str( Movie[4] ) + '},"id":1}'
		    debugLog( "JSON Query: " + jSonQuery )
		    jSonResponse = xbmc.executeJSONRPC( jSonQuery )
		    jSonResponse = unicode( jSonResponse, 'utf-8', errors='ignore' )
		    debugLog( "JSON Response: " + jSonResponse )
		    jSonResponse = jSon.loads( jSonResponse )
		    if jSonResponse['result'] != "OK": defaultLog( addonLanguage(32604) )
		    else:
			 if oldTop == 0:
			      defaultLog( addonLanguage(32301) % ( Movie[2], newTop ) ); self.Added = self.Added + 1;
			 else:
			      defaultLog( addonLanguage(32302) % ( Movie[2], oldTop, newTop ) ); self.Updated = self.Updated + 1;
	  else: defaultLog( addonLanguage(32303) % Movie[2] )

     def doScan( self ):
	  TotalMovies = len( self.Movies )
	  Count = 0; self.Added = 0; self.Updated = 0; self.Removed = 0;
	  defaultLog( addonLanguage(32254) )
	  if BackgroundRun == "0" and HideProgress == "false":
	       Progress = xbmcgui.DialogProgress()
	       Progress.create( addonName )
	  for Movie in self.Movies:
	       Count = Count + 1
	       if BackgroundRun == "0" and HideProgress == "false":
		    Progress.update( (Count*100)/TotalMovies, "%s %s" % ( addonLanguage(32403), Movie[2] ) )
		    xbmc.sleep(500)
		    if Progress.iscanceled():
			 Progress.close(); self.Aborted = True;
			 ruDatabase.Execute( 'UPDATE resume SET top250 = "30252"' )
			 defaultLog( addonLanguage(32603) )
			 dialogOK( addonLanguage(32602), addonLanguage(32603), "", "" )
			 break
	       self.doUpdate( Movie )
	  if self.Aborted != True:
	       RemovedMovies = []
	       for Movie in self.AllMovies:
		    if Movie[3] > 0: RemovedMovies.append( ( Movie[0], Movie[1], Movie[2] ) )
	       for Movie in RemovedMovies:
		    Found = False
		    for Top250 in self.Top250:
			 if Movie[1] == Top250[0]: Found = True
		    if Found != True:
			 if RawQueries == "true":
			      RawXBMC.Execute( 'UPDATE movie SET c13="0" WHERE idMovie="%s"' % Movie[0] )
			      defaultLog( addonLanguage(32304) % Movie[2] ); self.Removed = self.Removed + 1;
			 else:
			      jSonQuery = '{"jsonrpc":"2.0","method":"VideoLibrary.SetMovieDetails","params":{"movieid":' + str( Movie[0] ) + ',"top250":0},"id":1}'
			      debugLog( "JSON Query: " + jSonQuery )
			      jSonResponse = xbmc.executeJSONRPC( jSonQuery )
			      jSonResponse = unicode( jSonResponse, 'utf-8', errors='ignore' )
			      debugLog( "JSON Response: " + jSonResponse )
			      jSonResponse = jSon.loads( jSonResponse )
			      if jSonResponse['result'] != "OK": defaultLog( addonLanguage(32604) )
			      else:
				   defaultLog( addonLanguage(32304) % Movie[2] ); self.Removed = self.Removed + 1;
	       getResponse = addonLanguage(32400) + ": " + addonLanguage(32305).replace("|", ". ") % ( self.Updated, self.Added, self.Removed, TotalMovies )
	       defaultLog( getResponse )
	       if BackgroundRun == "0" and HideProgress == "false": getResponse = addonLanguage(32305) % ( self.Updated, self.Added, self.Removed, TotalMovies )
	       return getResponse
	  else:
	       getResponse = addonLanguage(32603)
	       return getResponse

class Movies:
     def __init__( self ):
	  self.Today = datetime.datetime.now()
	  self.Resume = 0; self.InitResume = 0; self.Aborted = False;
	  Resume = ruDatabase.Query( 'SELECT movies FROM resume' )
	  if int( Resume[0][0] ) > 0:
	       if BackgroundRun == "0":
		    Question = dialogQuestion( addonLanguage(32600), addonLanguage(32200), addonLanguage(32201), "", "", "" )
		    if Question == 1:
			 self.Resume = int( Resume[0][0] ); self.InitResume = int( Resume[0][0] );
	       else:
		    if ResumeResponse == "1":
			 self.Resume = int( Resume[0][0] ); self.InitResume = int( Resume[0][0] );
	  self.Movies = []; self.getDBMovies()
	  if len( self.Movies ) <= 0:
	       defaultLog( addonLanguage(32607) )
	       if BackgroundRun == "0" and HideProgress == "false": dialogOK( addonLanguage(32601), addonLanguage(32607), "", "" )
	       else: doNotify( addonLanguage(32607), 15000 )
	  else:
	       getResponse = self.doScan()
	       ruDatabase.Execute( 'UPDATE latest SET movies = "%s"' % self.Today.strftime( Local ) )
	       if self.Aborted != True:
		    Movies = len( self.Movies ) + self.InitResume
		    if self.Resume != Movies: Resume = self.Resume
		    else: Resume = 0
		    ruDatabase.Execute( 'UPDATE resume SET movies = "%s"' % Resume )
		    if BackgroundRun == "0" and HideProgress == "false": dialogOK( addonLanguage(32600), addonLanguage(32401), getResponse, "" )
		    else: doNotify( getResponse, 15000 )
	       else:
		    if BackgroundRun == "0" and HideProgress == "false": getResponse = addonLanguage(32401) + ": " + getResponse
		    doNotify( getResponse, 15000 )

     def getDBMovies( self ):
	  jSonQuery = '{"jsonrpc":"2.0","method":"VideoLibrary.GetMovies","params":{"limits":{"start":' + str( self.Resume ) + '},"properties":["imdbnumber","rating","votes","mpaa"],"sort":{"order":"ascending","method":"label","ignorearticle":true}},"id":1}'
	  debugLog( "JSON Query: " + jSonQuery )
	  jSonResponse = xbmc.executeJSONRPC( jSonQuery )
	  jSonResponse = unicode( jSonResponse, 'utf-8', errors='ignore' )
	  debugLog( "JSON Response: " + jSonResponse )
	  jSonResponse = jSon.loads( jSonResponse )
	  try:
	       if jSonResponse['result'].has_key( 'movies' ):
		    for item in jSonResponse['result']['movies']:
			 MovieID = item.get('movieid'); IMDb = item.get('imdbnumber'); Title  = item.get('label'); 
			 Rating = item.get('rating'); Votes = item.get('votes'); Mpaa = item.get('mpaa');
			 self.Movies.append( ( MovieID, IMDb, Title, Rating, Votes, Mpaa ) )
	  except: pass

     def doUpdate( self ):
	  MovieID = self.Movie[0]; IMDb = self.Movie[1]; Title = self.Movie[2];
	  Rating = self.Movie[3]; Votes = self.Movie[4]; Mpaa = self.Movie[5];
	  jSonData = getRatings( IMDb )
	  if jSonData != "":
	       try:
		    jSonData = unicode( jSonData, 'utf-8', errors='ignore' )
		    jSonData = jSon.loads( jSonData )
		    getResponse = jSonData['response']
	       except: getResponse = "false"
	       if getResponse == "true":
		    jsParams = ""; rawParams = ""; showResult = "";
		    newVotes = jSonData['votes']
		    if newVotes != "0":
			 Rating = float( ( "%.1f" % Rating ) )
			 newRating = float( jSonData['rating'] )
			 if Votes != newVotes or Rating != newRating:
			      jsParams += '"rating":' + str( newRating ) + ',"votes":"' + str( newVotes ) + '",'
			      rawParams += 'c04="' + str( newVotes ) + '",c05="'+ str( newRating ) +'",'
			      showResult += addonLanguage(32500) % ( str( newRating ), str( newVotes ) )
			 else: showResult += addonLanguage(32502)
		    else: showResult += addonLanguage(32502)
		    if ( addonSettings.getSetting( "MpaaRating" ) == "true"):
			 if ( addonSettings.getSetting( "MpaaReason" ) == "0" and MpaaCountry == "USA" and jSonData['mpaa_reason'] != ""):
			      newReason = jSonData['mpaa_reason']
			      if Mpaa != newReason:
				   jsParams += '"mpaa":"' + newReason + '",'
				   rawParams += 'c12="' + newReason + '",'
				   showResult += addonLanguage(32501) % newReason
			      else: showResult += addonLanguage(32503)
			 else:
			      newMpaa = MpaaPrefixMovies + jSonData['mpaa']
			      if jSonData['mpaa'] and jSonData['mpaa'] != "Not Rated" and Mpaa != newMpaa:
				   jsParams += '"mpaa":"' + newMpaa + '",'
				   rawParams += 'c12="' + newMpaa + '",'
				   showResult += addonLanguage(32501) % newMpaa
			      else: showResult +=  addonLanguage(32503)
		    if jsParams:
			 if RawQueries == "true":
			      rawParams = rawParams[:-1]
			      RawXBMC.Execute( 'UPDATE movie SET ' + rawParams + ' WHERE idMovie="%s"' % MovieID )
			      self.Updated = self.Updated + 1
			 else:
			      jsParams = jsParams[:-1]
			      jSonQuery = '{"jsonrpc":"2.0","method":"VideoLibrary.SetMovieDetails","params":{"movieid":' + str( MovieID ) + ',' + jsParams + '},"id":1}'
			      debugLog( "JSON Query: " + jSonQuery )
			      jSonResponse = xbmc.executeJSONRPC( jSonQuery )
			      jSonResponse = unicode( jSonResponse, 'utf-8', errors='ignore' )
			      debugLog( "JSON Response: " + jSonResponse )
			      jSonResponse = jSon.loads( jSonResponse )
			      if jSonResponse['result'] != "OK": showResult = addonLanguage(32604)
			      else: self.Updated = self.Updated + 1
		    defaultLog( "%s: %s" % ( Title, showResult[0].lower() + showResult[1:] ) )
	       else: defaultLog( addonLanguage(32605) )
	  else: defaultLog( addonLanguage(32605) )

     def doScan( self ):
	  Count = 0; self.Updated = 0; Movies = len( self.Movies );
	  defaultLog( addonLanguage(32255) )
	  if BackgroundRun == "0" and HideProgress == "false":
	       Progress = xbmcgui.DialogProgress()
	       Progress.create( addonName )
	  else: doNotify( addonLanguage(32255), 15000 )
	  for self.Movie in self.Movies:
	       if BackgroundRun == "0" and HideProgress == "false":
		    Count = Count + 1
		    Progress.update( (Count*100)/Movies, "%s %s" % ( addonLanguage(32403), self.Movie[2] ), "" )
		    if Progress.iscanceled():
			 Progress.close(); self.Aborted = True;
			 defaultLog( addonLanguage(32603) )
			 dialogOK( addonLanguage(32602), addonLanguage(32603), addonLanguage(32202), "" )
			 break
	       if self.Aborted != True:
		    self.doUpdate()
		    self.Resume = self.Resume + 1
		    ruDatabase.Execute( 'UPDATE resume SET movies = "%s"' % self.Resume )
	  Movies = Movies + self.InitResume
	  getResponse = addonLanguage(32401) + ": " + addonLanguage(32504) % ( self.Updated, Movies )
	  defaultLog( getResponse )
	  if BackgroundRun == "0" and HideProgress == "false": getResponse = addonLanguage(32504) % ( self.Updated, Movies )
	  return getResponse

class TVShows:
     def __init__( self ):
	  self.Today = datetime.datetime.now()
	  self.Resume = 0; self.InitResume = 0; self.Aborted = False;
	  Resume = ruDatabase.Query( 'SELECT tvshows FROM resume' )
	  if int( Resume[0][0] ) > 0:
	       if BackgroundRun == "0":
		    Question = dialogQuestion( addonLanguage(32600), addonLanguage(32200), addonLanguage(32201), "", "", "" )
		    if Question == 1:
			 self.Resume = int( Resume[0][0] ); self.InitResume = int( Resume[0][0] );
	       else:
		    if ResumeResponse == "1":
			 self.Resume = int( Resume[0][0] ); self.InitResume = int( Resume[0][0] );
	  self.TVShows = []; self.getDBTVShows()
	  if len( self.TVShows ) <= 0:
	       defaultLog( addonLanguage(32607) )
	       if BackgroundRun == "0" and HideProgress == "false": dialogOK( addonLanguage(32601), addonLanguage(32607), "", "" )
	       else: doNotify( addonLanguage(32607), 15000 )
	  else:
	       getResponse = self.doScan()
	       ruDatabase.Execute( 'UPDATE latest SET tvshows = "%s"' % self.Today.strftime( Local ) )
	       if self.Aborted != True:
		    TVShows = len( self.TVShows ) + self.InitResume
		    if self.Resume != TVShows: Resume = self.Resume
		    else: Resume = 0
		    ruDatabase.Execute( 'UPDATE resume SET tvshows = "%s"' % Resume )
		    if BackgroundRun == "0" and HideProgress == "false": dialogOK( addonLanguage(32600), addonLanguage(32402), getResponse, "" )
		    else: doNotify( getResponse, 15000 )
	       else: 
		    if BackgroundRun == "0" and HideProgress == "false": getResponse = addonLanguage(32402) + ": " + getResponse
		    doNotify( getResponse, 15000 )

     def getDBTVShows( self ):
	  jSonQuery = '{"jsonrpc":"2.0","method":"VideoLibrary.GetTVShows","params":{"limits":{"start":' + str( self.Resume ) + '},"properties":["imdbnumber","rating","votes","mpaa"],"sort":{"order":"ascending","method":"label","ignorearticle":true}},"id":1}'
	  debugLog( "JSON Query: " + jSonQuery )
	  jSonResponse = xbmc.executeJSONRPC( jSonQuery )
	  jSonResponse = unicode( jSonResponse, 'utf-8', errors='ignore' )
	  debugLog( "JSON Response: " + jSonResponse )
	  jSonResponse = jSon.loads( jSonResponse )
	  try:
	       if jSonResponse['result'].has_key( 'tvshows' ):
		    for item in jSonResponse['result']['tvshows']:
			 TVShowID = item.get('tvshowid'); FakeIMDb = item.get('imdbnumber'); Title  = item.get('label'); 
			 Rating = item.get('rating'); Votes = item.get('votes'); Mpaa = item.get('mpaa');
			 self.TVShows.append( ( TVShowID, FakeIMDb, Title, Rating, Votes, Mpaa ) )
	  except: pass

     def doUpdate( self ):
	  IMDb = ruDatabase.Query( 'SELECT imdbID FROM tvshows WHERE tvshowID="%s"' % self.TVShow[1] )
	  if not IMDb or IMDb[0][0] == "-":
	       if BackgroundRun == "0":
		    IMDbID = ""; getByTitle = searchByTitle( self.TVShow[2] );
		    while IMDbID == "":
			 Notify = False
			 if len( getByTitle ) == 0 and IMDbID != "SKIP":
			      keyBoard = xbmc.Keyboard( self.TVShow[2] )
			      keyBoard.doModal()
			      if ( keyBoard.isConfirmed() ):
				   getTitle = keyBoard.getText()
				   getByTitle = searchByTitle( getTitle.decode( 'utf-8' ) )
			      else: IMDbID = "SKIP"
			 else:
			      nameList = []; html = HTMLParser.HTMLParser();
			      Titles = re.findall( "<Title>(.*?)</Title>", getByTitle, re.DOTALL )
			      IMDbIDs = re.findall( "<ID>(.*?)</ID>", getByTitle, re.DOTALL )
			      for Title in Titles: nameList.append( html.unescape( Title ) )
			      if len( nameList ) > 0:
				   Notify = True
				   doNotify( doNormalize( addonLanguage(32450) ) + self.TVShow[2], -1 )
				   nameList.append( addonLanguage(32457) )
				   nameList.append( addonLanguage(32452) )
				   skipAlways = len( nameList ) - 2
				   editName = len( nameList ) - 1
				   chooseDialog = xbmcgui.Dialog()
				   getResult = chooseDialog.select( addonLanguage(32451), nameList )
				   if getResult == editName:
					keyBoard = xbmc.Keyboard( self.TVShow[2] )
					keyBoard.doModal()
					if ( keyBoard.isConfirmed() ):
					     getTitle = keyBoard.getText()
					     getByTitle = searchByTitle( getTitle.decode( 'utf-8' ) )
				   elif getResult == skipAlways: IMDbID = addonLanguage(32458)
				   elif getResult != -1: IMDbID = IMDbIDs[getResult]
				   else: IMDbID = "SKIP"
		    if Notify == True: doNotify( doNormalize( addonLanguage(32450) ) + self.TVShow[2], 1 )
		    if IMDbID != "SKIP":
			 defaultLog( "%s: " % self.TVShow[2] + addonLanguage(32454) % IMDbID )
			 if not IMDb: ruDatabase.Query( 'INSERT INTO tvshows VALUES ("%s","%s","%s")' % ( self.TVShow[1], IMDbID, self.TVShow[2] ) )
			 else: ruDatabase.Execute( 'UPDATE tvshows SET imdbID = "%s" WHERE tvshowID = "%s"' % ( IMDbID, self.TVShow[1] ) )
			 self.doUpdate()
		    else: defaultLog( "%s: " % self.TVShow[2] + addonLanguage(32453) )
	       else:
		    if not IMDb:
			 defaultLog( "%s: " % self.TVShow[2] + addonLanguage(32456) )
			 doNotify( "%s: " % self.TVShow[2] + doNormalize( addonLanguage(32456) ), 3000 )
			 ruDatabase.Query( 'INSERT INTO tvshows VALUES ("%s","-","%s")' % ( self.TVShow[1], self.TVShow[2] ) )
	  else:
	       jSonData = ""; TVShowID = self.TVShow[0]; Title = self.TVShow[2];
	       Rating = self.TVShow[3]; Votes = self.TVShow[4]; Mpaa = self.TVShow[5];
	       if IMDb[0][0] != addonLanguage(32458): jSonData = getRatings( IMDb[0][0] )
	       else: defaultLog( "%s: %s" % ( Title, addonLanguage(32459).lower() ) )
	       if jSonData != "":
		    try:
			 jSonData = unicode( jSonData, 'utf-8', errors='ignore' )
			 jSonData = jSon.loads( jSonData )
			 getResponse = jSonData['response']
		    except: getResponse = "false"
		    if getResponse == "true":
			 jsParams = ""; rawParams = ""; showResult = "";
			 newVotes = jSonData['votes']
			 if newVotes != "0":
			      Rating = float( ( "%.1f" % Rating ) )
			      newRating = float( jSonData['rating'] )
			      if Votes != newVotes or Rating != newRating:
				   jsParams += '"rating":' + str( newRating ) + ',"votes":"' + str( newVotes ) + '",'
				   rawParams += 'c03="' + str( newVotes ) + '",c04="'+ str( newRating ) +'",'
				   showResult += addonLanguage(32500) % ( str( newRating ), str( newVotes ) )
			      else: showResult += addonLanguage(32502)
			 else: showResult += addonLanguage(32502)
			 if ( addonSettings.getSetting( "MpaaRating" ) == "true"):
			      newMpaa = MpaaPrefixTVShows + jSonData['mpaa']
			      if newMpaa and Mpaa != newMpaa:
				   jsParams += '"mpaa":"' + newMpaa + '",'
				   rawParams += 'c13="' + newMpaa + '",'
				   showResult += addonLanguage(32501) % newMpaa
			      else: showResult +=  addonLanguage(32503)
			 if jsParams:
			      if RawQueries == "true":
				   rawParams = rawParams[:-1]
				   RawXBMC.Execute( 'UPDATE tvshow SET ' + rawParams + ' WHERE idShow="%s"' % TVShowID )
				   self.Updated = self.Updated + 1
			      else:
				   jsParams = jsParams[:-1]
				   jSonQuery = '{"jsonrpc":"2.0","method":"VideoLibrary.SetTVShowDetails","params":{"tvshowid":' + str( TVShowID ) + ',' + jsParams + '},"id":1}'
				   debugLog( "JSON Query: " + jSonQuery )
				   jSonResponse = xbmc.executeJSONRPC( jSonQuery )
				   jSonResponse = unicode( jSonResponse, 'utf-8', errors='ignore' )
				   debugLog( "JSON Response: " + jSonResponse )
				   jSonResponse = jSon.loads( jSonResponse )
				   if jSonResponse['result'] != "OK": showResult = addonLanguage(32604)
				   else: self.Updated = self.Updated + 1
			 defaultLog( "%s: %s" % ( Title, showResult[0].lower() + showResult[1:] ) )
		    else: defaultLog( addonLanguage(32605) )
	       else:
		    if IMDb[0][0] != addonLanguage(32458): defaultLog( addonLanguage(32605) )

     def doScan( self ):
	  Count = 0; self.Updated = 0; TVShows = len( self.TVShows );
	  defaultLog( addonLanguage(32256) )
	  if BackgroundRun == "0" and HideProgress == "false":
	       Progress = xbmcgui.DialogProgress()
	       Progress.create( addonName )
	  else: doNotify( addonLanguage(32256), 15000 )
	  for self.TVShow in self.TVShows:
	       if BackgroundRun == "0" and HideProgress == "false":
		    Count = Count + 1
		    Progress.update( (Count*100)/TVShows, "%s %s" % ( addonLanguage(32403), self.TVShow[2] ), "" )
		    if Progress.iscanceled():
			 Progress.close(); self.Aborted = True;
			 defaultLog( addonLanguage(32603) )
			 dialogOK( addonLanguage(32602), addonLanguage(32603), addonLanguage(32202), "" )
			 break
	       if self.Aborted != True: 
		    self.doUpdate()
		    self.Resume = self.Resume + 1
		    ruDatabase.Execute( 'UPDATE resume SET tvshows = "%s"' % self.Resume )
	  TVShows = TVShows + self.InitResume
	  getResponse = addonLanguage(32402) + ": " + addonLanguage(32504) % ( self.Updated, TVShows )
	  defaultLog( getResponse )
	  if BackgroundRun == "0" and HideProgress == "false": getResponse = addonLanguage(32504) % ( self.Updated, TVShows )
	  return getResponse

if ( __name__ == "__main__" ):
     if ( BackgroundRun == "0" ):
	  import ruMainGui
	  ruMainGui.ruMainGui( "script_rating_update-main.xml", addonSettings.getAddonInfo( "path" ), "Default" )
     else:
	  if onTop250 == "true": Top250()
	  if onMovies == "true": Movies()
	  if onTVShows == "true": TVShows()