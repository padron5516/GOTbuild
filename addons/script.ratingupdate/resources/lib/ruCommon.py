# -*- coding: utf-8 -*-

###########################
# Rating Update           #
# by Max (m4x1m) Headroom #
###########################

import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import os, sys, subprocess, unicodedata
from subprocess import Popen, PIPE

addonSettings   = xbmcaddon.Addon( "script.ratingupdate" )
addonName       = addonSettings.getAddonInfo( "name" )
addonAuthor     = addonSettings.getAddonInfo( "author" )
addonVersion    = addonSettings.getAddonInfo( "version" )
addonResource   = os.path.join( addonSettings.getAddonInfo( "path" ), "resources", "lib" )
addonIcon       = os.path.join( addonSettings.getAddonInfo( "path" ), "icon.png" )
addonProfile    = xbmc.translatePath( addonSettings.getAddonInfo( "profile" ) )
addonLanguage   = addonSettings.getLocalizedString

if not xbmcvfs.exists( addonProfile ): xbmcvfs.mkdir( addonProfile )

onTop250          = addonSettings.getSetting( "Top250" )
onMovies          = addonSettings.getSetting( "Movies" )
onTVShows         = addonSettings.getSetting( "TVShows" )
MpaaCountry       = addonSettings.getSetting( "MpaaCountry" )
MpaaPrefixMovies  = addonSettings.getSetting( "MpaaPrefixMovies" )
MpaaPrefixTVShows = addonSettings.getSetting( "MpaaPrefixTVShows" )
BackgroundRun     = addonSettings.getSetting( "BackgroundRun" )
ResumeResponse    = addonSettings.getSetting( "ResumeResponse" )
HideProgress      = addonSettings.getSetting( "HideProgress" )
RawQueries        = addonSettings.getSetting( "RawQueries" )
DBType            = addonSettings.getSetting( "DBType" )
DBName            = addonSettings.getSetting( "DBName" )
DBHost            = addonSettings.getSetting( "DBHost" )
DBUser            = addonSettings.getSetting( "DBUser" )
DBPass            = addonSettings.getSetting( "DBPass" )
MissingTop250     = os.path.normpath( addonSettings.getSetting( "MissingPath" ) )
if ( MissingTop250 == "."): MissingTop250 = os.path.join( addonProfile, "Missing_TOP250.txt" )
else: MissingTop250 = os.path.join( MissingTop250, "Missing_TOP250.txt" )

Local = '%d %b %Y'
CheckLocal = xbmc.getRegion( 'dateshort' ).lower()
if CheckLocal[0] == 'm': Local = '%b %d, %y'

if "win32" in sys.platform:
     binaryName = "php-cgi.exe"
     startupinfo = subprocess.STARTUPINFO()
     startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
     startupinfo.wShowWindow = subprocess._subprocess.SW_HIDE
elif "linux" in sys.platform or "darwin" in sys.platform:
     binaryName = "php-cgi"; startupinfo = None;
binaryPath  = os.path.normpath( os.path.join( addonSettings.getSetting( "BinaryPath" ), binaryName ) )

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

def debugLog( textMessage ):
     xbmc.log( "[%s] - %s" % ( addonName, doNormalize( textMessage ) ), level = xbmc.LOGDEBUG )

def dialogOK( T, A, B, C ):
     xbmcgui.Dialog().ok( "%s - %s" % ( addonName, T ), "%s" % A, "%s" % B, "%s" % C )

def dialogQuestion( T, A, B, C, N, Y ):
     Q = xbmcgui.Dialog().yesno("%s - %s" % ( addonName, T ), "%s" % A, "%s" % B, "%s" % C, "%s" % N, "%s" % Y )
     return Q

def doNotify( textMessage, millSec ):
     xbmc.executebuiltin( 'Notification( "%s", "%s", %s, "%s")' % ( addonName, textMessage.encode('utf-8'), millSec, addonIcon ) )

def getTop250():
     jXmlData = ""; top250Path  = os.path.normpath( os.path.join( addonResource, "php", "getTop250.php" ) );
     jXmlData = Popen([r"" + binaryPath + "","-q",r"" + top250Path + ""], startupinfo=startupinfo, stdout=PIPE).communicate()[0]
     debugLog( 'PHP Command: ' + binaryPath + ' -q ' + top250Path )
     debugLog( 'XML Response: ' + jXmlData )
     return jXmlData

