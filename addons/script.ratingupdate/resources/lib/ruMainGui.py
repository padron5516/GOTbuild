# -*- coding: utf-8 -*-

###########################
# Rating Update           #
# by Max (m4x1m) Headroom #
###########################

import xbmcgui
from ruCommon import *

class ruMainGui( xbmcgui.WindowXMLDialog ):

     def __init__( self, *args, **kwargs ):
	  xbmcgui.WindowXMLDialog.__init__( self )
	  self.doModal()

     def onInit( self ):
	  self.defineControls()
	  self.TitleLabel.setLabel("%s v%s by %s" % ( addonName, addonVersion, addonAuthor ) )
	  self.Top250Button.setLabel( addonLanguage(32101) )
	  if onTop250 == "false": self.Top250Button.setEnabled( False )
	  self.MoviesButton.setLabel( addonLanguage(32102) )
	  if onMovies == "false": self.MoviesButton.setEnabled( False )
	  self.TvShowsButton.setLabel( addonLanguage(32103) )
	  if onTVShows == "false": self.TvShowsButton.setEnabled( False )
	  self.ExitButton.setLabel( addonLanguage(32104) )
	  Check = self.InfoLabel.getLabel()
	  if Check == "": self.InfoLabel.setLabel( addonLanguage(32109) )

     def defineControls( self ):
	  # IDs
	  self.TitleID   = 100
	  self.ImageID   = 101
	  self.InfoID    = 102
	  self.LatestID  = 103
	  self.Top250ID  = 21
	  self.MoviesID  = 22
	  self.TvShowsID = 23
	  self.ExitID    = 24
	  # Controls
	  self.TitleLabel    = self.getControl( self.TitleID )
	  self.ImageLabel    = self.getControl( self.ImageID )
	  self.InfoLabel     = self.getControl( self.InfoID )
	  self.LatestLabel   = self.getControl( self.LatestID )
	  self.Top250Button  = self.getControl( self.Top250ID )
	  self.MoviesButton  = self.getControl( self.MoviesID )
	  self.TvShowsButton = self.getControl( self.TvShowsID )
	  self.ExitButton    = self.getControl( self.ExitID )

     def onClick( self, ID ):
	  if ID == self.Top250ID:
	       from ruMain import Top250
	       self.closeDialog(); Top250(); self.doModal();
	  elif ID == self.MoviesID:
	       from ruMain import Movies
	       self.closeDialog(); Movies(); self.doModal();
	  elif ID == self.TvShowsID:
	       from ruMain import TVShows
	       self.closeDialog(); TVShows(); self.doModal();
	  elif ID == self.ExitID:
	       self.closeDialog()

     def onFocus( self, ID ):
	  try:
	       if ID == self.Top250ID:
		    Latest = ruDatabase.Query( 'SELECT top250 FROM latest' )
		    if Latest[0][0] != "32253":
			 Resume = ruDatabase.Query( 'SELECT top250 FROM resume' )
			 latestTop250 = Latest[0][0] + " (" + addonLanguage( int( Resume[0][0] ) ) + ")"
		    else: latestTop250 = addonLanguage( int( Latest[0][0]) )
		    self.LatestLabel.setLabel( latestTop250 )
		    self.InfoLabel.setLabel( addonLanguage(32106) )
		    self.ImageLabel.setImage( "top250.png" )
	       elif ID == self.MoviesID:
		    Latest = ruDatabase.Query( 'SELECT movies FROM latest' )
		    if Latest[0][0] != "32253":
			 Resume = ruDatabase.Query( 'SELECT movies FROM resume' )
			 latestMovies = Latest[0][0]
			 if (Resume[0][0] == "0"): latestMovies += " (" + addonLanguage(32251) + ")"
			 else: latestMovies += " (" + addonLanguage(32252) + ")"
		    else: latestMovies = addonLanguage( int( Latest[0][0]) )
		    self.LatestLabel.setLabel( latestMovies )
		    self.InfoLabel.setLabel( addonLanguage(32107) )
		    self.ImageLabel.setImage( "movies.png" )
	       elif ID == self.TvShowsID:
		    Latest = ruDatabase.Query( 'SELECT tvshows FROM latest' )
		    if Latest[0][0] != "32253":
			 Resume = ruDatabase.Query( 'SELECT tvshows FROM resume' )
			 latestTvShows = Latest[0][0]
			 if (Resume[0][0] == "0"): latestTvShows += " (" + addonLanguage(32251) + ")"
			 else: latestTvShows += " (" + addonLanguage(32252) + ")"
		    else: latestTvShows = addonLanguage( int( Latest[0][0]) )
		    self.LatestLabel.setLabel( latestTvShows )
		    self.InfoLabel.setLabel( addonLanguage(32108) )
		    self.ImageLabel.setImage( "tvshows.png" )
	       elif ID == self.ExitID:
		    self.LatestLabel.setLabel( "" )
		    self.InfoLabel.setLabel( addonLanguage(32109) )
		    self.ImageLabel.setImage( "exit.png" )
	  except: pass

     def closeDialog( self ):
	  self.close()