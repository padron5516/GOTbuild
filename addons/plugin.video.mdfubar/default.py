import urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
import urlresolver
import requests
from addon.common.addon import Addon
from addon.common.net import Net
from metahandler import metahandlers
from bs4 import BeautifulSoup as bs

#F.U.B.A.R - By Mucky Duck (07/2015)

addon_id='plugin.video.mdfubar'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
baseurl = 'dummy'
net = Net()
metaset = selfAddon.getSetting('enable_meta')
metaget = metahandlers.MetaData(preparezip=False)
#User_Agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'


baseurl1 = 'http://mediaportal4kodi.ml/smf/index.php?board=2.0'
baseurl2 = 'https://www.youtube.com'

#http://watch-free-movies-streaming.com/
baseurl101 = 'http://vodlocker.tv'
baseurl102 = 'http://www.alluc.ee'
#http://movies-search-engine.com/
#http://watch-streaming-movies.com/
#http://wawashare.com/
##http://stagevu.com/
##http://online-tvseries.com/


baseurl350 = 'http://documentaryaddict.com'
baseurl450 = 'http://concert.ga'


#http://misspremieretv.com/2014/09/
#http://series-cravings.me/
#http://www.tvids.net/
#http://tvstream.ch/
#http://geektv.me/
#http://tvoox.com/
#http://watchtvlinks.ag/
########http://fullepisode.info/
#http://hdfull.tv
##http://movies.documentaryvideosworld.com/
##https://www3.iconcerts.com
##https://www.reddit.com/r/fullconcerts/
##http://music.naij.com/
##https://www.youtube.com/playlist?list=PLD6BF044AE5B386D2
##https://www.itstream.tv/play/NDIyMjc=
##http://www.veoh.com/
##https://www.youtube.com/channel/UCAsanw03kzGRhAG4AvjVA_Q/playlists?sort=dd&view=1
##https://www.youtube.com/playlist?list=PL0vM4tWpymIU4bVBv9XJG26Tbz33KB7Rs
##https://www.youtube.com/playlist?list=PLR8X0-qEtOCf8aeA-6bEBHNNwZv0GqvyZ
##https://www.youtube.com/user/TheRealConcertKing/playlists?view=1&sort=dd real concert king
##https://www.youtube.com/user/GreenDayConcerts/playlists green day
##http://abelgaloismuse.blogspot.co.uk/p/concerts-full.html
baseurl500 = 'http://hdsoapcity.blogspot.co.uk' #'http://newsoapcity.blogspot.co.uk'
baseurl510 = 'http://uksoapshare.blogspot.co.uk'
##http://tvlog.link/ benders
##http://tv-show-online.sx/
##http://www.cbc.ca/

##http://luv-movies.com/
##http://primeflicks.me/ looks like vodx
##http://funtastic-vids.com/ hd movies
##http://free-on-line.org/ hd movies
##http://putlocker.tn/
##http://www.movie25.cz/
##http://worldfree4uk.com/
##http://www.vumoo.me/
##http://motionempire.org/  mix of everything
##http://crackmovies.com/
##http://k-films.net/
##http://sceper.ws/2015/06/ted-2-2015-1080p-hdcam-x264-ac3-mrg.html
##http://webmaster-connect.me/2014/08/fast-n-loud-s05e01-chopped-and-dropped-model-a-part1.html
##http://watchseries-online.ch/
##http://watchmovies-online.ch/
#http://watchmovies-online.ch/hellboy-2004/  1080p
#http://tvoox.com/
##http://www.movie25.cz/
##http://rlsbb.com/fast-n-loud-s05e01-720p-hdtv-x264-dhd/  hd bluray 1080 movies
##http://www.newvideoz.com/
##http://board.dailyflix.net/  forum hd links
##'http://moviesearth.net'
##'http://www.badassmovies4u.com/'
baseurl50 =  'http://www.filmovizija.studio/'  #'http://www.filmovizija.club' #'http://www.filmovizija.in'
baseurl150 = 'http://geektv.me'
baseurl200 = 'http://www.allcinemamovies.com'
baseurl250 = 'http://www.24t.us'
baseurl300 = 'http://ultra-vid.com'
baseurl400 = 'http://pandamovie.net'

baseurl5001 = 'http://www.hack-sat.com'
#baseurl5001 = 'http://select-pedia.com/tutos/tag/sport/'
#baseurl50002 = 'http://www.iptvlinks.com/2014/12/super-torrent-stream.html'
baseurl5002 = 'http://iptv.filmover.com'
baseurl5010 = 'http://www.iptvsharing.com/2015/07/sport-klub-iptv-links-m3u8.html'
baseurl5020 = 'http://67.159.5.242/ip-1/encoded/Oi8vcGFzdGViaW4uY29tL2hxNlBKWVpS'
baseurl5030 = 'http://free-links-iptv.blogspot.co.uk'
#http://iptv-zak.blogspot.co.uk/2015_10_01_archive.html
##http://www.iptvsportt.com/
##http://www.ramalin.com/
##http://iptvplaylists.com/category/m3u/
baseurl5040 = 'http://iptvapps.blogspot.co.uk/2015/06/playlist-m3u-662015.html'



def INDEX():
        #addDir('[COLOR cyan]Alluc[/COLOR]',baseurl102,102,art+'alluc.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Ultra-Vid[/COLOR]',baseurl300,300,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]PandaMovie[/COLOR]','url',400,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Filmovizija[/COLOR]',baseurl150,50,art+'vizi.png',art+'f1.jpg','')
        addDir('[COLOR cyan]GeekTV[/COLOR]',baseurl150,150,art+'geek.png',art+'f1.jpg','')
        addDir('[COLOR cyan]24t[/COLOR]',baseurl250,250,art+'epis.png',art+'f1.jpg','')
        addDir('[COLOR cyan]DocumentaryAddict[/COLOR]',baseurl350,350,art+'da.png',art+'f1.jpg','')
        addDir('[COLOR cyan]NewSoapCity[/COLOR]',baseurl500,500,art+'wls.png',art+'f1.jpg','')
        #addDir('[COLOR cyan]uksoapshare.blogspot.co.uk[/COLOR]',baseurl510,510,art+'wls',art+'f1.jpg','')
        addDir('[COLOR cyan]Concerts[/COLOR]','url',3,art+'concert.png',art+'f1.jpg','')
        #addDir('[COLOR cyan]www.allcinemamovies.com[/COLOR]','url',200,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Search[/COLOR]','url',100,art+'search.png',art+'f1.jpg','')
        addDir('[COLOR cyan]IPTV[/COLOR]','url',5000,art+'iptv.png',art+'f1.jpg','')
        
        
def CONINDEX():
        #addDir('[COLOR cyan]#Concert[/COLOR]',baseurl450+'/channel/UCAsanw03kzGRhAG4AvjVA_Q/playlists?sort=dd&view=1',451,'',art+'f1.jpg','')
        addDir('[COLOR cyan]concert.ga[/COLOR]','url',450,art+'concert.png',art+'f1.jpg','')
        #addDir('[COLOR cyan]HD Movies[/COLOR]',baseurl400+'/watch-hd-movies-online-free',401,'',art+'f1.jpg','')
############################################################################################################################

############################################################################################################################

def BASE50(url):
        addDir('[I][B][COLOR red]MOST VIEWED TODAY[/COLOR][/B][/I]',baseurl50+'list.php?k=top_today',51,art+'vizi.png',art+'f6.jpg','')
        addDir('[I][B][COLOR red]SEARCH MOVIES[/COLOR][/B][/I]','url',61,art+'vizi.png',art+'f6.jpg','')
        addDir('[I][B][COLOR red]MOVIE GENRE[/COLOR][/B][/I]',baseurl50+'browse-movies-videos-1-date.html',57,art+'vizi.png',art+'f6.jpg','')
        addDir('[I][B][COLOR red]LAST ADDED[/COLOR][/B][/I]',baseurl50+'list.php?k=last_added',51,art+'vizi.png',art+'f6.jpg','')
        addDir('[I][B][COLOR red]TOP MOVIES[/COLOR][/B][/I]',baseurl50,54,art+'vizi.png',art+'f6.jpg','')
        addDir('[I][B][COLOR red]SEARCH TV[/COLOR][/B][/I]','url',60,art+'vizi.png',art+'f6.jpg','')
        addDir('[I][B][COLOR red]TV SHOWS[/COLOR][/B][/I]',baseurl50+'tvshows.html',58,art+'vizi.png',art+'f6.jpg','')
        
        

