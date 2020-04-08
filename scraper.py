"""
@author: North America Team
"""

# =============================================================================
# %% URLs
# =============================================================================
​
#An example of how to input the keywords.
#urls = ['https://www.usatoday.com/search/?q=toilet+paper',
#    'https://www.wsj.com/search/term.html?KEYWORDS=toilet%20paper&min-date=2016/04/05&max-date=2020/04/05&isAdvanced=true&daysback=4y&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,interactivemedia,sitesearch,wsjpro',
#    'https://www.nytimes.com/search?dropmab=true&endDate=20200405&query=toilet%20paper&sort=newest&startDate=20190405',
​
#     https://nypost.com/search/toilet+paper/?sf=20180101&orderby=date&order=desc''
#    'https://www.latimes.com/search?s=1&q=toilet+paper',
#    'https://www.washingtonpost.com/newssearch/?datefilter=All%20Since%202005&sort=Date&query=toilet%20paper',
​
#    'https://www.startribune.com/search/?sort=date-desc&q=toilet+paper',
#    'https://www.newsday.com/search#filter=stories&query=toilet%20paper',
#    "doesn't have an option for news searching",
​
#    'https://www3.bostonglobe.com/queryResult/search?q=toilet%20paper&p1=BGMenu_Search&arc404=true']
​
#urls = ['https://www.usatoday.com/search/?q=',
#        ['https://www.wsj.com/search/term.html?min-date=2018/01/01', '&max-date=2020/04/05', '&isAdvanced=true&daysback=4y&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,interactivemedia,sitesearch,wsjpro&KEYWORDS='],
#        'https://www.nytimes.com/search?dropmab=true&endDate=20200405&startDate=20180101&sort=newest&query=toilet%20paper',
​
#        ['https://nypost.com/search/', '', '/?sf=20180101&orderby=date&order=desc', ],
#        'https://www.latimes.com/search?s=1&q=',
#        'https://www.washingtonpost.com/newssearch/?datefilter=All%20Since%202005&sort=Date&query=',
​
#        'https://www.startribune.com/search/?sort=date-desc&q=',
#        'https://www.newsday.com/search#filter=stories&query=',
#        "doesn't have an option for news searching",
​
#        ['https://www3.bostonglobe.com/queryResult/search?','q=toilet%20paper','&p1=BGMenu_Search&arc404=true']
#        ]
​
​
urls = {'usa_today': ['https://www.usatoday.com/search/?q='],
'wsj': ['https://www.wsj.com/search/term.html?min-date=2018/01/01&max-date=', '&isAdvanced=true&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,interactivemedia,sitesearch,wsjpro&KEYWORDS='],
'ny_t': ['https://www.nytimes.com/search?dropmab=true&endDate=','&startDate=20180101&sort=newest&query='],
​
'ny_p': ['https://nypost.com/search/', '/?sf=20180101&orderby=date&order=desc'],
'la_t': ['https://www.latimes.com/search?s=','&q='],
'washington_p': ['https://www.washingtonpost.com/newssearch/?datefilter=All%20Since%202005&sort=Date&query='],
​
'star_t': ['https://www.startribune.com/search/?sort=date-desc&q='],
'news_day': ['https://www.newsday.com/search#filter=stories&query='],
'chicago_t': False,
'boston_g': ['https://www3.bostonglobe.com/queryResult/search?q=','&p', '=BGMenu_Search&arc404=true']
}
​
​
# masks format ['separator for words', 'format of date', 'Does it have different pages?', [array. index of the string number where the search, the date, and the pagination must be joined]]
masks = {'usa_today': {'q_sep':['+', 0]},
         'wsj': {'q_sep': ['%20', 1], 'd_sep': ['/',0]},
         'ny_t': {'q_sep':['%20',1], 'd_sep':['',0]},
​
         'ny_p': {'q_sep':['%20',0]},
         'la_t': {'q_sep':['+',1], 'pag':[True,0]},
         'washington_p': {'q_sep':['%20',0]},
​
         'star_t': {'q_sep': ['+',0]},
         'news_day': {'q_sep':['%20',0]},
         'chicago_t': {},
​
         'boston_g': {'q_sep':['%20',0], 'pag':[True,1]}
        }
​
​
​
# =============================================================================
# %% Imports
# =============================================================================
​
import numpy as np
import pandas as pd
​
from threading import Thread
​
from threading import Timer
import gc,requests,json
​
from datetime import datetime
​
from bs4 import BeautifulSoup
​
​
​
# =============================================================================
# %% Functions
# =============================================================================
​
def downloadPage(url,verbose):
​
    page = requests.get(url)
    print('Status Code: '+str(page.status_code))
    if verbose:
        print(page)
​
    return page
​
​
​
​
​
# =============================================================================
# %% Settings
# =============================================================================
​
keyword = 'toilet paper'
end_date = str(datetime(2020, 4, 5))[:10]
​
​
# =============================================================================
# %% Download Pages
# =============================================================================
​
​
pages_ = {}
​
# iter through the urls and its masks
keys = list(urls.keys())
for key in keys:
    url = urls[key]
    mask = masks[key]
    
    keys_mask = list(mask.keys())
    for key_mask in keys_mask:
        if key_mask == 'q_sep':
            #convert the work into a readable format for the databse of the page
            keyword_temp = keyword.replace(' ', mask[key_mask][0])
            idx = mask[key_mask][1]
            url[idx] = ''.join([url[idx],keyword_temp])
            
        elif key_mask == 'd_sep':
            end_date_temp = end_date.replace('-', mask[key_mask][0])
            idx = mask[key_mask][1]
            url[idx] = ''.join([url[idx],end_date_temp])
            
        elif key_mask == 'pag':
            n = 1
            #TO DO: ge the number of pages so is easier to iterate through.
            idx = mask[key_mask][1]
            url[idx] = ''.join([url[idx],str(n)])
    
    if url:
        url = ''.join(url)
    
#        Download the name of the pages
        page = downloadPage(url,True)
        
        #parse the page
        page_parsed = BeautifulSoup(page.content, 'html.parser')
        
        pages_[key] = page_parsed
        f = open(key+'.txt', 'wb')
        f.write(page.content)
        f.close()
