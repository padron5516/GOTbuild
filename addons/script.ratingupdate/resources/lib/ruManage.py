# -*- coding: utf-8 -*-

###########################
# Rating Update           #
# by Max (m4x1m) Headroom #
###########################

import re, sys, HTMLParser, xbmcgui
if sys.version_info >= (2, 7): import json as jSon
else: import simplejson as jSon
from ruCommon import *

class Manage( xbmcgui.WindowXMLDialog ):

     def __init__( self, *args, **kwargs ):
	  xbmcgui.WindowXMLDialog.__init__( self )
	  self.doModal()

     def onInit( self ):
	  self.defineControls()
	  self.TitleLabel.setLabel( addonName + " v" + addonVersion + " - " + addonLanguage(32550) )
	  self.Info01Label.setLabel( addonLanguage(32651) )
	  self.Info02Label.setLabel( addonLanguage(32652) )
	  self.CleanButton.setLabel( addonLanguage(32650) )
	  self.ExitButton.setLabel( addonLanguage(32104) )
	  self.ItemsList.reset()
	  TVShows = ruDatabase.Execute( 'SELECT * FROM tvshows ORDER BY Title ASC' )
	  for Item in TVShows: self.ItemsList.addItem( xbmcgui.ListItem( label=Item[2].encode( 'utf-8' ), label2=Item[1] ) )

     def defineControls( self ):
	  # IDs
	  self.ListID   = 10
	  self.TitleID  = 80
	  self.Info01ID = 81
	  self.Info02ID = 82
	  self.CleanID  = 90
	  self.ExitID   = 91
	  # Controls
	  self.ItemsList  = self.getControl( self.ListID )
	  self.TitleLabel = self.getControl( self.TitleID )
	  self.Info01Label = self.getControl( self.Info01ID )
	  self.Info02Label = self.getControl( self.Info02ID )
	  self.CleanButton = self.getControl( self.CleanID )
	  self.ExitButton = self.getControl( self.ExitID )

     def onClick( self, ID ):
	  if ID == self.ListID:
	       self.close()
	       defaultLog( addonLanguage(32250) )
	       doNotify( addonLanguage(32250), 1000 )
	       titleSelected = self.ItemsList.getSelectedItem()
	       TVShowTitle = titleSelected.getLabel()
	       IMDbID = ""; getByTitle = searchByTitle( str( TVShowTitle ).decode( 'utf-8' ) );
	       while IMDbID == "":
		    Notify = False
		    if len( getByTitle ) == 0 and IMDbID != "SKIP":
			 keyBoard = xbmc.Keyboard( TVShowTitle )
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
			      doNotify( doNormalize( addonLanguage(32450) ) + str( TVShowTitle ), -1 )
			      nameList.append( addonLanguage(32457) )
			      nameList.append( addonLanguage(32452) )
			      skipAlways = len( nameList ) - 2
			      editName = len( nameList ) - 1
			      chooseDialog = xbmcgui.Dialog()
			      getResult = chooseDialog.select( addonLanguage(32451), nameList )
			      if getResult == editName:
				   keyBoard = xbmc.Keyboard( TVShowTitle )
				   keyBoard.doModal()
				   if ( keyBoard.isConfirmed() ):
					getTitle = keyBoard.getText()
					getByTitle = searchByTitle( getTitle.decode( 'utf-8' ) )
			      elif getResult == skipAlways: IMDbID = addonLanguage(32458)
			      elif getResult != -1: IMDbID = IMDbIDs[getResult]
			      else: IMDbID = "SKIP"
	       if Notify == True: doNotify( doNormalize( addonLanguage(32450) ) + str( TVShowTitle ), 1 )
	       if IMDbID != "SKIP":
		    defaultLog( "%s: " % str( TVShowTitle ).decode( 'utf-8' ) + addonLanguage(32455) % IMDbID )
		    ruDatabase.Execute( 'UPDATE tvshows SET imdbID = "%s" WHERE Title="%s"' % ( IMDbID, TVShowTitle ) )
	       else: defaultLog( "%s: " % str( TVShowTitle ).decode( 'utf-8' ) + addonLanguage(32453) )
	       self.doModal()
	  elif ID == self.CleanID:
	       self.close()
	       ruTVShows = []; DBTVShows = []; Removed = 0;
	       TVShows = ruDatabase.Query( 'SELECT tvshowID FROM tvshows ORDER BY Title ASC' )
	       for TVShow in TVShows: ruTVShows.append( TVShow[0] )
	       jSonQuery = '{"jsonrpc":"2.0","method":"VideoLibrary.GetTVShows","params":{"properties":["imdbnumber"],"sort":{"order":"ascending","method":"label","ignorearticle":true}},"id":1}'
	       debugLog( "JSON Query: " + jSonQuery )
	       jSonResponse = xbmc.executeJSONRPC( jSonQuery )
	       jSonResponse = unicode( jSonResponse, 'utf-8', errors='ignore' )
	       debugLog( "JSON Response: " + jSonResponse )
	       jSonResponse = jSon.loads( jSonResponse )
	       try:
		    if jSonResponse['result'].has_key( 'tvshows' ):
			 for item in jSonResponse['result']['tvshows']:
			      FakeIMDb = item.get('imdbnumber')
			      DBTVShows.append( FakeIMDb )
	       except: pass
	       for ruTVShow in ruTVShows:
		    if ruTVShow not in DBTVShows:
			 ruDatabase.Execute( 'DELETE FROM tvshows WHERE tvshowID = "%s"' % ruTVShow )
			 Removed = Removed + 1
	       dialogOK( addonLanguage(32600), addonLanguage(32653), addonLanguage(32654) % Removed, "" )
	       defaultLog( addonLanguage(32653) + ": " + addonLanguage(32654) % Removed )
	       self.doModal()
	  if ID == self.ExitID: self.close()

if ( __name__ == "__main__" ):
     Manage( "script_rating_update-lists.xml", addonSettings.getAddonInfo( "path" ), "Default" )