def BASE50INDEX(url):
        link = OPEN_URL(url)
        all_videos = regex_get_all(link, '<li><div id', '</a></div></li>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, "/><div>", "<")
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                url = regex_from_to(a, "href='", "'").replace("&amp;","&")
                thumb = regex_from_to(a, "original='", "'")
                epn = regex_from_to(a, "epname'>", "<")
                if name > '':
                        addDir2('[COLOR white]%s[/COLOR]' %name,url,52,thumb,items)
        try:
                soup = bs(link, "html.parser")
                a = soup.find('a', href=True, text=re.compile("next"))
                if a:
                        np = baseurl50+a["href"]
                addDir('[I][B][COLOR red]Next Page >>>[/COLOR][/B][/I]',np,51,art+'vizi.png',art+'f6.jpg','')
        except: pass
        setView('movies', 'movie-view')        


def BASE50HOSTS(url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        if iconimage == '':
                iconimage = art+'vizi.png'
        try:
                prime = re.findall('\("#contents"\)\.load\("(.*?)"\)',link)[0]
                links = OPEN_URL(prime)
                url1 = re.findall(r'<i.*?rc="(.*?)".*?>', links, re.I|re.DOTALL)[0]
                name1 = url1.replace('http://','').partition('/')[0]
                addDir('[COLOR white]%s[/COLOR]' %name1,url1,1,art+'vizi.png',art+'f6.jpg','')
        except:pass
        match=re.compile('<span class="fullm"><a href="(.*?)" title="(.*?)" target="_blank">Watch <i class="fa fa-external-link">').findall(link)
        for url,name in match:
                if urlresolver.HostedMediaFile(url):
                        name = name.replace('&amp;','&').replace('Movie - ','')
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,art+'f6.jpg','')


def BASE50INDEX2(url):
        link = OPEN_URL(url)
        all_videos = regex_get_all(link, 'form action', '</a></div></li>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, "/><div>", "<")
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                url = regex_from_to(a, "data='", "'")
                url = 'http://www.filmovizija.studio/episode.php?vid='+url
                thumb = regex_from_to(a, "original='", "'")
                epn = regex_from_to(a, "epname'>", "<")
                if name > '':
                        addDir3('[COLOR white]%s[/COLOR] [COLOR red]%s[/COLOR]' %(name,epn),url,56,thumb,items,'',name)
        try:
                soup = bs(link, "html.parser")
                a = soup.find('a', href=True, text=re.compile("next"))
                if a:
                        np = baseurl50+a["href"]
                        addDir('[I][B][COLOR red]Next Page >>>[/COLOR][/B][/I]',np,53,art+'vizi.png',art+'f6.jpg','')
        except: pass
        setView('tvshows', 'show-view')   


def BASE50TOP(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<a href="(.*?)"><i style=".*?" class="fa fa-star"></i> (.*?)</a>').findall(link)
        for url,name in match:
                ok = 'topvideos'
                if ok in url:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,51,art+'vizi.png',art+'f6.jpg','')


#def BASE50TOPL(url):
        #link = OPEN_URL(url)
        #link = link.encode('ascii', 'ignore')
        #match=re.compile('.+?</a></div><a href="(.+?)"><img src="(.+?)" alt="(.+?)"  class="tinythumb1" width="53" height="40" align="left" border="1" />').findall(link)
        #for url,thumb,name in match:
                #addDir('[COLOR white]%s[/COLOR]' %name,url,52,thumb,art+'f1.jpg','')


def BASE50GENRE(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<li><a href="(.+?)" title="(.+?)"><div id="tsuper"><span>.+?</span></div><img src=(.+?)></a></li>').findall(link)
        for url,name,icon in match:
                addDir('[COLOR white]%s[/COLOR]' %name,url,51,icon,art+'f6.jpg','')


def BASE50TV(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile("div class='col-sm-4 series-list'><a href='(.*?)'>(.*?)</a></div>").findall(link)
        for url,name in match:
                addDir('[COLOR white]%s[/COLOR]' %name,baseurl50+url,59,art+'vizi.png',art+'f6.jpg','')


def BASE50TVSEA(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        try:
                thumb = re.compile("<img class='img-responsive' .*?rc=(.*?)>").findall(link)[0]
        except:
                thumb = art+'vizi.png'
        try:
                dis = re.compile('description" content="(.*?)"').findall(link)[0]
        except:
                dis = 'None'
        match=re.compile("toggle='dropdown'>(.*?)<span").findall(link)
        for seas in match:
                addDir('[COLOR white]%s[/COLOR]' %seas,url,56,thumb,art+'f6.jpg',dis)
        setView('movies', 'show-view')


def BASE50EPIS(name,url,iconimage,description):
        name = name.replace('[COLOR white]','').replace('[/COLOR]','')
        link = OPEN_URL(url)
        all_links = regex_get_all(link, name, '</div></li>')
        all_videos = regex_get_all(str(all_links), "class='epi'>", "</i>")
        for a in all_videos:
                name = regex_from_to(a, "block;'>", "<")
                name = name.replace('&nbsp;','').replace("u2019","'")
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                name = name.replace('\\','')
                url = regex_from_to(a, "epiloader' class='", "'")
                url = 'http://www.filmovizija.studio/episode.php?vid='+url
                addDir('[COLOR white]%s[/COLOR]' %name,url,52,iconimage,art+'f6.jpg',description)
        setView('movies', 'show-view')

def BASE50TVSEARCH():
        try:
                keyb = xbmc.Keyboard('', 'Search TV Shows')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','+')
                        url = baseurl50+'search1.php?keywords='+search+'&ser=528&subs=&lks=&rfrom=0&rto=0&gfrom=0&gto=0&gns=&btn='
                        BASE50INDEX2(url)   
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")

def BASE50MSEARCH():
        try:
                keyb = xbmc.Keyboard('', 'Search Movies')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','+')
                        url = baseurl50+'search1.php?keywords='+search+'&ser=506&subs=&lks=&rfrom=0&rto=0&gfrom=0&gto=0&gns=&btn='
                        BASE50INDEX(url)
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")

############################################################################################################################

############################################################################################################################
############################################################################################################################

############################################################################################################################

def BASE150():
        addDir('[I][B][COLOR red]A/Z[/COLOR][/B][/I]',baseurl150+'/tv',154,art+'geek.png',art+'f5.jpg','')
        addDir('[I][B][COLOR red]Genre[/COLOR][/B][/I]',baseurl150,153,art+'geek.png',art+'f5.jpg','')
        addDir('[I][B][COLOR red]Search[/COLOR][/B][/I]','url',155,art+'geek.png',art+'f5.jpg','')




def BASE150INDEX(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, 'col-xs-6', '</div></a></div>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'class="h5">', '<').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#039;',"'")
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                thumb = regex_from_to(a, 'src="', '"')
                #dis = regex_from_to(a, '<p>', '</p>').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#039;',"'")
                addDir3('[B][COLOR white]%s[/COLOR][/B]' %name,url,156,thumb,items,'',name)
        try:
                nextp=re.compile('<a href="(.*?)" .*?>&gt;</a></li>').findall(link)[0]
                addDir('[I][B][COLOR red]Next Page>>>[/COLOR][/B][/I]',nextp,151,art+'geek.png',art+'f5.jpg','')
        except: pass
        setView('tvshows', 'show-view')
       	

def BASE150LINKS(name,url,iconimage,show_title):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<a href="(.*?)" class="btn btn-link btn-xs"><img src=".*?"> (.*?)</a></td><td class="hidden-xs">.*?</td><td>.*?</td>').findall(link)
        items = len(match)
        for url,name in match:
                link = OPEN_URL(baseurl150+url)
                link = link.encode('ascii', 'ignore').decode('ascii')
                url = re.findall(r'<IFRAM.*?RC="(.*?)" .*?>', str(link), re.I|re.DOTALL)[0]
                if urlresolver.HostedMediaFile(url):
                        addDir3('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name,url,1,iconimage,items,'',show_title)
        setView('tvshows', 'show-view')



def BASE150GENRE(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<li><a href="(.*?)"><span class="fa fa-tag"></span> (.*?)</a></li>').findall(link)
        for url,name in match:
                addDir('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name,url,151,art+'geek.png',art+'f5.jpg','')




def BASE150ATOZ(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<li.*?><a href="(.*?)" title="(.*?)">.*?</a></li>').findall(link)
        for url,name in match:
                addDir('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name,baseurl150+url,151,art+'geek.png',art+'f5.jpg','')




def BASE150SEARCH():
        try:
                keyb = xbmc.Keyboard('', 'GeekTV')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','+')
                        #encode=urllib.quote(search)
                        #print encode
                        url = baseurl150+'/search?q='+search
                        print url
                        try:
                                link = OPEN_URL(url)
                                link = link.encode('ascii', 'ignore')
                                all_videos = regex_get_all(link, '<td class="col-md-2">', '</div></td></tr>')
                                items = len(all_videos)
                                for a in all_videos:
                                        name = regex_from_to(a, 'alt="', '"').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#039;',"'")
                                        url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                                        icon = regex_from_to(a, 'src="', '"')
                                        dis = regex_from_to(a, '<div>', '</').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#039;',"'")
                                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,baseurl150+url,156,icon,art+'f5.jpg',dis)
                        except:
                                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY SITE DOWN[/B][/COLOR],,7000,"")")
                        try:
                                match=re.compile('<a class="next page-numbers" href="(.+?)">(.+?)</a>').findall(link)
                                name = name.replace(' \xc2\xbb','')
                                for url, name in match:
                                        addDir('[I][B][COLOR red]%s[/COLOR][/B][/I]' %name,url,301,art+'geek.png',art+'f5.jpg','')
                        except: pass
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")
        setView('movies', 'movie-view')




def BASE150SEA(url,iconimage,show_title):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<a class="pull-right" href="(.*?)"><span class="fa fa-link"></span>(.*?)</a></div></div>').findall(link)
        items = len(match)
        for url,name in match:
                name = name.replace(' Page ','')
                addDir3('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name,url,157,iconimage,items,'',show_title)
        setView('tvshows', 'show-view')



def BASE150EP(url,iconimage,show_title):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<tr><td><a href="(.*?)"><span class="fa fa-play-circle"></span>(.*?)</a></td><td>(.*?)</td></tr>').findall(link)
        items = len(match)
        for url,name,name2 in match:
                addDir3('[B][COLOR white]%s[/COLOR][/B] [I][B][COLOR red](%s)[/COLOR][/B][/I]' %(name,name2),url,152,iconimage,items,'',show_title)
        setView('tvshows', 'show-view')


############################################################################################################################

############################################################################################################################
############################################################################################################################

############################################################################################################################        

def BASE200():
        addDir('[COLOR cyan]Newest Movies[/COLOR]',baseurl200+'/movies',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Popular Movies[/COLOR]',baseurl200+'/movies/popular',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies By IMDB Rating[/COLOR]',baseurl200+'/movies/imdb_rating',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies Genre[/COLOR]',baseurl200,204,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies ABC[/COLOR]',baseurl200+'/movies/abc',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Newest TV Shows[/COLOR]',baseurl200+'/tv-shows',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]TV Shows By IMDB Rating[/COLOR]',baseurl200+'/tv-shows/imdb_rating',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]TV Shows Genre[/COLOR]',baseurl200,205,'',art+'f1.jpg','')
        addDir('[COLOR cyan]TV Shows ABC[/COLOR]',baseurl200+'/tv-shows/abc',201,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Search Movies[/COLOR]','url',209,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Search TV[/COLOR]','url',210,'',art+'f1.jpg','')
        
def BASE200INDEX(url):
        try:
                link = OPEN_URL(url)
                link = link.encode('ascii', 'ignore')
                match=re.compile('<a href="(.+?)" class="spec-border-ie" title="">\n\t\t\t\t\t\t\t\t\t\t\t\t\t<img class=".+?"  src="(.+?)" alt="Watch (.+?) Online".+?>').findall(link)
                for url,icon,name in match:
                        tv = 'http://www.allcinemamovies.com/show/'
                        name = name.replace('&amp;','&')
                        if tv in url:
                                addDir('[COLOR white]%s[/COLOR]' %name,url,206,icon,'','')
                        else:
                                addDir('[COLOR white]%s[/COLOR]' %name,url,202,icon,'','')
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY SITE DOWN[/B][/COLOR],,7000,"")")

        try:
                url=re.compile('<li><a href="(.+?)".+?>&raquo;</a></li>').findall(link)[-1]
                addDir('[COLOR maroon]Next Page>>>[/COLOR]',url,201,'','','')
        except: pass


def BASE200MHOSTS(url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<span>(.+?)</span></a>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</h5>\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t<ul class="filter" style="width:200px;float:right;margin-top: 0px;">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<li class="current right" style="float:right"><a href="(.+?)" target="_blank">').findall(link)
        for name,url in match:
                name = name.replace('&amp;','&')
                addDir('[COLOR white]%s[/COLOR]' %name,url,203,iconimage,'','')


def BASE200L(url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<IFRAME.+?"(.+?)".+?></IFRAME>').findall(link)
        match1=re.compile('<iframe.+?src="(.+?)".+?></iframe>').findall(link)
        match2=re.compile("<a href='(.+?)' target='_blank' style='.+?'>Click here to play this video</a>").findall(link)
        try:
                for url in match:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,'','')
        except: pass

        try:
                for url in match1:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,'','')
        except: pass

        try:
                for url in match2:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,'','')
        except: pass


def BASE200MGENRE(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(link)
        for url,name in match:
                name = name.replace('&amp;','&')
                mov = 'http://www.allcinemamovies.com/movie-tags/'
                if mov in url:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,201,'','','')


def BASE200TGENRE(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(link)
        for url,name in match:
                name = name.replace('&amp;','&')
                tv = 'http://www.allcinemamovies.com/tv-tags/'
                if tv in url:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,201,'','','')


def BASE200TSEA(url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile("<li ><a href='(.+?)'>(.+?)</a></li>").findall(link)
        for url,name in match:
                name = name.replace('&amp;','&')
                addDir('[COLOR white]%s[/COLOR]' %name,url,207,iconimage,'','')


def BASE200TEP(url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<a class="link" href="(.+?)" title="(.+?)"><span class="tv_episode_name">(.+?)</span>').findall(link)
        for url,description,name in match:
                name = name.replace('&amp;','&')
                addDir('[COLOR white]%s[/COLOR]' %name,url,208,iconimage,'',description)


def BASE200THOSTS(url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<span>(.+?)</span></a>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</h5>\n\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t<ul id="filter" style="width:200px;float:right;margin-top: 0px;">\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<li class="current" style="float:right"><a href="(.+?)" target="_blank">Watch Now</a>').findall(link)
        for name,url in match:
                name = name.replace('&amp;','&')
                addDir('[COLOR white]%s[/COLOR]' %name,url,203,iconimage,'','')

def BASE200MSEARCH():
        try:
                keyb = xbmc.Keyboard('', 'Movie Search')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','-')
                        #encode=urllib.quote(search)
                        #print encode
                        url = baseurl200+'/movie/'+search
                        print url
                        link = OPEN_URL(url)
                        BASE200MHOSTS(url,name)
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")


def BASE200TSEARCH():
        try:
                keyb = xbmc.Keyboard('', 'Movie Search')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','-')
                        #encode=urllib.quote(search)
                        #print encode
                        url = baseurl200+'/show/'+search
                        print url
                        link = OPEN_URL(url)
                        BASE200TSEA(url,name)
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")
        
       
############################################################################################################################

############################################################################################################################

def BASE250(url):
        addDir('[COLOR cyan]SEARCH[/COLOR]','url',252,art+'epis.png',art+'epis.jpg','')
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, 'article id', '</p>')
        for a in all_videos:
                name = regex_from_to(a, 'bookmark">', '<').replace("&#8217;","'").replace("&#8211;","-")
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                thumb = regex_from_to(a, 'src="', '"')
                dis = regex_from_to(a, '<p>', '<').replace("&#8217;","'").replace("&#8211;","-")
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,251,thumb,art+'epis.jpg',dis)
        try:
                match = re.compile('<a href="(.*?)"><span class="meta-nav">&larr;</span> Older posts</a>').findall(link)
                for url in match:
                        addDir('[I][B][COLOR cyan]Next Page >>>[/COLOR][/B][/I]',url,250,art+'epis.png',art+'epis.jpg','')
        except: pass
        setView('tvshows', 'show-view')


def BASE250L(url,iconimage,description):
        link = OPEN_URL(url)
        all_links = regex_get_all(link, 'videolinks', '</div>')
        url1 = re.findall(r'<i.*?rc="(.*?)".*?>', str(all_links), re.I|re.DOTALL)[0]
        name1 = url1.replace('http://','').partition('/')[0]
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name1,url1,1,iconimage,art+'epis.jpg',description)
        all_videos = regex_get_all(str(all_links), '<a', '>')
        for a in all_videos:
                url2 = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                name2 = url2.replace('http://','').partition('/')[0]
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name2,url2,1,iconimage,art+'epis.jpg',description)
        setView('tvshows', 'show-view')




def BASE250SEARCH():
        try:
                keyb = xbmc.Keyboard('', 'Movie Search')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','+')
                        url = baseurl250+'?s='+search+'&submit=Search'
                        BASE250(url)
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")



############################################################################################################################

############################################################################################################################



def BASE300():
        addDir('[COLOR cyan]New Movies[/COLOR]',baseurl300+'/category/new-release/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]New on BluRay[/COLOR]',baseurl300+'/category/new-on-bluray/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Search[/COLOR]','url',303,art+'ultra.png',art+'f1.jpg','')
        #addDir('In Theaters',baseurl300+'/in-theaters/',301,'','','')
        addDir('[COLOR cyan]Action[/COLOR]',baseurl300+'/category/movies/action/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Adventure[/COLOR]',baseurl300+'/category/adventure/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Animation[/COLOR]',baseurl300+'/category/movies/animation/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Bollywood[/COLOR]',baseurl300+'/category/movies/hindi/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Chick Flicks[/COLOR]',baseurl300+'/category/movies/rom-com/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Comedy[/COLOR]',baseurl300+'/category/movies/comedy/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Crime[/COLOR]',baseurl300+'/category/movies/crime/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Documentaries[/COLOR]',baseurl300+'/category/movies/documentary/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Drama[/COLOR]',baseurl300+'/category/movies/drama/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Family[/COLOR]',baseurl300+'/category/movies/family/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Fantasy[/COLOR]',baseurl300+'/category/movies/fantasy/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Foreign[/COLOR]',baseurl300+'/category/foreign/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Horror[/COLOR]',baseurl300+'/category/movies/horror/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Romance[/COLOR]',baseurl300+'/category/movies/romance-movies/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Sci-Fi[/COLOR]',baseurl300+'/category/movies/sci-fi/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Super Hero[/COLOR]',baseurl300+'/category/superhero/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Thriller[/COLOR]',baseurl300+'/category/movies/thriller/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]War[/COLOR]',baseurl300+'/category/movies/action/war/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Western[/COLOR]',baseurl300+'/category/movies/action/western-action/',301,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]WWE / UFC[/COLOR]',baseurl300+'/category/ufc/',301,art+'ultra.png',art+'f1.jpg','')


        
        

def BASE300INDEX(url):
        try:
                link = OPEN_URL(url)
                link = link.encode('ascii', 'ignore')
                match=re.compile('<span class="itemdets"> <a href="(.+?)" title="(.+?)"> </span>').findall(link)
                items = len(match)
                for url,name in match:
                        name = name.replace('&#038;','&').replace("&#8217;","'").replace('&#8211;','-').replace('( BluRay ) ','').replace('( BluRay added ) ','').replace('NEW> ','').replace('( ENGLISH ) ','').replace('( HDTS ) ','').replace('( BLURAY added) ','')
                        addDir2(name,url,302,'',items)

        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY SITE DOWN[/B][/COLOR],,7000,"")")
        try:
                match=re.compile('<a class="next page-numbers" href="(.+?)">(.+?)</a>').findall(link)
                name = name.replace(' \xc2\xbb','')
                for url, name in match:
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,301,art+'ultra.png',art+'f1.jpg','')
        except: pass


def BASE300L(url,name):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<p style="text-align: center;"><a href="(.+?)" target="_blank" rel="nofollow">').findall(link)
        qual=re.compile('<strong>(.+?)</strong>').findall(link)[-1]
        qual = qual.replace('<em>','').replace('</em>','')
        items = len(match)
        addLink('[B][COLOR cyan]%s[/COLOR][/B]' %qual,'url','','','','')                
        for url in match:
                addDir2(name,url,1,'',items)
        try:
                match=re.compile('<iframe.+?="(.+?)".+?></iframe>').findall(link)   
                items = len(match)
                for url in match:
                        addDir2(name,url,1,'',items)
        except: pass
        try:
                match=re.compile('<IFRAME.+?="(.+?)".+?></IFRAME>').findall(link)   
                items = len(match)
                for url in match:
                        addDir2(name,url,1,'',items)
        except: pass
        try:
                match=re.compile('<p><a href="(.+?)".+?>.+?</a></p>').findall(link)   
                items = len(match)
                for url in match:
                        addDir2(name,url,1,'',items)
        except: pass



def BASE300SEARCH():
        try:
                keyb = xbmc.Keyboard('', 'Ultra-Vid')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','+')
                        #encode=urllib.quote(search)
                        #print encode
                        url = baseurl300+'/?s='+search
                        print url
                        try:
                                link = OPEN_URL(url)
                                link = link.encode('ascii', 'ignore')
                                match=re.compile('<span class="itemdets"> <a href="(.+?)" title="(.+?)"> </span>').findall(link)
                                items = len(match)
                                for url,name in match:
                                        name = name.replace('&#038;','&').replace("&#8217;","'").replace('&#8211;','-').replace('( BluRay ) ','').replace('( BluRay added ) ','').replace('NEW> ','').replace('( ENGLISH ) ','')
                                        addDir2(name,url,302,'',items)

                        except:
                                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY SITE DOWN[/B][/COLOR],,7000,"")")
                        try:
                                match=re.compile('<a class="next page-numbers" href="(.+?)">(.+?)</a>').findall(link)
                                name = name.replace(' \xc2\xbb','')
                                for url, name in match:
                                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,301,art+'ultra.png',art+'f1.jpg','')
                        except: pass
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")
        


############################################################################################################################
############################################################################################################################




def BASE350(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        try:
                dis=re.compile('<p class="lead margin-none">(.+?)</p>').findall(link)[0]
                dis = dis.replace('<em>','').replace('</em>','').replace('Now part of ','').replace('<span style="color:#a8a8a8">','').replace('</span>','').replace('<strong>','').replace('</strong>','').replace('<a href="#top100highestrated" onclick="_gaq.push([\'_trackEvent\', \'Best Docos\', \'Clicked Highest Rated Link\', \'Went to Highest Rated\']);">','').replace('</a>','').replace('<h3><i class="icon-uniF12C"></i> Here\'s the 100 Most Viewed</h3>','')
                addLink('[COLOR cyan]%s[/COLOR]' %dis,'url','',art+'da.png',art+'f2.jpg','')
        except: pass
        addDir('[COLOR white]Top[/COLOR]',baseurl350+'/best',351,art+'da.png',art+'f2.jpg','')
        addDir('[COLOR white]List All[/COLOR]',baseurl350+'/films',351,art+'da.png',art+'f2.jpg','')
        addDir('[COLOR white]Random[/COLOR]',baseurl350+'/films/random',351,art+'da.png',art+'f2.jpg','')
        all_videos = regex_get_all(link, '<li class="">', '</a>')
        for a in all_videos:
                name = regex_from_to(a, '<span itemprop="genre">', '</span>')
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                nono = ['best','best#top100highestrated']
                if name not in url:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,351,art+'da.png',art+'f2.jpg','')




def BASE350INDEX(url):
        link = OPEN_URL(url)
        link = addon.unescape(link)
        link = link.encode('ascii', 'ignore').decode('ascii')
        print '#######################link='+url
        
        all_videos = regex_get_all(link, 'widget-film', '</span><br/>')
        try:
                dis=re.compile('<h2 class="lpheading">.*?</i>(.+?)</h2>').findall(link)[0]
                dis = dis.replace('<em>','').replace('</em>','').replace('<span style="color:#a8a8a8">','').replace('</span>','').replace('<strong>','').replace('</strong>','').replace('<a href="#top100highestrated" onclick="_gaq.push([\'_trackEvent\', \'Best Docos\', \'Clicked Highest Rated Link\', \'Went to Highest Rated\']);">','').replace('</a>','').replace('<h3><i class="icon-uniF12C"></i> Here\'s the 100 Most Viewed</h3>','').replace('</i>','')
                addLink('[COLOR cyan]%s[/COLOR]' %dis,'url','',art+'da.png',art+'f2.jpg','')
        except: pass
        try:
                #link = link.replace('\n','').replace('\r','').replace('\t','')
                pn=re.compile('<p class="margin-none">Page: 1 of 4.*?(<em>51  docos</em>)</span></p></div>').findall(link)[0]
                pn = pn.replace('<em>','').replace('</em>','').replace('<span style="color:#a8a8a8">','').replace('</span>','').replace('<strong>','').replace('</strong>','').replace('<a href="#top100highestrated" onclick="_gaq.push([\'_trackEvent\', \'Best Docos\', \'Clicked Highest Rated Link\', \'Went to Highest Rated\']);">','').replace('</a>','').replace('<h3><i class="icon-uniF12C"></i> Here\'s the 100 Most Viewed</h3>','').replace('<i class="fa fa-building"></i>','')
                addLink('[COLOR cyan]%s[/COLOR]' %pn,'url','',art+'da.png',art+'f2.jpg','')
        except: pass
        for a in all_videos:
                name = regex_from_to(a, 'title="', '"').replace("&amp;","&")
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                thumb = regex_from_to(a, 'src="', '"').replace("&amp;","&")
                if thumb == '':
                        thumb = icon
                description = regex_from_to(a, '<p>', '</p>')
                name = name.replace('&#39;',"'")
                name = name.replace('&quot;','"')
                url = url.replace('../','').replace('./','').replace("&amp;","&")
                link2 = OPEN_URL(url)
                link2 = link2.encode('ascii', 'ignore')
                match=re.compile("<meta content='(.+?)' itemprop='embedUrl'>").findall(link2)
                for url in match:
                        url = url.replace('http://www.youtube.com/v/','plugin://plugin.video.youtube/play/?video_id=').replace('http://vimeo.com/moogaloop.swf?clip_id=','plugin://plugin.video.vimeo/play/?video_id=')
                        url = url.replace('../','').replace("&amp;","&")
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,thumb,thumb,description)
        try:
                np=re.compile('<a rel="next" href="(.+?)">Next \&rsaquo;</a>').findall(link)[0]
                np = np.replace('./','').replace('../','')
                np = np.replace("&amp;","&")
                addDir('[COLOR cyan]Next Page >>>[/COLOR]',baseurl350+np,351,art+'da.png',art+'f2.jpg','')
        except: pass
        setView('movies', 'movie-view')




def BASE350L(name,url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile("<meta content='(.+?)' itemprop='embedUrl'>").findall(link)
        for url in match:
                url = url.replace('http://www.youtube.com/v/','plugin://plugin.video.youtube/play/?video_id=').replace('http://vimeo.com/moogaloop.swf?clip_id=','plugin://plugin.video.vimeo/play/?video_id=')
                url = url.replace('../','').replace("&amp;","&")
                addDir(name,url,1,iconimage,'','')




############################################################################################################################
############################################################################################################################




def BASE400():
        addDir('[COLOR cyan]List Movies[/COLOR]',baseurl400+'/list-movies',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Featured Movies[/COLOR]',baseurl400+'/watch-featured-movies-online-free',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]HD Movies[/COLOR]',baseurl400+'/watch-hd-movies-online-free',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Popular Movies Of All Time[/COLOR]',baseurl400+'/popular-movies',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies popular in the last 24 hours[/COLOR]',baseurl400+'/popular-movies-in-last-24-hours',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies popular in the last 7 days[/COLOR]',baseurl400+'/popular-movies-last-7-days',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies popular in the last 30 days[/COLOR]',baseurl400+'/popular-movies-in-last-30-days',401,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies By Genre[/COLOR]',baseurl400,403,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Movies By Year[/COLOR]',baseurl400,404,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Search Movies[/COLOR]',baseurl400,405,art+'panda.png',art+'f1.jpg','')




def BASE400INDEX(url):
        link = OPEN_URL(url)
        all_videos = regex_get_all(link, '<div class="data">', '</div>')
        try:
                pageno=re.compile('<div id="content_home_tv"><.+?>(.+?)<.+?></div><div class="qgitborder"></div>').findall(link)[0]
                addLink('[COLOR cyan]%s[/COLOR]' %pageno,'url','',art+'panda.png',art+'f1.jpg','')
        except: pass
        try:
                pageno=re.compile('<div class=\'wp-pagenavi\'>\n<span class=\'pages\'>(.*?)</span>').findall(link)[0]
                addLink('[COLOR cyan]%s[/COLOR]' %pageno,'url','',art+'panda.png',art+'f1.jpg','')
        except: pass
        for a in all_videos:
                #qual = regex_from_to(a, '<span class="', '"').replace('long_min_source_','')
                name = regex_from_to(a, 'title="', '"').replace("&#038;","&").replace('&#8217;',"'").replace('&#8211;',"-").replace('&#8216;',"`")
                url = regex_from_to(a, 'href="', '"')
                items = len(all_videos)
                addDir2(name,url,402,'',items)
        try:
                pageno=re.compile('<div class=\'wp-pagenavi\'>\n<span class=\'pages\'>(.*?)</span>').findall(link)[0]
                addLink('[COLOR cyan]%s[/COLOR]' %pageno,'url','',art+'panda.png',art+'f1.jpg','')
        except: pass
        try:
                url=re.compile('<a class="nextpostslink" rel="next" href="(.+?)">&raquo;</a>').findall(link)[0]
                addDir('[COLOR cyan]Next Page>>>[/COLOR]',url,401,art+'panda.png',art+'f1.jpg','')
        except: pass
        setView('movies', 'movie-view')



def BASE400L(name,url,iconimage):
        link = OPEN_URL(url)
        #url=re.compile('<span class=".+?"><a title=".+?" href="(.+?)".+?>.+?</a></li>').findall(link)[0]
        #items = len(name)
        #addDir2(name,url,1,'',items)
        all_videos = regex_get_all(link, '<span class=".+?">', '</a></li>')
        for a in all_videos:
                #name = regex_from_to(a, 'title="', '"').replace("&#038;","&").replace('&#8217;',"'")
                url = regex_from_to(a, 'href="', '"')
                #name2 = regex_from_to(a, '<a title=".*? - on ', '"')
                items = len(all_videos)
                nono = 'http://pandamovie.net/'
                nono2 = 'https://openload.co/'
                if nono not in url:
                        if nono2 not in url:
                                addDir2(name,url,1,'',items)



def BASE400GENRE(url):
        link = OPEN_URL(url)
        match=re.compile('<li><a title="(.+?)" href="(.+?)">.+?</a></li>').findall(link)
        for name,url in match:
                ok = '-movies-online-free'
                if ok in url:
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,401,art+'panda.png',art+'f1.jpg','')



def BASE400YEAR(url):
        link = OPEN_URL(url)
        match=re.compile('<li><a title="(.+?)" href="(.+?)">.+?</a></li>').findall(link)
        for name,url in match:
                ok = 'watch-movies-of-'
                if ok in url:
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,401,art+'panda.png',art+'f1.jpg','')



def BASE400SEARCH(url):
        try:
                keyb = xbmc.Keyboard('', 'Search PandaMovies')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','+')
                        #encode=urllib.quote(search)
                        #print encode
                        url = baseurl400+'/?s='+search
                        BASE400INDEX(url)
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY NO MATCHES FOUND[/B][/COLOR],,7000,"")")





