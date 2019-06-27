'''
TODO: Finish adding comments
TODO: Spellcheck/Review existing comments

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
from bs4 import BeautifulSoup as bs         # searches and loads BeautifulSoup in the bs4 and gives it the name(alias) "bs"
import pandas as pd, numpy as np            #^

print('Module Import = Done \n \n Start the next bit') #\n will create a new line in the output. Like hitting the enter key

#part ONE (makes hashtag + opens instagram )

hashtag = 'damn' # This assigns the #hashtag that will be searched for in Instagram
print('Looking for >#',hashtag+"<") # Variabales can be included in print functions like this. remember to seperate the pieces of your
                                   # Print function with commas , or plus + signs
browser = webdriver.Chrome(r'C:\Users\19258\Desktop\chromedriver.exe') # Finds the webdriver.exe on the path provided
                                                                       # Selenium requires a driver to interface with the chosen browser
                                                                       # All webdrivers can be found at: https://docs.seleniumhq.org/download/
                                                                       # You will need to download the corresponding webdriver for the browser you want to use
browser.get('https://www.instagram.com/explore/tags/' +hashtag) # Load the page at the given url with the #Hashtag
print("Here is the browser",browser)
Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scrolls to the ZERO position (horizontal)
                                                                                       # Document.body.scrollHeight gets the height
print('Part1 is complete')

# part TWO (parse the html + adds ___ to links)

links=[] #creates an empty list "links"
source = browser.page_source # Open the source page
data = bs(source, 'html.parser') # Use beautiful soup to parse it.
body = data.find('body')         # Search through BeautifulSoup file for <body> tags
script = body.find('span')       # Within the <body> tags in "body", find the <span> tags
for link in script.findAll('a'): # For the <span> tags in "script", find the <a..>
     if re.match("/p", link.get('href')):   # Searching for this format <a href="/p..."
        links.append('https://www.instagram.com'+link.get('href')) # Adds those ^ to the links links if true

result = pd.DataFrame()     # Creates an empty dataframe
for i in range(len(links)): # Iterates from zero to the length of the list list
    try:                    # The try block lets you test a block of code for errors.
        page = urlopen(links[i]).read()   # Searches for the i'th item from the list and opens it with urlib imported from the urllib.request module
        data = bs(page, 'html.parser')    # Uses the BeautifulSoup html parser to load the 'page' url as soup data to  'data'
        body = data.find('body')          # Finds the <body> tag in the soup and puts it into 'body'
        script = body.find('script')      # Finds the <script...> and puts it into 'script'
        # print(script)
        raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
        # print("this is raw! ",raw)
        json_data=json.loads(raw)
        posts =json_data['entry_data']['PostPage'][0]['graphql']
        posts = json.dumps(posts)
        posts = json.loads(posts)
        x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns')
        x.columns =  x.columns.str.replace("shortcode_media.", "")
        result=result.append(x)
    except: # The except block lets you handle the error
        np.nan # np.nan will return an NaN (null)
# Just check for the duplicates
result = result.drop_duplicates(subset = 'shortcode')
result.index = range(len(result.index))
print('Part2 is complete')

#part THREE: This is the part where the images are loaded on your computah

import os
import requests
result.index = range(len(result.index))
directory= r"C:\Users\19258\Desktop\code\python_test_code\scrape\images\new"

for i in range(len(result)):
    r = requests.get(result['display_url'][i])
    with open(directory+result['shortcode'][i]+".jpg", 'wb') as f:
                    f.write(r.content)

print('Part3 is complete')
print('Fin')
