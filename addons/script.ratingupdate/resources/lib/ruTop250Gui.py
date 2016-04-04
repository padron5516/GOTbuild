# -*- coding: utf-8 -*-

###########################
# Rating Update           #
# by Max (m4x1m) Headroom #
###########################

import xbmcgui
from ruCommon import *

class ruTop250Gui( xbmcgui.WindowXMLDialog ):

     def __init__( self, xmlFile, resourcePath, defaultName = 'Default', forceFallback = False, parent = None ):
	  xbmcgui.WindowXML.__init__( self )
	  self.parent = parent
	  self.doModal()

     def onInit( self ):
	  self.defineControls()
	  self.TitleLabel.setLabel( addonName + " v" + addonVersion + " - " + addonLanguage(32306) )
	  self.FakeButton.setVisible( False )
	  self.ExitButton.setLabel( addonLanguage(32104) )
	  self.ItemsList.reset()
	  for Item in self.parent.MissingTop250: self.ItemsList.addItem( xbmcgui.ListItem( label=Item[0], label2=Item[1] ) )

     def defineControls( self ):
	  # IDs
	  self.ListID  = 10
	  self.TitleID = 80
	  self.FakeID = 90
	  self.ExitID  = 91
	  # Controls
	  self.ItemsList   = self.getControl( self.ListID )
	  self.TitleLabel  = self.getControl( self.TitleID )
	  self.FakeButton = self.getControl( self.FakeID )
	  self.ExitButton  = self.getControl( self.ExitID )

     def onClick( self, ID ):
	  if ID == self.ListID: pass
	  if ID == self.ExitID: self.close()