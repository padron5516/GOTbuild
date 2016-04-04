# coding: utf-8
# Main Addon
__author__ = 'mancuniancol'

from xbmcswift2 import Plugin
from tools2 import *

# INITIALISATION
storage = Storage(settings.storageName, type="dict", eval=True)
plugin = Plugin()

cookies = plugin.get_storage('token', TTL=15)
if cookies.get("token", "") == "":
    response = browser.get(settings.value["urlAddress"] + "?get_token=get_token&app_id=imdb-viewer")
    data = response.json()
    cookies["token"] = data["token"]
    cookies.sync()
    settings.log("new token updated!")


###############################
###  MENU    ##################
###############################
@plugin.route('/')
def index():
    textViewer(settings.string(32000), once=True)
    items = [
        {'label': settings.string(32194),
         'path': plugin.url_for('searchMenu'),
         'thumbnail': dirImages("search.png"),
         'properties': {'fanart_image': settings.fanart}
         }]
    listTypes = ['Genre',
                 'Language',
                 'Popular and Oscar Winners',
                 'TOP 250',
                 ]
    listUrl = ['',
               '',
               '',
               'http://www.imdb.com/chart/top?ref_=nv_ch_250_4',
               '',
               ]
    listIcons = [dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 ]
    listAction = ['genre',
                  'language',
                  'popular',
                  'readID',
                  ]
    for type, url, icon, action in zip(listTypes, listUrl, listIcons, listAction):
        items.append({'label': type,
                      'path': plugin.url_for(action, url=url, showSeasons='True'),
                      'thumbnail': icon,
                      'properties': {'fanart_image': settings.fanart},
                      })
    items.append({'label': settings.string(32016),
                  'path': plugin.url_for('configuration'),
                  'thumbnail': dirImages("settings.png"),
                  'properties': {'fanart_image': settings.fanart}
                  })
    items.append({'label': settings.string(32017),
                  'path': plugin.url_for('help'),
                  'thumbnail': dirImages("help.png"),
                  'properties': {'fanart_image': settings.fanart}
                  })
    return items


