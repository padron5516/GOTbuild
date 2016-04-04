import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

import json


ADDON = xbmcaddon.Addon(id='plugin.video.cartoonhdtwo')
art= "%s/art/"%ADDON.getAddonInfo("path")

DATAKEY='M2FiYWFkMjE2NDYzYjc0MQ=='
FILMKEY = 'MmIyYTNkNTNkYzdiZjQyNw=='

API='http://gearscenter.com/gold-server/gapiandroid205/?'


if ADDON.getSetting('kidmode')=='true':
    KID ='1'
else:
    KID ='0'

    
def GetStream(url,key):
    from lib import pyaes as pyaes
    import base64

    key = base64.b64decode(key)
    decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(key))
    url = base64.decodestring(url)
    url = decrypter.feed(url) + decrypter.feed()
    return str(url)


def CATEGORIES():
    addDir('Search','search',8,art+'search.png','')            
    addDir('Movies','movies',1,'','')
    addDir('Tv Shows','tvshow',1,'','')
    addDir('Collections','list',5,'','')
    setView('movies', 'default')       
       
                                                                      
def GetContent(url):
    PAGE= 1

    new_url = API+'option=category&type=%s&total=0&sort=4&filter=-1&block=%s' % (url,KID)+str(extra())+'&page='
    link = json.loads(OPEN_URL(new_url+str(PAGE)))
   
    data=json.loads(GetStream(link['data'],DATAKEY))
    
    for field in data['categories']:
        name=field['catalog_name'].encode('utf8')
        url=str(field['catalog_id'])
        iconimage=field['catalog_icon']
        addDir(name,url,3,iconimage,'')
        
    addDir('[COLOR blue][B]Next Page >>[/B][/COLOR]',new_url,2,art+'nextpage.png','1')
    setView('movies', 'movies')

def extra():
    import random
    import time
    import hashlib
    ANDROID_LEVELS = {'22': '5.1', '21': '5.0', '19': '4.4.4', '18': '4.3.0', '17': '4.2.0', '16': '4.1.0', '15': '4.0.4', '14': '4.0.2', '13': '3.2.0'}
    COUNTRIES = ['US', 'GB', 'CA', 'DK', 'MX', 'ES', 'JP', 'CN', 'DE', 'GR']
    EXTRA_URL = ('&os=android&version=2.0.5&versioncode=205&param_1=F2EF57A9374977FD431ECAED984BA7A2&'
         'deviceid=%s&param_3=7326c76a03066b39e2a0b1dc235c351c&param_4=%s'
         '&param_5=%s&token=%s&time=%s&devicename=Google-Nexus-%s-%s')

    now = str(int(time.time()))
    build = random.choice(ANDROID_LEVELS.keys())
    device_id = hashlib.md5(str(random.randint(0, sys.maxint))).hexdigest()
    country = random.choice(COUNTRIES)
    return EXTRA_URL % (device_id, country, country.lower(), hashlib.md5(now).hexdigest(), now, build, ANDROID_LEVELS[build])




def SEARCHPLAYBOX(url):
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search Cartoon HD Extra')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText() .replace(' ','+')    
    new_url = API+'option=search&page=1&total=0&block=0&q=%s' % search_entered +extra()
    
    link = json.loads(OPEN_URL(new_url))
   
    data=json.loads(GetStream(link['data'],DATAKEY))
    
    for field in data['categories']:
        name=field['catalog_name'].encode('utf8')
        url=str(field['catalog_id'])
        iconimage=field['catalog_icon']
        addDir(name,url,3,iconimage,'')

    setView('movies', 'movies')


def TodayList(url):

    new_url = 'http://gearscenter.com/gold-server/gapiandroid205/?option=getbox'+ extra()

    link = json.loads(OPEN_URL(new_url))
   
    data=json.loads(GetStream(link['data'],DATAKEY))
    
    for field in data['box']:
        name=field['name_box'].encode('utf8')
        url=str(field['id_box'])
        iconimage=field['image_box']
        addDir(name,url,6,iconimage,'')
        
    setView('movies', 'movies')

def TodayListGetContent(url):
    PAGE= 1

    new_url = API+'option=contentbox&id_box=%s&total=0&sort=4&filter=-1&block=%s' % (url,KID)+str(extra())+'&page='
    link = json.loads(OPEN_URL(new_url+str(PAGE)))
   
    data=json.loads(GetStream(link['data'],DATAKEY))
    
    for field in data['categories']:
        name=field['catalog_name'].encode('utf8')
        url=str(field['catalog_id'])
        iconimage=field['catalog_icon']
        addDir(name,url,3,iconimage,'')
        
    addDir('[COLOR blue][B]Next Page >>[/B][/COLOR]',new_url,2,art+'nextpage.png','1')
    setView('movies', 'movies')
    