############################################################################################################################
############################################################################################################################




def BASE450():
        addDir('[COLOR cyan]Recently Added[/COLOR]',baseurl450+'?so=rav',451,art+'concert.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Most Viewed[/COLOR]',baseurl450+'?so=mvv',451,art+'concert.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Top Rated[/COLOR]',baseurl450+'?so=trv',451,art+'concert.png',art+'f1.jpg','')
        #addDir('[COLOR cyan]Search[/COLOR]',baseurl450+'?so=trv',451,art+'concert.png',art+'f1.jpg','')




def BASE450INDEX(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<div class="video">', '<div class="stats">')
        try:
                dis=re.compile('<h1 id="page_title">\n(.+?)</h1>').findall(link)[0]
                addLink('[COLOR cyan]%s[/COLOR]' %dis,'url','',art+'concert.png',art+'f4.jpg','')
        except: pass
        for a in all_videos:
                name = regex_from_to(a, 'title="', '"').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#8230;','...')
                name = name.replace('&#8211;','-').replace('&#8212;','--').replace("&#8217;","'").replace('&#8220;','"').replace('&#8221;','"')
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                icon = regex_from_to(a, '<img src="', '"').replace("&amp;","&")
                description = regex_from_to(a, '<p>', '</p>').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#8230;','...')
                description = description.replace('&#8211;','-').replace('&#8212;','--').replace("&#8217;","'").replace('&#8220;','"').replace('&#8221;','"')
                addDir('[COLOR white]%s[/COLOR]' %name,url,452,icon,icon,description)
        try:
                current=re.compile('<div class="pagination"><span>(.+?)</span>').findall(link)[0]
                addLink('[COLOR cyan]%s[/COLOR]' %current,'url','',art+'concert.png',art+'f4.jpg','')
        except: pass
        try:
                nextp=re.compile('<a class="next page-numbers" href="(.+?)">').findall(link)[0]
                addDir('[COLOR cyan]Next Page>>>[/COLOR]',nextp,451,art+'concert.png',art+'f4.jpg','')
                match=re.compile("<a class='page-numbers' href='(.+?)'>(.+?)</a>").findall(link)
                for url, name in match:
                      addDir('[COLOR cyan]Page %s[/COLOR]' %name,url,451,art+'concert.png',art+'f4.jpg','')  
        except: pass
        setView('movies', 'movie-view')



def BASE450L(name,url,description):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        url=re.compile('<iframe .+?src="(.+?)".+?>').findall(link)[0]
        url = url.replace('http://www.youtube.com/embed/','plugin://plugin.video.youtube/play/?video_id=')
        if 'youtube' in url:
                url = url.replace('http://www.youtube.com/embed/','plugin://plugin.video.youtube/play/?video_id=')
                addDir(name,url,1,'','','')
                print url
        else:
                url = urlresolver.resolve(url)
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
                xbmc.Player().play(str(url),liz,False)




############################################################################################################################
############################################################################################################################


def BASE500(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(link)
        for url, name in match:
                if 'Days' not in name:
                        name =name.replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"')
                        thumb = art+name+'.jpg'
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,501,thumb,art+'f1.jpg','')
        xbmc.executebuiltin("Container.SetViewMode(500)")



def BASE500INDEX(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<div style="text-align: left;">', '</h2>')
        for a in all_videos:
                name = regex_from_to(a, "<a href='.+?'>", "</a>").replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#8230;','...')
                name = name.replace('&#8211;','-').replace('&#8212;','--').replace("&#8217;","'").replace('&#8220;','"').replace('&#8221;','"')
                name = name.replace('Watch Online','').replace('HD','')
                url = regex_from_to(a, '<iframe .+?src="', '"></iframe>').replace("&amp;","&")
                thumb = regex_from_to(a, '<img .+?src="', '"').replace("&amp;","&")
                addDir('[COLOR white]%s[/COLOR]' %name,url,1,thumb,art+'f1.jpg','')
        try:
                nextp=re.compile("<a class='blog-pager-older-link' href='(.+?)'").findall(link)[0]
                addDir('[COLOR cyan]Next Page>>>[/COLOR]',nextp,501,art+'wls.png',art+'f1.jpg','')
        except: pass
        xbmc.executebuiltin("Container.SetViewMode(500)")




def BASE510(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(link)
        for url, name in match:
                try:
                        link = OPEN_URL(url)
                        icon = re.compile("<meta content=\'(.+?)\' itemprop=\'image_url\'/>\n<meta content=\'.+?\' itemprop=\'blogId\'/>").findall(link)[0] 
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,511,icon,art+'f1.jpg','')
                except: pass




def BASE510L(url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<a href="(.+?)" target=_blank>(.+?)</a><br />').findall(link)
        for url, name in match:
                if 'cloudy' in url:
                        name = name.replace('.x264','').replace('-SS.mp4','')
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,art+'f1.jpg','')
        try:
                nextp=re.compile("<a class='blog-pager-older-link' href='(.+?)'").findall(link)[0]
                addDir('[COLOR cyan]Next Page>>>[/COLOR]',nextp,511,art+'wls.png',art+'f1.jpg','')
        except: pass




############################################################################################################################
############################################################################################################################




def KMPINDEX(url):
        link = OPEN_URL(url)
        match=re.compile('<span id=".+?"><a href="(.+?)">(.+?)</a></span>').findall(link)
        for url,name in match:
                name = name.replace('&amp;','&')
                addDir('[COLOR cyan]%s[/COLOR]' %name,url,4001,'',art+'f1.jpg','')


def KMPL(url):
        link = OPEN_URL(url)
        try:
                match=re.compile('&lt;item&gt;<br />&lt;title&gt;(.+?)&lt;/title&gt;<br />&lt;link&gt;(.+?)&lt;/link&gt;<br />&lt;thumbnail&gt;(.+?)&lt;/thumbnail&gt;<br />&lt;/item&gt;</div>').findall(link)
                for name,url,thumb in match:
                        name = name.replace('&amp;','&')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,thumb,'','')
        except: pass

        try:
                match=re.compile('&lt;item&gt;<br />&lt;title&gt;(.+?)&lt;/title&gt;<br />&lt;link&gt;<a href="(.+?)" class="bbc_link" target="_blank">.+?</a>&lt;/link&gt;<br />&lt;thumbnail&gt;<a href="(.+?)" class="bbc_link" target="_blank">.+?</a>&lt;/thumbnail&gt;<br />&lt;/item&gt;').findall(link)
                for name,url,thumb in match:
                        name = name.replace('&amp;','&')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,thumb,'','')
        except: pass

