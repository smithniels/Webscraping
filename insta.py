from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np

print('is this working?')
#part ONE (makes hashtag + opens instagram )
# username = 'smithkneels'

hashtag='Denmark'
browser = webdriver.Chrome(r'C:\Users\19258\Desktop\chromedriver.exe')
browser.get('https://www.instagram.com/explore/tags/'+hashtag)
Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scrolls to the ZERO position (horizontal)
                                                                                       #document.body.scrollHeight gets the height

# part TWO (parse the html + adds ___ to links)
links=[]
source = browser.page_source
data=bs(source, 'html.parser')
body = data.find('body')
script = body.find('span')
for link in script.findAll('a'):
     if re.match("/p", link.get('href')):
        links.append('https://www.instagram.com'+link.get('href'))

result=pd.DataFrame()
for i in range(len(links)):
    try:
        page = urlopen(links[i]).read()
        data=bs(page, 'html.parser')
        body = data.find('body')
        script = body.find('script')
        raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
        json_data=json.loads(raw)
        posts =json_data['entry_data']['PostPage'][0]['graphql']
        posts= json.dumps(posts)
        posts = json.loads(posts)
        x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns')
        x.columns =  x.columns.str.replace("shortcode_media.", "")
        result=result.append(x)

    except:
        np.nan
# Just check for the duplicates
result = result.drop_duplicates(subset = 'shortcode')
result.index = range(len(result.index))

#part FIVE
import os
import requests
result.index = range(len(result.index))
directory= r"C:\Users\19258\Desktop\Code"
for i in range(len(result)):
    r = requests.get(result['display_url'][i])
    with open(directory+result['shortcode'][i]+".jpg", 'wb') as f:
                    f.write(r.content)
