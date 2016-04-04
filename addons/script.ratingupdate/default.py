# -*- coding: utf-8 -*-

###########################
# Rating Update           #
# by Max (m4x1m) Headroom #
###########################

import os, sys
import xbmc, xbmcgui, xbmcaddon
from resources.lib.ruCommon import *

addonSettings   = xbmcaddon.Addon( "script.ratingupdate" )
addonName       = addonSettings.getAddonInfo( "name" )
addonVersion    = addonSettings.getAddonInfo( "version" )
addonResource   = os.path.join( addonSettings.getAddonInfo( "path" ), "resources", "lib" )
addonLanguage   = addonSettings.getLocalizedString

if "win32" in sys.platform: binaryName = "php-cgi.exe"
elif "linux" in sys.platform or "darwin" in sys.platform: binaryName = "php-cgi"
binaryPath  = os.path.normpath( os.path.join( addonSettings.getSetting( "BinaryPath" ), binaryName ) )

binaryCheck = "True"; dbCheck = "True";
try: open( binaryPath ).close()
except:
     binaryCheck = "False"
     xbmcgui.Dialog().ok( "%s - %s" % ( addonName, addonLanguage(32601) ),  addonLanguage(32608), addonLanguage(32609) )

if RawQueries == "true":
     try: dbTest = RawXBMC.Execute( 'SELECT idVersion FROM version' )
     except:
	  dbCheck = "False"
	  xbmcgui.Dialog().ok( "%s - %s" % ( addonName, addonLanguage(32601) ),  addonLanguage(32612), addonLanguage(32613) )

if binaryCheck == "True" and dbCheck == "True":
     try:
	  try: getParams = dict( arg.split( "=" ) for arg in sys.argv[ 1 ].split( "&" ) )
	  except: getParams = dict( sys.argv[ 1 ].split( "=" ))
     except: getParams = {}
     addonSwitch = getParams.get( "Single" )
     if addonSwitch == "Movie":
	  xbmc.log( "[%s] - Starting %s v%s (Single Mode Movie)" % ( addonName, addonName, addonVersion ) )
	  xbmc.executebuiltin( 'XBMC.RunScript(%s)' % os.path.join( addonResource , "ruMovie.py" ) )
     elif addonSwitch == "TVShow":
	  xbmc.log( "[%s] - Starting %s v%s (Single Mode TVShow)" % ( addonName, addonName, addonVersion ) )
	  xbmc.executebuiltin( 'XBMC.RunScript(%s)' % os.path.join( addonResource , "ruTVShow.py" ) )
     else:
	  xbmc.log( "[%s] - Starting %s v%s" % ( addonName, addonName, addonVersion ) )
	  xbmc.executebuiltin( 'XBMC.RunScript(%s)' % os.path.join( addonResource , "ruMain.py" ) )