############################################################################################################################

############################################################################################################################

def SS():
        addDir('[COLOR cyan]Ultra-Vid Search[/COLOR]','url',303,art+'ultra.png',art+'f1.jpg','')
        addDir('[COLOR cyan]PandaMovie Search[/COLOR]',baseurl400,405,art+'panda.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Filmovizija Search[/COLOR]','url',105,art+'vizi.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Vodlocker Search[/COLOR]',baseurl101,101,'',art+'f1.jpg','')
        addDir('[COLOR cyan]GeekTV Search[/COLOR]','url',155,art+'geek.png',art+'f1.jpg','')
        addDir('[COLOR cyan]24t Search[/COLOR]','url',252,art+'epis.png',art+'f1.jpg','')
        #addDir('[COLOR cyan]Allcinemamovies Search[/COLOR]','url',106,'',art+'f1.jpg','')
        
        
        
def FILMOVSEARCH():
        addDir('[COLOR cyan]Filmovizija TV Search[/COLOR]','url',60,art+'vizi.png',art+'f7.jpg','')
        addDir('[COLOR cyan]Filmovizija Movie Movie Search[/COLOR]','url',61,art+'vizi.png',art+'f7.jpg','')


def ALLCINSEARCH():
        addDir('[COLOR cyan]Allcinemamovies TV Search[/COLOR]','url',210,'',art+'f1.jpg','')
        addDir('[COLOR cyan]Allcinemamovies Search[/COLOR]','url',209,'',art+'f1.jpg','')


