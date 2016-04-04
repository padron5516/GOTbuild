# -*- coding: utf-8 -*-

###########################
# Rating Update           #
# by Max (m4x1m) Headroom #
###########################

import xbmc
import re, sys, HTMLParser
if sys.version_info >= (2, 7): import json as jSon
else: import simplejson as jSon
from ruCommon import *

class TVShows:
     def __init__( self ):
	  getResponse = self.doUpdate()
	  if getResponse:
	       defaultLog( "%s: %s" % ( self.Title, getResponse ) )
	       doNotify( getResponse, 15000 )

     def getDBTVShow( self ):
	  ID = xbmc.getInfoLabel("ListItem.DBID")
	  jSonQuery = '{"jsonrpc":"2.0","method":"VideoLibrary.GetTVShowDetails","params":{"properties":["imdbnumber","rating","votes","mpaa"],"tvshowid":%s},"id":1}' % ID
	  debugLog( "JSON Query: " + jSonQuery )
	  jSonResponse = xbmc.executeJSONRPC( jSonQuery )
	  jSonResponse = unicode( jSonResponse, 'utf-8', errors='ignore' )
	  debugLog( "JSON Response: " + jSonResponse )
	  jSonResponse = jSon.loads( jSonResponse )
	  if jSonResponse['result'].has_key( 'tvshowdetails' ):
	       self.TVShowID = jSonResponse['result']['tvshowdetails'].get('tvshowid')
	       self.FakeIMDb = jSonResponse['result']['tvshowdetails'].get('imdbnumber')
	       self.Title    = jSonResponse['result']['tvshowdetails'].get('label')
	       self.Rating   = jSonResponse['result']['tvshowdetails'].get('rating')
	       self.Votes    = jSonResponse['result']['tvshowdetails'].get('votes')
	       self.Mpaa     = jSonResponse['result']['tvshowdetails'].get('mpaa')

     def doUpdate( self ):
	  self.getDBTVShow()
	  IMDb = ruDatabase.Query( 'SELECT imdbID FROM tvshows WHERE tvshowID="%s"' % self.FakeIMDb )
	  if not IMDb or IMDb[0][0] == "-":
	       defaultLog( addonLanguage(32250) )
	       doNotify( addonLanguage(32250), 1000 )
	       IMDbID = ""; getByTitle = searchByTitle( self.Title );
	       while IMDbID == "":
		    Notify = False
		    if len( getByTitle ) == 0 and IMDbID != "SKIP":
			 keyBoard = xbmc.Keyboard( self.Title )
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
			      doNotify( doNormalize( addonLanguage(32450) ) + self.Title, -1 )
			      nameList.append( addonLanguage(32457) )
			      nameList.append( addonLanguage(32452) )
			      skipAlways = len( nameList ) - 2
			      editName = len( nameList ) - 1
			      chooseDialog = xbmcgui.Dialog()
			      getResult = chooseDialog.select( addonLanguage(32451), nameList )
			      if getResult == editName:
				   keyBoard = xbmc.Keyboard( self.Title )
				   keyBoard.doModal()
				   if ( keyBoard.isConfirmed() ):
					getTitle = keyBoard.getText()
					getByTitle = searchByTitle( getTitle.decode( 'utf-8' ) )
			      elif getResult == skipAlways: IMDbID = addonLanguage(32458)
			      elif getResult != -1: IMDbID = IMDbIDs[getResult]
			      else: IMDbID = "SKIP"
	       if Notify == True: doNotify( doNormalize( addonLanguage(32450) ) + self.Title, 1 )
	       if IMDbID != "SKIP":
		    defaultLog( "%s: " % self.Title + addonLanguage(32454) % IMDbID )
		    if not IMDb: ruDatabase.Execute( 'INSERT INTO tvshows VALUES ("%s","%s","%s")' % ( self.FakeIMDb, IMDbID, self.Title ) )
		    else: ruDatabase.Execute( 'UPDATE tvshows SET imdbID = "%s" WHERE tvshowID = "%s"' % ( IMDbID, self.FakeIMDb ) )
		    self.doUpdate()
	       else: defaultLog( "%s: " % self.Title + addonLanguage(32453) )
	  else:
	       jSonData = ""
	       if IMDb[0][0] != addonLanguage(32458):
		    defaultLog( addonLanguage(32250) )
		    doNotify( addonLanguage(32250), 1000 )
		    jSonData = getRatings( IMDb[0][0] )
	       else:
		    defaultLog( "%s: %s" % ( self.Title, addonLanguage(32459).lower() ) )
		    doNotify( addonLanguage(32459), 15000 )
	       if jSonData != "":
		    try:
			 jSonData = unicode( jSonData, 'utf-8', errors='ignore' )
			 jSonData = jSon.loads( jSonData )
			 getResponse = jSonData['response']
		    except: getResponse = "false"
		    if getResponse == "true":
			 jsParams = ""; showResult = "";
			 newVotes = jSonData['votes']
			 if newVotes != "0":
			      self.Rating = float( ( "%.1f" % self.Rating ) )
			      newRating = float( jSonData['rating'] )
			      if self.Votes != newVotes or self.Rating != newRating:
				   jsParams += '"rating":' + str( newRating ) + ',"votes":"' + str( newVotes ) + '",'
				   showResult += addonLanguage(32500) % ( str( newRating ), str( newVotes ) )
			      else: showResult += addonLanguage(32502)
			 else: showResult += addonLanguage(32502)
			 if ( addonSettings.getSetting( "MpaaRating" ) == "true"):
			      newMpaa = MpaaPrefixTVShows + jSonData['mpaa']
			      if newMpaa and self.Mpaa != newMpaa:
				   jsParams += '"mpaa":"' + newMpaa + '",'
				   showResult += addonLanguage(32501) % newMpaa
			      else: showResult +=  addonLanguage(32503)
			 if jsParams:
			      jsParams = jsParams[:-1]
			      jSonQuery = '{"jsonrpc":"2.0","method":"VideoLibrary.SetTVShowDetails","params":{"tvshowid":' + str( self.TVShowID ) + ',' + jsParams + '},"id":1}'
			      debugLog( "JSON Query: " + jSonQuery )
			      jSonResponse = xbmc.executeJSONRPC( jSonQuery )
			      jSonResponse = unicode( jSonResponse, 'utf-8', errors='ignore' )
			      debugLog( "JSON Response: " + jSonResponse )
			      jSonResponse = jSon.loads( jSonResponse )
			      if jSonResponse['result'] != "OK": showResult = addonLanguage(32604)
			 defaultLog( "%s: %s" % ( self.Title, showResult[0].lower() + showResult[1:] ) )
			 doNotify( showResult, 15000 )
		    else: return addonLanguage(32605)
	       else:
		    if IMDb[0][0] != addonLanguage(32458): return addonLanguage(32605)

if ( __name__ == "__main__" ):
     TVShows()