def getRatings( IMDb ):
     jSonData = ""; ratingsPath = os.path.normpath( os.path.join( addonResource, "php", "getRatings.php" ) );
     jSonData = Popen([r"" + binaryPath + "","-q",r"" + ratingsPath + "","-d","ID=" + IMDb + "","Country=" + MpaaCountry + ""], startupinfo=startupinfo, stdout=PIPE).communicate()[0]
     debugLog( 'PHP Command: ' + binaryPath + ' -q ' + ratingsPath + ' -d ID=' + IMDb + ' Country=' + MpaaCountry )
     debugLog( 'JSON Response: ' + jSonData )
     return jSonData

def searchByTitle( Title ):
     jXmlData = ""; searchPath  = os.path.normpath( os.path.join( addonResource, "php", "searchByTitle.php" ) );
     jXmlData = Popen([r"" + binaryPath + "","-q",r"" + searchPath + "","-d","Title=\"" + Title.encode( 'utf-8' ) + "\""], startupinfo=startupinfo, stdout=PIPE).communicate()[0]
     debugLog( 'PHP Command: ' + binaryPath + ' -q ' + searchPath + ' -d Title="' + doNormalize( Title ) + '"' )
     debugLog( 'XML Response: ' + jXmlData )
     return jXmlData

class ruDatabase():
     @staticmethod
     def Query( Query ):
	  ruDatabaseConnect = ConnectToDb()
	  Cursor = ruDatabaseConnect.cursor()
	  Cursor.execute( Query )
	  Matches = []
	  for Row in Cursor: Matches.append( Row )
	  ruDatabaseConnect.commit()
	  Cursor.close()
	  return Matches

     @staticmethod
     def Execute( Query ):
	  return ruDatabase.Query( Query )

def ConnectToDb():
     import sqlite3
     dbHost = os.path.join ( addonProfile, "ruDatabase.db" )
     return sqlite3.connect( dbHost )

class RawXBMC():
     @staticmethod
     def Query( Query ):
	  RawXBMCConnect = ConnectToXbmcDb()
	  Cursor = RawXBMCConnect.cursor()
	  Cursor.execute( Query )
	  Matches = []
	  for Row in Cursor: Matches.append( Row )
	  RawXBMCConnect.commit()
	  Cursor.close()
	  return Matches

     @staticmethod
     def Execute( Query ):
	  return RawXBMC.Query( Query )

def ConnectToXbmcDb():
     if DBType == "0":
	  import sqlite3
	  dbPath = xbmc.translatePath( "special://database" )
	  dbHost = os.path.join ( dbPath, DBName + ".db" )
	  return sqlite3.connect( dbHost )
     else:
	  import mysql.connector
	  return mysql.connector.Connect( host = str( DBHost ), port = int( "3306" ), database = str( DBName ), user = str( DBUser ), password = str( DBPass ) )

ActualDBVersion = "1.0"
if not xbmcvfs.exists( os.path.join ( addonProfile, "ruDatabase.db" ) ):
     defaultLog( addonLanguage(32610) )
     ruDatabase.Execute( 'CREATE TABLE latest (top250 TEXT, movies TEXT, tvshows TEXT)')
     ruDatabase.Execute( 'INSERT INTO latest (top250, movies, tvshows) VALUES ("32253", "32253", "32253")')
     ruDatabase.Execute( 'CREATE TABLE resume (top250 TEXT, movies TEXT, tvshows TEXT)')
     ruDatabase.Execute( 'INSERT INTO resume (top250, movies, tvshows) VALUES ("0", "0", "0")')
     ruDatabase.Execute( 'CREATE TABLE tvshows (tvshowID TEXT, imdbID TEXT, Title TEXT)')
     ruDatabase.Execute( 'CREATE TABLE version (version TEXT)')
     ruDatabase.Execute( 'INSERT INTO version (version) VALUES ("' + ActualDBVersion + '")')
else:
     CurrenDBVersion = ruDatabase.Query( 'SELECT version FROM version' )
     if CurrenDBVersion[0][0] != ActualDBVersion:
	  defaultLog( addonLanguage(32611) % ActualDBVersion )
	  ruDatabase.Execute( 'UPDATE version SET version="%s"' % ActualDBVersion )
	  # From here follows the new code for the tables to be altered