@plugin.route('/genre/')
def genre():
    items = []
    listTypes = ['Action',
                 'Action Comedy',
                 'Action Crime',
                 'Action Thriller',
                 'Adventure',
                 'Adventure Biography',
                 'Adventure Thriller',
                 'Adventure War',
                 'Animation',
                 'Animation Adventure',
                 'Animation Comedy',
                 'Animation Family',
                 'Animation Fantasy',
                 'Biography',
                 'Biography Crime',
                 'Biography Mystery',
                 'Biography Sport',
                 'Comedy',
                 'Comedy Action',
                 'Comedy Horror',
                 'Comedy Romance',
                 'Crime',
                 'Crime Drama',
                 'Crime Mystery',
                 'Crime Romance',
                 'Documentary',
                 'Documentary Biography',
                 'Documentary Comedy',
                 'Documentary Crime',
                 'Documentary History',
                 'Drama',
                 'Drama Film-Noir',
                 'Drama Musical',
                 'Drama Romance',
                 'Drama War',
                 'Family',
                 'Family Adventure',
                 'Family Comedy',
                 'Family Fantasy',
                 'Family Romance',
                 'Fantasy',
                 'Fantasy Adventure',
                 'Fantasy Comedy',
                 'Fantasy Drama',
                 'Fantasy Romance',
                 'Film-Noir',
                 'Film-Noir Crime',
                 'Film-Noir Mystery',
                 'Film-Noir Romance',
                 'Film-Noir Thriller',
                 'History',
                 'History Adventure',
                 'History Biography',
                 'History Drama',
                 'History War',
                 'Horror',
                 'Horror Comedy',
                 'Horror Drama',
                 'Horror Sci-fi',
                 'Music',
                 'Music Biography',
                 'Music Documentary',
                 'Music Drama',
                 'Musical',
                 'Musical Comedy',
                 'Musical History',
                 'Musical Romance',
                 'Mystery',
                 'Mystery Adventure',
                 'Mystery Comedy',
                 'Mystery Thriller',
                 'Romance',
                 'Romance Comedy',
                 'Romance Crime',
                 'Romance History',
                 'Romance Thriller',
                 'Sci-fi',
                 'Sci-fi Animation',
                 'Sci-fi Comedy',
                 'Sci-fi Family',
                 'Sci-fi Horror',
                 'Sport',
                 'Sport Biography',
                 'Sport Comedy',
                 'Sport Documentary',
                 'Thriller',
                 'Thriller Comedy',
                 'Thriller Crime',
                 'Thriller Horror',
                 'Thriller Mystery',
                 'War',
                 'War Action',
                 'War Biography',
                 'War Comedy',
                 'War Documentary',
                 'Western',
                 'Western Action',
                 'Western Adventure',
                 'Western Comedy',
                 ]
    listUrl = ['http://www.imdb.com/search/title?genres=action&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=action,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_ac_1',
               'http://www.imdb.com/search/title?count=100&genres=action,crime&num_votes=10000,&title_type=feature&ref_=gnr_mn_ac_2',
               'http://www.imdb.com/search/title?count=100&genres=action,thriller&num_votes=10000,&title_type=feature&ref_=gnr_mn_ac_3',
               'http://www.imdb.com/search/title?genres=adventure&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=adventure,biography&num_votes=10000,&title_type=feature&ref_=gnr_mn_ad_1',
               'http://www.imdb.com/search/title?count=100&genres=adventure,thriller&num_votes=10000,&title_type=feature&ref_=gnr_mn_ad_2',
               'http://www.imdb.com/search/title?count=100&genres=adventure,war&num_votes=10000,&title_type=feature&ref_=gnr_mn_ad_3',
               'http://www.imdb.com/search/title?genres=animation&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=animation,adventure&num_votes=10000,&title_type=feature&ref_=gnr_mn_an_1',
               'http://www.imdb.com/search/title?count=100&genres=animation,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_an_2',
               'http://www.imdb.com/search/title?count=100&genres=animation,family&num_votes=10000,&title_type=feature&ref_=gnr_mn_an_3',
               'http://www.imdb.com/search/title?count=100&genres=animation,fantasy&num_votes=10000,&title_type=feature&ref_=gnr_mn_an_4',
               'http://www.imdb.com/search/title?genres=biography&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=biography,crime&num_votes=10000,&title_type=feature&ref_=gnr_mn_bi_1',
               'http://www.imdb.com/search/title?count=100&genres=biography,mystery&num_votes=5000,&title_type=feature&ref_=gnr_mn_bi_2',
               'http://www.imdb.com/search/title?count=100&genres=biography,sport&num_votes=10000,&title_type=feature&ref_=gnr_mn_bi_3',
               'http://www.imdb.com/search/title?genres=comedy&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=comedy,action&num_votes=10000,&title_type=feature&ref_=gnr_mn_co_1',
               'http://www.imdb.com/search/title?count=100&genres=comedy,horror&num_votes=10000,&title_type=feature&ref_=gnr_mn_co_2',
               'http://www.imdb.com/search/title?count=100&genres=comedy,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_co_3',
               'http://www.imdb.com/search/title?genres=crime&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=crime,drama&num_votes=10000,&title_type=feature&ref_=gnr_mn_cr_1',
               'http://www.imdb.com/search/title?count=100&genres=crime,mystery&num_votes=10000,&title_type=feature&ref_=gnr_mn_cr_2',
               'http://www.imdb.com/search/title?count=100&genres=crime,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_cr_3',
               'http://www.imdb.com/search/title?title_type=documentary&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=documentary,biography&num_votes=1000,&title_type=documentary&ref_=gnr_mn_do_1',
               'http://www.imdb.com/search/title?count=100&genres=documentary,comedy&num_votes=1000,&title_type=documentary&ref_=gnr_mn_do_2',
               'http://www.imdb.com/search/title?count=100&genres=documentary,crime&num_votes=1000,&title_type=documentary&ref_=gnr_mn_do_3',
               'http://www.imdb.com/search/title?count=100&genres=documentary,history&num_votes=1000,&title_type=documentary&ref_=gnr_mn_do_4',
               'http://www.imdb.com/search/title?genres=drama&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=drama,film_noir&num_votes=10000,&title_type=feature&ref_=gnr_mn_dr_2',
               'http://www.imdb.com/search/title?count=100&genres=drama,musical&num_votes=10000,&title_type=feature&ref_=gnr_mn_dr_3',
               'http://www.imdb.com/search/title?count=100&genres=drama,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_dr_1',
               'http://www.imdb.com/search/title?count=100&genres=drama,war&num_votes=10000,&title_type=feature&ref_=gnr_mn_dr_4',
               'http://www.imdb.com/search/title?genres=family&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=family,adventure&num_votes=10000,&title_type=feature&ref_=gnr_mn_fm_1',
               'http://www.imdb.com/search/title?count=100&genres=family,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_fm_2',
               'http://www.imdb.com/search/title?count=100&genres=family,fantasy&num_votes=10000,&title_type=feature&ref_=gnr_mn_fm_3',
               'http://www.imdb.com/search/title?count=100&genres=family,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_fm_4',
               'http://www.imdb.com/search/title?genres=fantasy&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=fantasy,adventure&num_votes=10000,&title_type=feature&ref_=gnr_mn_fa_1',
               'http://www.imdb.com/search/title?count=100&genres=fantasy,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_fa_2',
               'http://www.imdb.com/search/title?count=100&genres=fantasy,drama&num_votes=10000,&title_type=feature&ref_=gnr_mn_fa_3',
               'http://www.imdb.com/search/title?count=100&genres=fantasy,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_fa_4',
               'http://www.imdb.com/search/title?genres=film_noir&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=film_noir,crime&num_votes=10000,&title_type=feature&ref_=gnr_mn_fn_1',
               'http://www.imdb.com/search/title?count=100&genres=film_noir,mystery&num_votes=10000,&title_type=feature&ref_=gnr_mn_fn_2',
               'http://www.imdb.com/search/title?count=100&genres=film_noir,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_fn_3',
               'http://www.imdb.com/search/title?count=100&genres=film_noir,thriller&num_votes=10000,&title_type=feature&ref_=gnr_mn_fn_4',
               'http://www.imdb.com/search/title?genres=history&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=history,adventure&num_votes=10000,&title_type=feature&ref_=gnr_mn_hi_1',
               'http://www.imdb.com/search/title?count=100&genres=history,biography&num_votes=10000,&title_type=feature&ref_=gnr_mn_hi_2',
               'http://www.imdb.com/search/title?count=100&genres=history,drama&num_votes=10000,&title_type=feature&ref_=gnr_mn_hi_3',
               'http://www.imdb.com/search/title?count=100&genres=history,war&num_votes=10000,&title_type=feature&ref_=gnr_mn_hi_4',
               'http://www.imdb.com/search/title?genres=horror&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=horror,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_ho_1',
               'http://www.imdb.com/search/title?count=100&genres=horror,drama&num_votes=10000,&title_type=feature&ref_=gnr_mn_ho_2',
               'http://www.imdb.com/search/title?count=100&genres=horror,sci_fi&num_votes=10000,&title_type=feature&ref_=gnr_mn_ho_3',
               'http://www.imdb.com/search/title?genres=music&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=music,biography&num_votes=10000,&title_type=feature&ref_=gnr_mn_mu_1',
               'http://www.imdb.com/search/title?count=100&genres=documentary,music&num_votes=750,&title_type=documentary&ref_=gnr_mn_mu_2',
               'http://www.imdb.com/search/title?count=100&genres=music,drama&num_votes=10000,&title_type=feature&ref_=gnr_mn_mu_3',
               'http://www.imdb.com/search/title?genres=musical&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=musical,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_ml_1',
               'http://www.imdb.com/search/title?count=100&genres=musical,history&num_votes=10000,&title_type=feature&ref_=gnr_mn_ml_2',
               'http://www.imdb.com/search/title?count=100&genres=musical,romance&num_votes=10000,&title_type=feature&ref_=gnr_mn_ml_3',
               'http://www.imdb.com/search/title?genres=mystery&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=mystery,adventure&num_votes=10000,&title_type=feature&ref_=gnr_mn_my_1',
               'http://www.imdb.com/search/title?count=100&genres=mystery,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_my_2',
               'http://www.imdb.com/search/title?count=100&genres=mystery,thriller&num_votes=10000,&title_type=feature&ref_=gnr_mn_my_3',
               'http://www.imdb.com/search/title?genres=romance&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=romance,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_ro_1',
               'http://www.imdb.com/search/title?count=100&genres=romance,crime&num_votes=10000,&title_type=feature&ref_=gnr_mn_ro_2',
               'http://www.imdb.com/search/title?count=100&genres=romance,history&num_votes=10000,&title_type=feature&ref_=gnr_mn_ro_3',
               'http://www.imdb.com/search/title?count=100&genres=romance,thriller&num_votes=10000,&title_type=feature&ref_=gnr_mn_ro_4',
               'http://www.imdb.com/search/title?genres=sci_fi&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=sci_fi,animation&num_votes=10000,&title_type=feature&ref_=gnr_mn_sf_1',
               'http://www.imdb.com/search/title?count=100&genres=sci_fi,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_sf_2',
               'http://www.imdb.com/search/title?count=100&genres=sci_fi,family&num_votes=10000,&title_type=feature&ref_=gnr_mn_sf_3',
               'http://www.imdb.com/search/title?count=100&genres=sci_fi,horror&num_votes=10000,&title_type=feature&ref_=gnr_mn_sf_4',
               'http://www.imdb.com/search/title?genres=sport&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=sport,biography&num_votes=10000,&title_type=feature&ref_=gnr_mn_sp_1',
               'http://www.imdb.com/search/title?count=100&genres=sport,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_sp_2',
               'http://www.imdb.com/search/title?count=100&genres=sport,documentary&num_votes=1000,&title_type=documentary&ref_=gnr_mn_sp_3',
               'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=thriller,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_th_1',
               'http://www.imdb.com/search/title?count=100&genres=thriller,crime&num_votes=10000,&title_type=feature&ref_=gnr_mn_th_2',
               'http://www.imdb.com/search/title?count=100&genres=thriller,horror&num_votes=10000,&title_type=feature&ref_=gnr_mn_th_3',
               'http://www.imdb.com/search/title?count=100&genres=thriller,mystery&num_votes=10000,&title_type=feature&ref_=gnr_mn_th_4',
               'http://www.imdb.com/search/title?genres=war&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=war,action&num_votes=10000,&title_type=feature&ref_=gnr_mn_wa_1',
               'http://www.imdb.com/search/title?count=100&genres=war,biography&num_votes=10000,&title_type=feature&ref_=gnr_mn_wa_2',
               'http://www.imdb.com/search/title?count=100&genres=war,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_wa_3',
               'http://www.imdb.com/search/title?count=100&genres=war,documentary&num_votes=1000,&title_type=documentary&ref_=gnr_mn_wa_4',
               'http://www.imdb.com/search/title?genres=western&title_type=feature&sort=moviemeter,asc',
               'http://www.imdb.com/search/title?count=100&genres=western,action&num_votes=10000,&title_type=feature&ref_=gnr_mn_we_1',
               'http://www.imdb.com/search/title?count=100&genres=western,adventure&num_votes=10000,&title_type=feature&ref_=gnr_mn_we_2',
               'http://www.imdb.com/search/title?count=100&genres=western,comedy&num_votes=10000,&title_type=feature&ref_=gnr_mn_we_3',
               ]
    listIcons = [dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 ]
    listAction = ['readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  ]
    for type, url, icon, action in zip(listTypes, listUrl, listIcons, listAction):
        items.append({'label': type,
                      'path': plugin.url_for(action, url=url, showSeasons='True'),
                      'thumbnail': icon,
                      'properties': {'fanart_image': settings.fanart},
                      })
    return items


@plugin.route('/language/')
def language():
    items = []
    listTypes = ['Arabic',
                 'Bulgarian',
                 'Chinese',
                 'Croatian',
                 'Dutch',
                 'English',
                 'Finnish',
                 'French',
                 'German',
                 'Greek',
                 'Hebrew',
                 'Hindi',
                 'Hungarian',
                 'Icelandic',
                 'Italian',
                 'Japanese',
                 'Korean',
                 'Norwegian',
                 'Persian',
                 'Polish',
                 'Portuguese',
                 'Punjabi',
                 'Romanian',
                 'Russian',
                 'Spanish',
                 'Swedish',
                 'Turkish',
                 'Ukrainian',
                 ]
    listUrl = ['http://www.imdb.com/search/title?languages= ar|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= bg|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= zh|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= hr|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= nl|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= en|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= fi|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= fr|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= de|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= el|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= he|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= hi|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= hu|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= is|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= it|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= ja|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= ko|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= no|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= fa|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= pl|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= pt|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= pa|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= ro|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= ru|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= es|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= sv|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= tr|1&sort=moviemeter,asc&start=1&title_type=feature',
               'http://www.imdb.com/search/title?languages= uk|1&sort=moviemeter,asc&start=1&title_type=feature',
               ]
    listIcons = [dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("movies.png"),

                 ]
    listAction = ['readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  'readID',
                  ]
    for type, url, icon, action in zip(listTypes, listUrl, listIcons, listAction):
        items.append({'label': type,
                      'path': plugin.url_for(action, url=url, showSeasons='True'),
                      'thumbnail': icon,
                      'properties': {'fanart_image': settings.fanart},
                      })
    return items


@plugin.route('/popular/')
def popular():
    items = []
    listTypes = ['Feature Films',
                 'Feature Films/TV Movies',
                 'TV Movies',
                 'Oscar Winners',

                 ]
    listUrl = ['http://www.imdb.com/search/title?count=100&title_type=feature&ref_=nv_ch_mm_1',
               'http://www.imdb.com/search/title?count=100&title_type=feature,tv_movie&ref_=nv_ch_mm_1',
               'http://www.imdb.com/search/title?count=100&title_type=tv_movie&ref_=nv_ch_mm_1',
               'http://www.imdb.com/search/title?count=100&groups=oscar_best_picture_winners&sort=year,desc&ref_=nv_ch_osc_3'
               ]
    listIcons = [dirImages("movies.png"),
                 dirImages("movies.png"),
                 dirImages("shows.png"),
                 dirImages("movies.png"),
                 ]
    listAction = ['readID',
                  'readID',
                  'readID',
                  'readID',
                  ]
    for type, url, icon, action in zip(listTypes, listUrl, listIcons, listAction):
        items.append({'label': type,
                      'path': plugin.url_for(action, url=url, showSeasons='True'),
                      'thumbnail': icon,
                      'properties': {'fanart_image': settings.fanart},
                      })
    return items


# Search Menu
@plugin.route("/searchMenu/")
def searchMenu():
    items = [
        {'label': settings.string(32195),
         'path': plugin.url_for('search'),
         'thumbnail': dirImages("addSearch.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': settings.string(32196),
         'path': plugin.url_for('list'),
         'thumbnail': dirImages("addList.png"),
         'properties': {'fanart_image': settings.fanart}
         },
        {'label': settings.string(32197),
         'path': plugin.url_for('watchlist'),
         'thumbnail': dirImages("addWatchlist.png"),
         'properties': {'fanart_image': settings.fanart}
         },
    ]
    items.extend(read())
    return items


# Search
@plugin.route('/search/')
def search():
    keywords = settings.dialog.input(settings.string(32154) + ':').replace(' ', '-')
    year1 = settings.dialog.input(settings.string(32198))
    year2 = settings.dialog.input(settings.string(32199))
    if keywords != '':
        url = "http://www.imdb.com/search/title?keywords=%s&sort=moviemeter,asc&title_type=feature&year=%s,%s" \
              % (keywords, year1, year2)
        # Saving part
        response = settings.dialog.yesno(settings.name, settings.string(32193))
        if response:
            name = ''
            while name is '':
                name = settings.dialog.input(plugin.get_string(32192)).title()
            storage.database[name] = (url, False)  # url, isSubscribed
            storage.save()
        return readID(url)


# List
@plugin.route('/list/')
def list():
    list = settings.dialog.input('List:')
    if list.startswith("ls"):
        url = "http://www.imdb.com/list/%s/?&view=detail&sort=listorian:asc" % list
        # Saving part
        response = settings.dialog.yesno(settings.name, settings.string(32193))
        if response:
            name = ''
            while name is '':
                name = settings.dialog.input(plugin.get_string(32192)).title()
            storage.database[name] = (url, False)  # url, isSubscribed
            storage.save()
        return readID(url)


#
# WatchList
@plugin.route('/watchlist/')
def watchlist():
    user = settings.dialog.input('User:')
    if user.startswith("ur"):
        url = "http://www.imdb.com/user/%s/watchlist?ref_=wt_nv_wl_all_0" % user
        # Saving part
        response = settings.dialog.yesno(settings.name, settings.string(32193))
        if response:
            name = ''
            while name is '':
                name = settings.dialog.input(plugin.get_string(32192)).title()
            storage.database[name] = (url, False)  # url, isSubscribed
            storage.save()
        return readID(url)


# Settings
@plugin.route('/configuration/')
def configuration():
    settings.settings.openSettings()
    settings.settings = Settings()


####################################################
@plugin.route('/readID/<url>/<showSeasons>', name="readID")
def readID(url="", showSeasons='True'):  # First Page
    information = plugin.get_storage('information')
    information.clear()
    return nextPage(url=url, showSeasons=showSeasons)


@plugin.route('/nextPage/<url>/<page>/<showSeasons>', name="nextPage")
def nextPage(url="", page="1", showSeasons='True'):
    # First Page
    urlSearch = url
    urlSearch += "&start=%s" % page
    # Read
    settings.log(urlSearch)
    response = browser.get(urlSearch)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # Titles and Urls
    titles = []
    urlSources = []
    links = soup.select("td.title > a")
    if len(links) == 0:
        links = soup.select("td.titleColumn > a")
    if len(links) == 0:
        links = soup.select("div.info b a")
    if len(links) == 0:
        links = soup.select("h3.lister-item-header a")
    for a in links:
        titles.append(a.text)
        urlSources.append(
                settings.value["urlAddress"] + "?mode=search&search_imdb=%s&limit=100" % getID(a["href"]))
    # Create Menu
    createMenu(titles, urlSources)
    items = menu0()

    # Next page
    next = soup.select("span.pagination a")
    if len(next) > 0 and next[0].text.startswith("Next"):
        items.append({'label': "[B]" + settings.string(32191) + "[/B]",
                  'path': plugin.url_for('nextPage', url=url, page=int(page) + len(titles), showSeasons=showSeasons),
                  'thumbnail': dirImages("next11.png"),
                  'info': {'episode': 9999},
                  'properties': {'fanart_image': settings.fanart}
                  })

    if __name__ == '__main__':
        return plugin.finish(items=items, view_mode=settings.value['viewMode'],
                             sort_methods=[24, 'title'])
    else:
        return items


@plugin.route('/readHTML/<url>/<showSeasons>', name="readHTML")
def readHTML(url="", showSeasons='True'):
    information = plugin.get_storage('information')
    information.clear()
    urlSearch = url

    # Read
    data = {}
    loop = True
    while loop:  # if it is a token out-timing
        # Read token
        loop = False
        token = cookies["token"]

        urlSearch = url + "&token=%s" % token
        response = browser.get(urlSearch)
        settings.log(urlSearch)
        data = response.json()

        if data.get("error_code", 0) == 4:
            # the token needs to be renewed
            responseToken = browser.get(settings.value["urlAddress"] + "?get_token=get_token&app_id=imdb-viewer")
            dataToken = responseToken.json()
            cookies["token"] = dataToken["token"]
            cookies.sync()
            settings.log("new token updated!")
            loop = True
        settings.log(token)

    # Case of error or not results to notify the user
    if data.get("error_code", 0) != 0:
        settings.notification(data["error"])

    # Storage information
    source = plugin.get_storage('source')
    source['url'] = url

    # Titles and Urls
    titles = []
    urlSources = []
    for torrent in data["torrent_results"]:
        titles.append(torrent["filename"])
        urlSources.append(torrent["download"])

    # Create Menu
    createMenu(titles, urlSources)
    items = menu1(showSeasons=showSeasons)

    if __name__ == '__main__':
        return plugin.finish(items=items, view_mode=settings.value['viewMode'],
                             sort_methods=[24, 'title'])
    else:
        return items


###################################################
############## COMMON NOT TO CHANGE ###############
###################################################
@plugin.route('/play/<url>')
def play(url):
    magnet = url
    # Set-up the plugin
    uri_string = quote_plus(getPlayableLink(uncodeName(magnet)))
    if settings.value["plugin"] == 'Quasar':
        link = 'plugin://plugin.video.quasar/play?uri=%s' % uri_string
    elif settings.value["plugin"] == 'Pulsar':
        link = 'plugin://plugin.video.pulsar/play?uri=%s' % uri_string
    elif settings.value["plugin"] == 'KmediaTorrent':
        link = 'plugin://plugin.video.kmediatorrent/play/%s' % uri_string
    elif settings.value["plugin"] == "Torrenter":
        link = 'plugin://plugin.video.torrenter/?action=playSTRM&url=' + uri_string + \
               '&not_download_only=True'
    elif settings.value["plugin"] == "YATP":
        link = 'plugin://plugin.video.yatp/?action=play&torrent=' + uri_string
    else:
        link = 'plugin://plugin.video.xbmctorrent/play/%s' % uri_string
    # play media
    settings.debug("PlayMedia(%s)" % link)
    xbmc.executebuiltin("PlayMedia(%s)" % link)


@plugin.route('/help/')
def help():
    textViewer(plugin.get_string(32000), once=False)


@plugin.route('/unsubscribe/<key>')
def unsubscribe(key=""):
    storage.database[key] = (storage.database[key][0], False)
    storage.save()


@plugin.route('/subscribe/<key>/<url>')
def subscribe(key="", url=""):
    storage.add(key, (url, True), safe=False)
    storage.save()
    importAll(url)


@plugin.route('/importOne/<title>')
def importOne(title=""):
    information = plugin.get_storage('information')
    info = information[title][0]
    integration(titles=[title], magnets=[info.fileName], id=[info.id], typeVideo=[info.typeVideo], silence=True)


@plugin.route('/importAll/<url>')
def importAll(url=""):
    items = readHTML(url, showSeasons="False")  # only to create information
    information = plugin.get_storage('information')
    titles = []
    fileNames = []
    typeVideos = []
    ids = []
    for title in information:
        temp, level1 = information[title]
        for season in level1:
            level2 = level1[season]
            for episode in level2:
                temp, level3 = level2[episode]
                for info in level3:
                    ids.append(info.id)
                    titles.append(info.infoTitle["title"])
                    fileNames.append(info.fileName)
                    typeVideos.append(info.typeVideo)
    integration(titles=titles, magnets=fileNames, id=ids, typeVideo=typeVideos, silence=True)


@plugin.route('/rebuilt/<url>')
def rebuilt(url):
    overwrite = settings.value["overwrite"]  # save the user's value
    settings.value["overwrite"] = "true"  # force to overwrite
    importAll(url)
    settings.value["overwrite"] = overwrite  # return the user's value
    settings.log(url + " was rebuilt")


@plugin.route('/remove/<key>')
def remove(key=""):
    if settings.dialog.yesno(settings.cleanName, plugin.get_string(32006) % key):
        storage.remove(key, safe=False)
        storage.save()


@plugin.route('/modify/<key>')
def modify(key):
    selection = settings.dialog.input(plugin.get_string(32007), storage.database[key][0])
    newKey = ''
    while newKey is '':
        newKey = settings.dialog.input(plugin.get_string(32008), key).title()
    storage.database[newKey] = (selection, storage.database[key][1])
    if newKey != key: storage.remove(key, safe=False)
    storage.save()


def read():
    # list storage search
    items = []
    for key in sorted(storage.database):  # sort the dictionnary
        (url, isIntegrated) = storage.database[key]
        settings.debug(url)
        settings.debug(isIntegrated)
        if isIntegrated:
            importInfo = (plugin.get_string(32001),
                          'XBMC.Container.Update(%s)' % plugin.url_for('unsubscribe', key=key))
        else:
            importInfo = (plugin.get_string(32002),
                          'XBMC.Container.Update(%s)' % plugin.url_for('subscribe', key=key, url=url))
        items.append({'label': "- " + key,
                      'path': plugin.url_for('readID', url=url, showSeasons='True'),
                      'thumbnail': dirImages(key[0] + '.png'),
                      'properties': {'fanart_image': settings.fanart},
                      'context_menu': [importInfo,
                                       (plugin.get_string(32187),
                                        'XBMC.Container.Update(%s)' % plugin.url_for('remove', key=key)),
                                       (plugin.get_string(32188),
                                        'XBMC.Container.Update(%s)' % plugin.url_for('modify', key=key)),
                                       (plugin.get_string(32045),
                                        'XBMC.Container.Update(%s)' % plugin.url_for('rebuilt', url=url))
                                       ]
                      })
    return items


# Create the storage from titles and urls
def createMenu(titles=[], urlSources=[], typeVideo=""):
    information = plugin.get_storage('information')
    page = plugin.get_storage('page')
    page.clear()
    for title, urlSource in zip(titles, urlSources):
        # it gets all the information from the title and url
        info = UnTaggle(title, urlSource, typeVideo=typeVideo)  # Untaggle
        temp, level1 = information.get(info.infoTitle["folder"], ("", {}))  # infoLabels, dictionnary seasons
        level2 = level1.get(str(info.season), {})  # dictionnary episodes
        temp, level3 = level2.get(str(info.episode), ("", []))  # list info for that episode
        level3.append(info)  # add new info video
        level2[str(info.episode)] = (info, level3)
        level1[str(info.season)] = level2
        information[info.infoTitle["folder"]] = (info, level1)
        page[info.infoTitle["folder"]] = (info, level1)


def menu0(showSeasons='True'):  # create the menu for first level
    information = plugin.get_storage('page')
    source = plugin.get_storage('source')
    items = []
    typeVideo = "MOVIE"
    for title in information.keys():
        info, level1 = information.get(title, ("", {}))  # infoLabels, dictionnary seasons
        typeVideo = info.typeVideo
        try:
            items.append({'label': info.infoTitle["folder"],
                          'path': plugin.url_for('readHTML', url=info.fileName, showSeasons=showSeasons),
                          'thumbnail': info.infoLabels.get('cover_url', settings.icon),
                          'properties': {'fanart_image': info.fanart},
                          'info': info.infoLabels,
                          })
        except:
            pass
    # main
    if __name__ == '__main__':
        plugin.set_content("movies" if typeVideo == "MOVIE" else "tvshows")
    return items


@plugin.route('/menu1')
def menu1(showSeasons='True'):  # create the menu for first level
    information = plugin.get_storage('page')
    source = plugin.get_storage('source')

    items = []
    typeVideo = "MOVIE"
    if len(information.keys()) == 1:
        items = menu2(information.keys()[0], showSeasons=showSeasons)
    else:
        for title in information.keys():
            info, level1 = information.get(title, ("", {}))  # infoLabels, dictionnary seasons
            typeVideo = info.typeVideo
            if typeVideo == 'MOVIE':
                extraInfo = ("Extended Info",
                             'XBMC.RunScript(script.extendedinfo,info=extendedinfo,imdb_id=%s)' % info.imdb_id)
            else:
                extraInfo = ("Extended Info",
                             'XBMC.RunScript(script.extendedinfo,info=extendedtvinfo,imdb_id=%s)' % info.imdb_id)
            try:
                items.append({'label': info.infoTitle["folder"],
                              'path': plugin.url_for('menu2', title=info.infoTitle["folder"]),
                              'thumbnail': info.infoLabels.get('cover_url', settings.icon),
                              'properties': {'fanart_image': info.fanart},
                              'info': info.infoLabels,
                              'context_menu': [extraInfo],
                              })
            except:
                pass
        # main
        if __name__ == '__main__':
            plugin.set_content("movies" if typeVideo == "MOVIE" else "tvshows")
    return items


@plugin.route('/menu2/<title>')
def menu2(title="", showSeasons='True'):  # create the menu for second level
    information = plugin.get_storage('information')
    items = []
    typeVideo = "MOVIE"
    info, level1 = information.get(title, ("", {}))  # infoLabels, dictionnary seasons
    if len(level1) == 1:
        items = menu3(title, level1.keys()[0])
    else:
        for season in level1.keys():
            if showSeasons == 'True':
                typeVideo = info.typeVideo
                if typeVideo == 'MOVIE':
                    extraInfo = ("Extended Info",
                                 'XBMC.RunScript(script.extendedinfo,info=extendedinfo,imdb_id=%s)' % info.imdb_id)
                else:
                    extraInfo = ("Extended Info",
                                 'XBMC.RunScript(script.extendedinfo,info=seasoninfo,tvshow=%s, season=%s)' % (
                                     info.infoTitle['cleanTitle'], season))
                try:
                    items.append({'label': "Season %s" % season,
                                  'path': plugin.url_for('menu3', title=title, season=season),
                                  'thumbnail': info.infoLabels.get('cover_url', settings.icon),
                                  'properties': {'fanart_image': info.fanart},
                                  'info': info.infoLabels,
                                  'context_menu': [extraInfo],
                                  })
                except:
                    pass
            else:
                items.extend(menu3(title=title, season=season))
        # main
        if __name__ == '__main__':
            plugin.set_content("movies" if typeVideo == "MOVIE" else "tvshows")
    return items


@plugin.route('/menu3/<title>/<season>')
def menu3(title="", season=""):  # create the menu for third level
    information = plugin.get_storage('information')
    items = []
    typeVideo = "MOVIE"
    temp, level1 = information.get(title, ("", {}))  # infoLabels, dictionnary seasons
    level2 = level1[season]
    if len(level2) == 1:
        items = menu4(title, season, level2.keys()[0])
    else:
        for episode in level2.keys():
            info, level3 = level2[episode]  # dictionnary episodes
            typeVideo = info.typeVideo
            if typeVideo == 'MOVIE':
                extraInfo = ("Extended Info",
                             'XBMC.RunScript(script.extendedinfo,info=extendedinfo,imdb_id=%s)' % info.imdb_id)
            else:
                extraInfo = ("Extended Info",
                             'XBMC.RunScript(script.extendedinfo,info=extendedepisodeinfo,tvshow=%s, season=%s, episode=%s)' % (
                                 info.infoTitle['cleanTitle'], season, episode))
            try:
                items.append({'label': info.infoTitle["title"] + info.titleEpisode,
                              'path': plugin.url_for('menu4', title=title, season=season, episode=episode),
                              'thumbnail': info.cover,
                              'properties': {'fanart_image': info.fanart},
                              'info': info.info,
                              'context_menu': [extraInfo],
                              })
            except:
                pass
        # main
        if __name__ == '__main__':
            plugin.set_content("movies" if typeVideo == "MOVIE" else "episodes")
    return items


@plugin.route('/menu4/<title>/<season>/<episode>')
def menu4(title="", season="", episode=""):  # create the menu for last level
    information = plugin.get_storage('information')
    items = []
    typeVideo = "MOVIE"
    temp, level1 = information.get(title, ("", {}))  # infoLabels, dictionnary seasons
    level2 = level1[season]
    temp, level3 = level2[episode]
    for info in level3:
        typeVideo = info.typeVideo
        if typeVideo == 'MOVIE':
            extraInfo = ("Extended Info",
                         'XBMC.RunScript(script.extendedinfo,info=extendedinfo,imdb_id=%s)' % info.imdb_id)
        else:
            extraInfo = ("Extended Info",
                         'XBMC.RunScript(script.extendedinfo,info=extendedepisodeinfo,tvshow=%s, season=%s, episode=%s)' % (
                             info.infoTitle['cleanTitle'], season, episode))
        try:
            items.append({'label': info.label,
                          'path': plugin.url_for('play', url=info.fileName),
                          'thumbnail': info.cover,
                          'properties': {'fanart_image': info.fanart},
                          'info': info.info,
                          'stream_info': info.infoStream,
                          'context_menu': [
                              (plugin.get_string(32009),
                               'XBMC.RunPlugin(%s)' % plugin.url_for('importOne', title=title)),
                              extraInfo
                          ]
                          })
        except:
            pass
        # main
        if __name__ == '__main__':
            plugin.set_content("movies" if typeVideo == "MOVIE" else "episodes")
    return items


def getID(value=""):
    from re import search
    result = ""
    results = search("tt\\d{7}", value)
    if results <> None:
        result = results.group(0)
    return result


if __name__ == '__main__':
    try:
        plugin.run()
    except:
        pass
