# -*- coding: utf-8 -*-

###########################
# Rating Update           #
# by Max (m4x1m) Headroom #
###########################

import xbmc, xbmcaddon, xbmcvfs
import os, time, unicodedata
from datetime import date, datetime, timedelta

addonSettings = xbmcaddon.Addon( "script.ratingupdate" )
addonName     = addonSettings.getAddonInfo( "name" )
addonProfile  = xbmc.translatePath( addonSettings.getAddonInfo( "profile" ) )
addonLanguage = addonSettings.getLocalizedString
BackgroundRun = addonSettings.getSetting( "BackgroundRun" )
WeekDay       = addonSettings.getSetting( "WeekDay" )
DelayTime     = float( addonSettings.getSetting( "DelayTime" ) )
WeekText      = [addonLanguage(32821),addonLanguage(32822),addonLanguage(32823),addonLanguage(32824),addonLanguage(32825),addonLanguage(32826),addonLanguage(32827)]

def doUnicode( textMessage ):
    try: textMessage = unicode( textMessage, 'utf-8' )
    except: pass
    return textMessage

def doNormalize( textMessage ):
     try: textMessage = unicodedata.normalize( 'NFKD', doUnicode( textMessage ) ).encode( 'utf-8' )
     except: pass
     return textMessage

def defaultLog( textMessage ):
     xbmc.log( "[%s] - %s" % ( addonName, doNormalize( textMessage ) ) )

def AutoStart():
     Status = os.path.join( addonProfile, "tmp" )
     CurrentTime = datetime.now().time()
     CurrentTime = datetime( 100, 1, 1, CurrentTime.hour, CurrentTime.minute )
     DelayedTime = CurrentTime + timedelta( minutes=int( DelayTime ) )
     if BackgroundRun == "2":
	  defaultLog( addonLanguage(32655) % ( WeekText[int(WeekDay)], DelayedTime.time() ) )
	  while ( not xbmc.abortRequested ):
	       xbmc.sleep(5000)
	       if date.weekday( date.today() ) == int( WeekDay ):
		    if time.strftime('%H:%M:00') == str( DelayedTime.time() ) and not xbmcvfs.exists( Status ):
			 xbmcvfs.mkdir( Status )
			 xbmc.executebuiltin( "XBMC.RunScript(script.ratingupdate)" )
			 while ( not xbmc.abortRequested and time.strftime('%H:%M:00') == str( DelayedTime.time() ) ): xbmc.sleep(5000)
	       else:
		    if xbmcvfs.exists( Status ): xbmcvfs.rmdir( Status )

if (__name__ == "__main__"):
     AutoStart()