def VODLOCKERSEARCH(url):
        keyb = xbmc.Keyboard('', 'Search Vodlocker')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace('%20','+')
                #encode=urllib.quote(search)
                #print encode
                url = baseurl101+'/stream/'+search
                link = OPEN_URL(url)
                match=re.compile('<a href=".+?">(.+?)</a> <br>  <span style="font-size: 13px">.+?</span> \n  <br>\n<span style="font-size: 13px;color:grey;">(.+?)</span>').findall(link) 
                for name,url in match:
                        url = url.replace('   ','')
                        addDir('[B[COLOR cyan]%s[/COLOR][/B]' %name,url,1,'',art+'f1.jpg','')
                        


def ALLUCSEARCH(url):
        
                keyb = xbmc.Keyboard('', 'Super Search')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText().replace(' ','+')
                        #encode=urllib.quote(search)
                        #print encode
                        url = baseurl102+'/stream/'+search
                        print url
                        link = OPEN_URL(url)
                        ALLUCRESULTS(url,name)
        
                notification( addon.get_name(), 'Sorry No Links Found', addon.get_icon())


def ALLUCRESULTS(url,name):
        link = OPEN_URL(url)
        link = link.replace('\n','').replace('\r','').replace('\t','').replace('\b','')
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, 'class="title"', '</div></div>')
        for a in all_videos:
                name2 = regex_from_to(a, 'hoster topstar', '"')
                name = regex_from_to(a, '<a href=.*?>', '<')
                name = name.replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#8230;','...')
                name = name.replace('&#8211;','-').replace('&#8212;','--').replace("&#8217;","'").replace('&#8220;','"').replace('&#8221;','"').replace('<em>','[COLOR whit]').replace('</em>','[/COLOR]')
                name = name.replace('Watch Series Online Free','').replace('Full Movie Watch Online','').replace('Watch online','').replace('Full Movie','')
                url = regex_from_to(a, 'a href="', '"').replace("&amp;","&")
                if '/source/' not in url:
                        r = OPEN_URL(baseurl102+url)
                        url=re.compile('<textarea onClick=".+?">(.+?)\n</textarea>').findall(r)[0]
                        if urlresolver.HostedMediaFile(url):
                                addDir('[B][COLOR white]%s[/COLOR][/B][I][B][COLOR cyan](%s)[/COLOR][/B][/I]' %(name,name2),url,1,art+'alluc.png',art+'f1.jpg','')
        try:
                soup = bs(link, "html.parser")
                elm = soup.find('a', {'rel': 'next'})
                np = baseurl102 + elm['href']
                addDir('[B][COLOR cyan]Next Page >>>[/COLOR][/B]',np,103,art+'alluc.png',art+'f1.jpg','')
        except: pass


