'''
Instagram #Hashtag Webscraper
Original code was written by: Srujana Takkallapally @srujana.rao2
https://medium.com/@srujana.rao2/scraping-instagram-with-python-using-selenium-and-beautiful-soup-8b72c186a058

This is a step by step guide for scraping instagram for images based off of the inputted hashtag

TODO: Finish commenting to explain what the hell each line is doing, for the children...
'''

print("Start importing modules and things") # Prints output between quotation marks
import time     # Imports the ____ module
import re       #^
import json     #^
from os import mkdirs       #^
import requests #^
from selenium import webdriver              # Searches and loads webdriver in the selenium module
from urllib.request import urlopen          #^
from pandas.io.json import json_normalize   #^
from bs4 import BeautifulSoup as bs         # Searches and loads BeautifulSoup in the bs4 and gives it the name(alias) "bs"
import pandas as pd                         #^
import numpy  as np                         #^
print('Module Import = Done \n \n Start the next bit') #\n will create a new line in the output. Like hitting the enter key in a word document

#part ONE (makes hashtag + opens instagram )

hashtag = 'BFTC' # This assigns the #hashtag that will be searched for in Instagram
print('Looking for >#',hashtag+"<") # Variabales can be included in print functions like this. remember to seperate the pieces of your
                                    # Print function with commas , or plus + signs
browser = webdriver.Chrome(r'C:\Users\19258\Desktop\chromedriver.exe') # Finds the webdriver.exe on the path provided
                                                                       # Selenium requires a driver to interface with the chosen browser
                                                                       # All webdrivers can be found at: https://docs.seleniumhq.org/download/
                                                                       # You will need to download the corresponding webdriver for the browser you want to use
browser.get('https://www.instagram.com/explore/tags/' +hashtag) # Load the page at the given url with the #Hashtag
Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scrolls to the ZERO position (horizontal)
print('Part1 is complete')                                                             # Document.body.scrollHeight gets the height


# part TWO (parse the html + adds ___ to links)

links=[]                                  # Creates an empty list "links"
source = browser.page_source              # Open the source page
data = bs(source, 'html.parser')          # Use beautiful soup to parse it.
body = data.find('body')                  # Search through BeautifulSoup file for <body> tags
script = body.find('span')                # Within the <body> tags in "body", find the <span> tags
for link in script.findAll('a'):          # For the <span> tags in "script", find the <a..>
     if re.match("/p", link.get('href')): # Searching for this format <a href="/p..."
        links.append('https://www.instagram.com'+link.get('href')) # Adds those ^ to the links links if true
result = pd.DataFrame()                   # Creates an empty dataframe
for i in range(len(links)):               # Iterates from zero to the length of the list list
    try:                                  # The try block lets you test a block of code for errors.
        page = urlopen(links[i]).read()   # Searches for the i'th item from the list and opens it with urlib imported from the urllib.request module
        data = bs(page, 'html.parser')    # Uses the BeautifulSoup html parser to load the 'page' url as soup data to  'data'
        body = data.find('body')          # Finds the <body> t  ag in the soup and puts it into 'body'
        script = body.find('script')      # Finds the <script...> and puts it into 'script'
        raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
        json_data = json.loads(raw)       # json.loads() is turning the JSON data into a py object
        posts = json_data['entry_data']['PostPage'][0]['graphql'] # Within the json_data find entry_data then dive in until you find the graphql
        posts = json.dumps(posts) # Encodes into JSON
        posts = json.loads(posts) # Decodses JSon
        x = pd.DataFrame.from_dict(json_normalize(posts))
        x.columns =  x.columns.str.replace("shortcode_media.", "")
        result=result.append(x) # Add(append) x to the result
    except:                     # The except block lets you handle the error
        np.nan                  # np.nan will return an NaN (null)
result = result.drop_duplicates(subset = 'shortcode') # Check for the duplicates # Looks for duplicates in the 'shortcode' column only

print('Part2 is complete')

#part THREE: This is the part where the images are loaded on your computah
result.index = range(len(result.index)) # range(x) creates a series of numbers from 0 to x


# try:  #this path is going to need 'format', I think. I dunno. Python is hard. These are needed {} 
#     os.mkdirs(r"C:\Users\19258\Desktop\code\python_test_code\scrape\images\new"+hashtag)
# except FileExistsError:
#     pass



directory= r"C:\Users\19258\Desktop\code\python_test_code\scrape\images\new"  # This is where the photos will be saved to
for i in range(len(result)):                                       #iterates through the length of the data frame
    r = requests.get(result['display_url'][i])                     # Find display_url and download the respective jpeg from the result data frame
    with open(directory + result['shortcode'][i]+ "_" +hashtag +".jpg", 'wb') as f: # Save the images to the directory folder      # 'wb' stands for write binary
                    f.write(r.content)                             # With their respective shortcode
print('Part3 is complete')
print('Fin')
