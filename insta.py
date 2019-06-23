'''
Instagram #Hashtag Webscraper
Original code was written by: Srujana Takkallapally @srujana.rao2
https://medium.com/@srujana.rao2/scraping-instagram-with-python-using-selenium-and-beautiful-soup-8b72c186a058

This is a step by step guide for scraping instagram for images based off of the inputted hashtag
'''

print("start importing modules and things") # Prints output between quotation marks
import time # Imports the time module
import re   #^
import json #^
from selenium import webdriver # Searches and loads webdriver in the selenium module
from urllib.request import urlopen          #^
from pandas.io.json import json_normalize   #^
from bs4 import BeautifulSoup as bs # searches and loads BeautifulSoup in the bs4 and gives it the name/alias bs
import pandas as pd, numpy as np    #^

print('Module Import = Done \n \n Start the next bit') #\n will create a new line in the output. Like hitting the enter key

#part ONE (makes hashtag + opens instagram )

hashtag = 'Cal' # This assigns the #hashtag that will be searched for in Instagram
print('Looking for #',hashtag+"!") # Variabales can be included in print functions like this. remember to seperate the pieces of your
                                   # Print function with commas , or plus + signs
browser = webdriver.Chrome(r'C:\Users\19258\Desktop\chromedriver.exe') # Opens the webdriver that will open the corresponding browser
                                                                       # Selenium requires a driver to interface with the chosen browser
                                                                       # All webdrivers can be found at: https://docs.seleniumhq.org/download/
browser.get('https://www.instagram.com/explore/tags/' + hashtag) # Inputs the url with the hashtag 
print("Here is the browser",browser)
Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scrolls to the ZERO position (horizontal)
                                                                                       #document.body.scrollHeight gets the height
print('Part1 is complete')

# part TWO (parse the html + adds ___ to links)

links=[] #creates an empty list "links"
source = browser.page_source
data=bs(source, 'html.parser')
body = data.find('body')
script = body.find('span')
for link in script.findAll('a'):
     # print("This is link",link)
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
print('Part2 is complete')

#part THREE:

import os
import requests
i = 0
result.index = range(len(result.index))
directory= r"C:\Users\19258\Desktop\code\python_test_code\scrape\images\new"

for i in range(len(result)):
    r = requests.get(result['display_url'][i])
    with open(directory+result['shortcode'][i]+".jpg", 'wb') as f:
                    f.write(r.content)

print('Part3 is complete')
print('Fin')