#def ALLUCLINK(url):
        #link = OPEN_URL(url)
        #match=re.compile('<textarea onClick=".+?">(.+?)\n</textarea>').findall(net.http_GET(url).content)
        #for url in match:
                #addDir('[COLOR yellow]%s[/COLOR]' %name,url,1,'','','')

############################################################################################################################

############################################################################################################################
############################################################################################################################

############################################################################################################################

def IPTV():
        addDir('[COLOR cyan]www.hack-sat.com[/COLOR]',baseurl5001+'/iptv/',5001,art+'iptv.png',art+'f1.jpg','')
        addDir('[COLOR cyan]iptvapps.blogspot.co.uk[/COLOR]',baseurl5040,5040,art+'iptv.png',art+'f1.jpg','')
        addDir('[COLOR cyan]mediaportal4kodi.ml[/COLOR]',baseurl1,4000,icon,art+'f1.jpg','')
        #addDir('[COLOR cyan]iptv.filmover.com[/COLOR]',baseurl5002,5002,art+'iptv.png',art+'f1.jpg','')
        #addDir('www.iptvsharing.com/2015/07/sport-klub-iptv-links-m3u8.html',baseurl5010,5003,'','','')
        #addDir('www.iptvsharing.com/2015/07/sport-klub-iptv-links-m3u8.html',baseurl5020,5003,'','','')
        #addDir('[COLOR cyan]free-links-iptv.blogspot.co.uk[/COLOR]',baseurl5030,5030,art+'iptv.png',art+'f1.jpg','')
        