def GetNextPageContent(url,iconimage,page):
   
    PAGE=int(page)+1
    new_url = url+str(PAGE)

    try:link = json.loads(OPEN_URL(new_url))
    except:return PlayBoxFucker()   
    data=json.loads(GetStream(link['data'],DATAKEY))
    
    for field in data['categories']:
        name=field['catalog_name'].encode('utf8')
        url=str(field['catalog_id'])
        iconimage=field['catalog_icon']
        addDir(name,url,3,iconimage,'')
        
    addDir('[COLOR blue][B]Next Page >>[/B][/COLOR]',new_url,2,art+'nextpage.png',str(PAGE))     
    setView('movies', 'movies')
    
def PlayBoxFucker():
    d = xbmcgui.Dialog()
    d.ok('Playbox HD', 'No Response From Cartoon HD Server')

    
 


def OPEN_URL(url):
    import utils
    return utils.GetHTML(url)


def GetDetail(name,url,iconimage):
    
    NAME=name
    CATID=url
    
    new_url = API+'option=content&id=%s' % url +str(extra())

    try:link = json.loads(OPEN_URL(new_url))
    except:return PlayBoxFucker()
 
    data=json.loads(GetStream(link['data'],DATAKEY))
 
    data=data['listvideos']

    if len(data)>1: 
        for field in data:
            name=field['film_name'].encode('utf8')
            ID=str(field['film_id'])
            url = API+'option=filmcontent&id=%s&cataid=%s' % (ID,CATID) +str(extra())
            addDir(name.replace('E0','E'),url,4,iconimage,NAME + ' '+name.replace('E0','E'))
    else:
        for field in data:
            ID=str(field['film_id'])
            continue
        
            
        new_url = API+'option=filmcontent&id=%s&cataid=%s' % (ID,CATID) +str(extra())
       
        try:link = json.loads(OPEN_URL(new_url))
        except:return PlayBoxFucker()

        data=json.loads(GetStream(link['data'],DATAKEY))
        data=data['videos']
        for field in data:
            FILM = field['film_link']
            
            DATA=GetStream(FILM,FILMKEY)
            match=re.compile('(.+?)#(.+?)#').findall(DATA)               
            for url , name in match:
 
                name='GOOGLEVIDEO '+name+'p'
                if ('720' in name) or ('1080' in name):
                    name=name.replace('720p','[COLOR green]720P[/COLOR]').replace('1080p','[COLOR green]1080P[/COLOR]')         
                addDir(name,url,200,iconimage,str(NAME))

   
def GetStreamLinks(url,iconimage,name,page):
    
    NAME=page
    try:link = json.loads(OPEN_URL(url))
    except:return PlayBoxFucker()

    data=json.loads(GetStream(link['data'],DATAKEY))
    data=data['videos']
    for field in data:
        FILM = field['film_link']
        
        DATA=GetStream(FILM,FILMKEY)
        match=re.compile('(.+?)#(.+?)#').findall(DATA)               
        for url , name in match:

            name='GOOGLEVIDEO '+name+'p'
            if ('720' in name) or ('1080' in name):
                name=name.replace('720p','[COLOR green]720P[/COLOR]').replace('1080p','[COLOR green]1080P[/COLOR]')         
            addDir(name,url,200,iconimage,str(NAME))


        
    
def OPEN_URLS(url):
    req = urllib2.Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'})
    con = urllib2.urlopen( req )
    link= con.read()
    return link


def nowvideo(url):
    link=OPEN_URLS(url)
    match=re.compile('<source src="(.+?)"').findall(link)[0]
    return match


def anime(url):
    link=OPEN_URLS(url.replace('at/t','at/nw'))
    match=re.compile('_url = "(.+?)"').findall(link)[0]
    return urllib.unquote(match)


def thevideos(url):
    link=OPEN_URLS(url)
    match=re.compile('file:"(.+?)"').findall(link)
    last=len(match)-1
    return match[last]


    
def PLAY_STREAM(name,url,iconimage,page):    
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':page})
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

def addDir(name,url,mode,iconimage,page):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&page="+urllib.quote_plus(page)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        menu = []
        if mode ==200:
            liz.setProperty("IsPlayable","true")
            
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            menu.append(('Play All Videos','XBMC.RunPlugin(%s?name=%s&mode=2001&iconimage=None&url=%s)'% (sys.argv[0],name,url)))
            liz.addContextMenuItems(items=menu, replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
        
 
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
page=None


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
        page=urllib.unquote_plus(params["page"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        
        CATEGORIES()
       
elif mode==1:
        
        GetContent(url)

elif mode==2:
        
        GetNextPageContent(url,iconimage,page)

elif mode==3:
        
        GetDetail(name,url,iconimage)

elif mode==4:
      
        GetStreamLinks(url,iconimage,name,page)

elif mode==5:
       
        TodayList(url)


elif mode==6:
        
        TodayListGetContent(url)

elif mode==7:
        
        Genre(url)

elif mode==8:
        
        SEARCHPLAYBOX(url)         
        
elif mode==200:

        PLAY_STREAM(name,url,iconimage,page)

elif mode==2001:

        playall(name,url)        
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
