# -*- coding: utf-8 -*-

###########################
# Rating Update           #
# by Max (m4x1m) Headroom #
###########################

import sys, xbmc
if sys.version_info >= (2, 7): import json as jSon
else: import simplejson as jSon
from ruCommon import *

class Movies:
     def __init__( self ):
	  getResponse = self.doUpdate()
	  if getResponse:
	       defaultLog( "%s: %s" % ( self.Title, getResponse ) )
	       doNotify( getResponse, 15000 )

     def doUpdate( self ):
	  ID = xbmc.getInfoLabel("ListItem.DBID")
	  jSonQuery = '{"jsonrpc":"2.0","method":"VideoLibrary.GetMovieDetails","params":{"properties":["imdbnumber","rating","votes","mpaa"],"movieid":%s},"id":1}' % ID
	  debugLog( "JSON Query: " + jSonQuery )
	  jSonResponse = xbmc.executeJSONRPC( jSonQuery )
	  jSonResponse = unicode( jSonResponse, 'utf-8', errors='ignore' )
	  debugLog( "JSON Response: " + jSonResponse )
	  jSonResponse = jSon.loads( jSonResponse )
	  if jSonResponse['result'].has_key( 'moviedetails' ):
	       self.Title = jSonResponse['result']['moviedetails'].get('label')
	       IMDb       = jSonResponse['result']['moviedetails'].get('imdbnumber')
	       Rating     = jSonResponse['result']['moviedetails'].get('rating')
	       Votes      = jSonResponse['result']['moviedetails'].get('votes')
	       Mpaa       = jSonResponse['result']['moviedetails'].get('mpaa')
	       if IMDb:
		    defaultLog( addonLanguage(32250) )
		    doNotify( addonLanguage(32250), 1000 )
		    jSonData = getRatings( IMDb )
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
				   Rating = float( ( "%.1f" % Rating ) )
				   newRating = float( jSonData['rating'] )
				   if Votes != newVotes or Rating != newRating:
					jsParams += '"rating":' + str( newRating ) + ',"votes":"' + str( newVotes ) + '",'
					showResult += addonLanguage(32500) % ( str( newRating ), str( newVotes ) )
				   else: showResult += addonLanguage(32502)
			      else: showResult += addonLanguage(32502)
			      if ( addonSettings.getSetting( "MpaaRating" ) == "true"):
				   if ( addonSettings.getSetting( "MpaaReason" ) == "0" and MpaaCountry == "USA" and jSonData['mpaa_reason'] != ""):
					newReason = jSonData['mpaa_reason']
					if Mpaa != newReason:
					     jsParams += '"mpaa":"' + newReason + '",'
					     showResult += addonLanguage(32501) % newReason
					else: showResult += addonLanguage(32503)
				   else:
					newMpaa = MpaaPrefixMovies + jSonData['mpaa']
					if jSonData['mpaa'] and jSonData['mpaa'] != "Not Rated" and Mpaa != newMpaa:
					     jsParams += '"mpaa":"' + newMpaa + '",'
					     showResult += addonLanguage(32501) % newMpaa
					else: showResult +=  addonLanguage(32503)
			      if jsParams:
				   jsParams = jsParams[:-1]
				   jSonQuery = '{"jsonrpc":"2.0","method":"VideoLibrary.SetMovieDetails","params":{"movieid":' + ID + ',' + jsParams + '},"id":1}'
				   debugLog( "JSON Query: " + jSonQuery )
				   jSonResponse = xbmc.executeJSONRPC( jSonQuery )
				   jSonResponse = unicode( jSonResponse, 'utf-8', errors='ignore' )
				   debugLog( "JSON Response: " + jSonResponse )
				   jSonResponse = jSon.loads( jSonResponse )
				   if jSonResponse['result'] != "OK": showResult = addonLanguage(32604)
			      defaultLog( "%s: %s" % ( self.Title, showResult[0].lower() + showResult[1:] ) )
			      doNotify( showResult, 15000 )
			 else: return addonLanguage(32605)
		    else: return addonLanguage(32605)
	       else: return addonLanguage(32606)
	  else: return addonLanguage(32607)

if ( __name__ == "__main__" ):
     Movies()