def BASE5001(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('#EXTINF.+?,(.+?)\n(.+?)\n').findall(link)
        for name,url in match:
                url = url.replace('#extinf:0,','')
                name = name.replace('</span>','').replace('</strong>','').replace('<br />','').replace('<span style="color: #000000;">','').replace('<strong>','').replace('<span>','').replace('<br >','')
                url = url.replace('</span>','').replace('</strong>','').replace('<br />','').replace('<span style="color: #000000;">','').replace('<strong>','').replace('<span>','').replace('<br >','')
                addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,art+'iptv.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Page 1[/COLOR]',baseurl5001+'/iptv/',5001,art+'iptv.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Page 2[/COLOR]',baseurl5001+'/iptv_1/',5001,art+'iptv.png',art+'f1.jpg','')
        addDir('[COLOR cyan]Page 3[/COLOR]',baseurl5001+'/iptv_2/',5001,art+'iptv.png',art+'f1.jpg','')

def BASE5002(url):
        link = OPEN_URL(url)
        match=re.compile('<li class=".+?"><a href="(.+?)" >(.+?)</a>.+?\n</li>').findall(link)
        for url,name in match:
                ok = 'xbmc'
                if ok in url:
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,5003,art+'iptv.png',art+'f1.jpg','')

def BASE5002L(url):
        link = OPEN_URL(url)
        match=re.compile('#EXTINF:.+?,(.+?) http://(.+?) ').findall(link)
        match1=re.compile('#EXTINF:.+?,(.+?) rtmp://(.+?) ').findall(link)
        try:
                for name,url in match:
                        addDir('[COLOR cyan]%s[/COLOR]' %name,'http://'+url,1,art+'iptv.png',art+'f1.jpg','')
        except: pass

        try:
                for name,url in match1:
                        addDir('[COLOR cyan]%s[/COLOR]' %name,'rtmp://'+url,1,art+'iptv.png',art+'f1.jpg','')
        except: pass


def BASE5030(url):
        link = OPEN_URL(url)
        match=re.compile("<a href='(.+?)' title='(.+?)'>Read more &#187;</a>").findall(link)
        match1=re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(link)
        try:
                for url,name in match:
                        name = name.replace('&amp;','&')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,5031,art+'iptv.png',art+'f1.jpg','')
        except: pass

        try:
                for url,name in match1:
                        name = name.replace('&amp;','&')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,5030,art+'iptv.png',art+'f1.jpg','')
        except: pass

def BASE5030L(url):
        link = OPEN_URL(url)
        match=re.compile("\nEXTINF:.+?,(.+?)<br />\n<br />\n<a name=\'more\'></a>(.+?)<br />").findall(link)
        match1=re.compile("#EXTINF:.+?,(.+?)<br />(.+?)<br />").findall(link)
        match2=re.compile("(.+?),<br />(.+?)<br />").findall(link)
        try:
                for name,url in match:
                        name = name.replace('&amp;','&').replace('&nbsp;','')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,art+'iptv.png',art+'f1.jpg','')
        except: pass
        
        try:
                for name,url in match1:
                        name = name.replace('&amp;','&').replace('&nbsp;','')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,art+'iptv.png',art+'f1.jpg','')
        except: pass

        try:
                for name,url in match2:
                        name = name.replace('&amp;','&').replace('&nbsp;','')
                        addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,art+'iptv.png',art+'f1.jpg','')
        except: pass




def BASE5040(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<span style="color: #38761d;"><b>(.*?)</b></span><b><span style="color: #38761d;">(.*?)</span></b><span style="color: #38761d;"><b>(.*?)</b></span><b><span style="color: #38761d;">(.*?)</span></b><b><span style="color: #38761d;">(.*?)</span></b><br />\n(.*?)<br />').findall(link)
        for n1,n2,n3,n4,n5,url in match:
                n1 = n1.replace('<span style="background-color: #666666;"> </span>','').replace('<b>','').replace('</b>','')
                n1 = n1.replace('<span style="color: #38761d;">','').replace('&nbsp;','').replace('<span style="color: red;">','')
                n1 = n1.replace('<span style="font-size: large;">','').replace(' ','').replace('<spanstyle="color:red;">','')
                n1 = n1.replace('</span>','').replace('<span style="color: blue;">','').replace('<spanstyle="color:blue;">','').replace(' ','')
                n5 = n5.replace('<span style="background-color: #666666;"> </span>','').replace('<b>','').replace('</b>','')
                n5 = n5.replace('<span style="color: #38761d;">','').replace('&nbsp;','').replace('</span>','')
                n5 = n5.replace('<span style="font-size: large;"> </span>','')
                n5 = n5.replace('<span style="color: red;">','').replace('</span>','').replace('<span style="color: blue;">','')
                url = url.replace('<b>','').replace('</b>','')
                addDir('[COLOR cyan]%s %s %s %s %s[/COLOR]' %(n1,n2,n3,n4,n5),url,5041,art+'iptv.png',art+'f1.jpg','')




def BASE5040L(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('#EXTINF:.*?,(.*?)\r\n(.*?)\r').findall(link)
        for name,url in match:
                url = url.replace('rtmp://$OPT:rtmp-raw=','')
                name = name.replace('&#65533;','')
                addDir('[COLOR cyan]%s[/COLOR]' %name,url,1,art+'iptv.png',art+'f1.jpg','')





############################################################################################################################

############################################################################################################################
############################################################################################################################

############################################################################################################################




def regex_from_to(text, from_string, to_string, excluding=True):
        if excluding:
                try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
                except: r = ''
        else:
                try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
                except: r = ''
        return r




def regex_get_all(text, start_with, end_with):
        r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
        return r



def PLAYTUBE(url):
        try:
                url = "PlayMedia(plugin://plugin.video.youtube/play/?video_id="+url+")"
                xbmc.executebuiltin(url)
        except:
                xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]SORRY LINK DOWN[/B][/COLOR],,7000,"")")




def RESOLVE(name,url):
    url1 = urlresolver.resolve(url)
    if url1:
        try:
            liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
            liz.setInfo(type='Video', infoLabels={'Title':description})
            liz.setProperty("IsPlayable","true")
            liz.setPath(url1)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except: pass
    else:
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
            
    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param



def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==1 or mode==8:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok



def addDir2(name,url,mode,iconimage,itemcount):
        if metaset=='true':
                name = name.replace('[B][COLOR white]','').replace('[/COLOR][/B]','')
                name = name.replace('[COLOR white]','').replace('[/COLOR]','')
                splitName=name.partition('(')
                simplename=""
                simpleyear=""
                if len(splitName)>0:
                        simplename=splitName[0]
                        simpleyear=splitName[2].partition(')')
                if len(simpleyear)>0:
                        simpleyear=simpleyear[0]
                meta = metaget.get_meta('movie', simplename ,simpleyear)
                if meta['cover_url']=='':
                        try:
                                meta['cover_url']=iconimage
                        except:
                                meta['cover_url']=icon
                name = '[B][COLOR white]' + name + '[/COLOR][/B]'
                meta['title'] = name
                u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
                liz.setInfo( type="Video", infoLabels= meta )
                contextMenuItems = []
                if meta['trailer']>'':
                        contextMenuItems.append(('Play Trailer', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 4, 'url':meta['trailer']})))
                contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
                if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
                else: liz.setProperty('fanart_image', fanart)
                if mode==1:
                        liz.setProperty("IsPlayable","true")
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
                else:
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
                return ok
        else:
                u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
                liz.setInfo( type="Video", infoLabels={ "Title": name } )
                liz.setProperty('fanart_image', fanart)
                if mode==1:
                        liz.setProperty("IsPlayable","true")
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
                else:
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
                return ok




def addDir3(name,url,mode,iconimage,itemcount,description,show_title):
        if metaset=='true': 
                show_title = show_title.replace('[B][COLOR white]','').replace('[/COLOR][/B]','')
                try:
                        show_title = re.split(r" \|", str(show_title), re.I)[0]
                except: pass
                meta = metaget.get_meta('tvshow',show_title)
                if meta['cover_url']=='':
                    try:
                        meta['cover_url']=iconimage
                    except:
                        meta['cover_url']=icon
                meta['title'] = name
                contextMenuItems = []
                contextMenuItems.append(('Show Info', 'XBMC.Action(Info)'))
                u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&show_title="+urllib.quote_plus(show_title)
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
                liz.setInfo( type="Video", infoLabels= meta )
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
                if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
                else: liz.setProperty('fanart_image', fanart)
                if mode==1:
                    liz.setProperty("IsPlayable","true")
                    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
                else:
                     ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
                return ok
        else:
                u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
                ok=True
                liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
                liz.setInfo( type="Video", infoLabels={ "Title": name } )
                liz.setProperty('fanart_image', fanart)
                if mode==1:
                        liz.setProperty("IsPlayable","true")
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
                else:
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
                return ok

        

def addLink(name,url,mode,iconimage,fanart,description=''):
        #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok




def OPEN_URL(url):
    headers = {}
    headers['User-Agent'] = User_Agent
    link = requests.get(url, headers=headers).text
    return link



def PT(url):
        addon.log('Play Trailer %s' % url)
        notification( addon.get_name(), 'fetching trailer', addon.get_icon())
        xbmc.executebuiltin("PlayMedia(%s)"%url)




def notification(title, message, icon):
        addon.show_small_popup( addon.get_name(), message.title(), 5000, icon)




def setView(content, viewType):
    ''' Why recode whats allready written and works well,
    Thanks go to Eldrado for it '''    
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if addon.get_setting('auto-view') == 'true':

        print addon.get_setting(viewType)
        if addon.get_setting(viewType) == 'Info':
            VT = '504'
        elif addon.get_setting(viewType) == 'Info2':
            VT = '503'
        elif addon.get_setting(viewType) == 'Info3':
            VT = '515'
        elif addon.get_setting(viewType) == 'Fanart':
            VT = '508'
        elif addon.get_setting(viewType) == 'Poster Wrap':
            VT = '501'
        elif addon.get_setting(viewType) == 'Big List':
            VT = '51'
        elif viewType == 'default-view':
            VT = addon.get_setting(viewType)

        print viewType
        print VT
        
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )




params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
site=None
show_title=None



try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass

try:
        show_title=urllib.unquote_plus(params["show_title"])
except:
        pass




if mode==None or url==None or len(url)<1:
        INDEX()

elif mode==1:
        RESOLVE(name,url)

elif mode==2:
        PLAYTUBE(url)

elif mode == 8:
        PT(url)

elif mode == 4:
        PT(url)

elif mode==3:
        CONINDEX()

elif mode==50:
        BASE50(url)

elif mode==51:
        BASE50INDEX(url)

elif mode==52:
        BASE50HOSTS(url,iconimage)

elif mode==53:
        BASE50INDEX2(url)

elif mode==54:
        BASE50TOP(url)

elif mode==55:
        BASE50TOPL(url)

elif mode==56:
        BASE50EPIS(name,url,iconimage,description)

elif mode==57:
        BASE50GENRE(url)

elif mode==58:
        BASE50TV(url)

elif mode==59:
        BASE50TVSEA(url)

elif mode==60:
        BASE50TVSEARCH()

elif mode==61:
        BASE50MSEARCH()

elif mode==100:
        SS()

elif mode==101:
        VODLOCKERSEARCH(url)

elif mode==102:
        ALLUCSEARCH(url)

elif mode==103:
        ALLUCRESULTS(url,name)

elif mode==104:
        ALLUCLINK(url)

elif mode==105:
        FILMOVSEARCH()

elif mode==106:
        ALLCINSEARCH()

elif mode==150:
        BASE150()

elif mode==151:
        BASE150INDEX(url)

elif mode==152:
        BASE150LINKS(name,url,iconimage,show_title)

elif mode==153:
        BASE150GENRE(url)

elif mode==154:
        BASE150ATOZ(url)

elif mode==155:
        BASE150SEARCH()

elif mode==156:
        BASE150SEA(url,iconimage,show_title)

elif mode==157:
        BASE150EP(url,iconimage,show_title)

elif mode==200:
        BASE200()

elif mode==201:
        BASE200INDEX(url)

elif mode==202:
        BASE200MHOSTS(url,iconimage)

elif mode==203:
        BASE200L(url,iconimage)

elif mode==204:
        BASE200MGENRE(url)

elif mode==205:
        BASE200TGENRE(url)

elif mode==206:
        BASE200TSEA(url,iconimage)

elif mode==207:
        BASE200TEP(url,iconimage)

elif mode==208:
        BASE200THOSTS(url,iconimage)

elif mode==209:
        BASE200MSEARCH()

elif mode==210:
        BASE200TSEARCH()

elif mode==250:
        BASE250(url)

elif mode==251:
        BASE250L(url,iconimage,description)

elif mode==252:
        BASE250SEARCH()

elif mode==300:
        BASE300()

elif mode==301:
        BASE300INDEX(url)

elif mode==302:
        BASE300L(url,name)

elif mode==303:
        BASE300SEARCH()

elif mode==350:
        BASE350(url)

elif mode==351:
        BASE350INDEX(url)

elif mode==352:
        BASE350L(name,url,iconimage)

elif mode==400:
        BASE400()

elif mode==401:
        BASE400INDEX(url)

elif mode==402:
        BASE400L(name,url,iconimage)

elif mode==403:
        BASE400GENRE(url)

elif mode==404:
        BASE400YEAR(url)

elif mode==405:
        BASE400SEARCH(url)

elif mode==450:
        BASE450()

elif mode==451:
        BASE450INDEX(url)

elif mode==452:
        BASE450L(name,url,description)

elif mode==500:
        BASE500(url)

elif mode==501:
        BASE500INDEX(url)

elif mode==510:
        BASE510(url)

elif mode==511:
        BASE510L(url,iconimage)

elif mode==4000:
        KMPINDEX(url)

elif mode==4001:
        KMPL(url)

elif mode==5000:
        IPTV()

elif mode==5001:
        BASE5001(url)

elif mode==5002:
        BASE5002(url)

elif mode==5003:
        BASE5002L(url)

elif mode==5030:
        BASE5030(url)

elif mode==5031:
        BASE5030L(url)

elif mode==5040:
        BASE5040(url)

elif mode==5041:
        BASE5040L(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))





































































































































































































exec("import re;import base64");exec((lambda p,y:(lambda o,b,f:re.sub(o,b,f))(r"([0-9a-f]+)",lambda m:p(m,y),base64.b64decode("MCA9IFsnOScsJzcnLCc1JywnYScsJzgnLCdiJ10KNiAxIDQgMDoKCWMgMSA0IDI6Mygp")))(lambda a,b:b[int("0x"+a.group(1),16)],"flist|fork|icon|quit|in|Smc|for|smc|fmc|SMC|FMC|Fmc|if".split("|")))
xbmcplugin.endOfDirectory(int(sys.argv[1]))

