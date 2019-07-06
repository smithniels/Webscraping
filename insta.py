'''
Instagram #Hashtag Webscraper

# Modules to check out:
#     log
#     pillows

Original code was written by: Srujana Takkallapally @srujana.rao2
https://medium.com/@srujana.rao2/scraping-instagram-with-python-using-selenium-and-beautiful-soup-8b72c186a058
This is a step by step guide for scraping instagram for images based off of the inputted hashtag

TODO: Save a CSV Of JSON data into time stamped folder
TODO: Put things into functions
TODO: Duplicate images are being saved
    Figure out what the unique identifer is
'''
# TODO: Finish commenting to explain what the hell each line is doing, for the children...
# TODO: Why do l's keep being capitalized? This is definitely an Atom issue

print("Start importing modules and things") # Prints output between quotation marks
import json     # Imports the ____ module
import os
import re
import time
import requests
import pprint
from pandas.io.json import json_normalize   # Searches the ___ module and imports _____
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs         # loads ____ module and imports ____ giving it the alias _____
import numpy  as np
import pandas as pd

hashtag = 'Boop' # This assigns the #hashtag that will be searched for in Instagram

print('Module Import is Complete') #\n will create a new line in the output. Like hitting the enter key in a word document

def webscrapeIG():
    # part ONE (makes hashtag + opens instagram )
    print('Searching for #' , hashtag) # Variabales can be included in print functions like this. remember to seperate the pieces of your
                                        # Print function with commas , or plus + signs
    browser = webdriver.Chrome(r'C:\Users\19258\Desktop\chromedriver.exe') # Finds the webdriver.exe on the path provided
                                                                           # Selenium requires a driver to interface with the chosen browser
                                                                           # All webdrivers can be found at: https://docs.seleniumhq.org/download/
                                                                           # You will need to download the corresponding webdriver for the browser you want to use
    browser.get('https://www.instagram.com/explore/tags/' + hashtag) # Load the page at the given url with the #Hashtag
    Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scrolls to the ZERO position (horizontal)
    print('Part 1 is complete')                                                             # Document.body.scrollHeight gets the height


    # part TWO (parse the html + adds ___ to links)

    links = []                                # Creates an empty list "links"
    source = browser.page_source              # Open the source page
    data = bs(source, 'html.parser')          # Use beautiful soup to parse it.
    body = data.find('body')                  # Search through BeautifulSoup file for <body> tags
    script = body.find('span')                # Within the <body> tags in "body", find the <span> tags
    for link in script.findAll('a'):          # For the <span> tags in "script", find the <a..>
         if re.match("/p", link.get('href')): # Searching for this format <a href="/p..."
            links.append('https://www.instagram.com' + link.get('href')) # Adds those ^ to the links links if true
    result = pd.DataFrame()                   # Creates an empty dataframe
    c = 0
    for i in range(len(links)):               # Iterates from zero to the length of the list list
        try:                                  # The try block lets you test a block of code for errors.
            c +=1
            page = urlopen(links[i]).read()   # Searches for the i'th item from the list and opens it with urlib imported from the urllib.request module
            data = bs(page, 'html.parser')    # Uses the BeautifulSoup html parser to load the 'page' url as soup data to  'data'
            body = data.find('body')          # Finds the <body> t  ag in the soup and puts it into 'body'
            script = body.find('script')      # Finds the <script...> and puts it into 'script'
            raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
            json_data = json.loads(raw)      # json.loads() is turning the JSON data into a py object
            posts = json_data['entry_data']['PostPage'][0]['graphql'] # Within the json_data find entry_data then dive in until you find the graphql
            posts = json.dumps(posts)        # Encodes into JSON
            posts = json.loads(posts)        # Decodses JSon
            x = pd.DataFrame.from_dict(json_normalize(posts))
            x.columns =  x.columns.str.replace("shortcode_media.", "")
            result=result.append(x,sort = True) # Add(append) x to the result


            # with open('testthree.csv','w',newline = '') as c:
            #     print(posts)
            #     c.write(posts)



        except:       # The except block lets you handle the error
            np.nan    # np.nan will return an NaN (null)
    result = result.drop_duplicates(subset = 'shortcode') # Check for the duplicates # Looks for duplicates in the 'shortcode' columnx` only
    print(c, " Images Found")
    print('Part 2 is complete')

    # part THREE: This is the part where the images are loaded on your computah
    timestamp = str(time.time())
    result.index = range(len(result.index)) # range(x) creates a series of numbers from 0 to x
    directory= r"C:\Users\19258\Desktop\code\python_test_code\scrape\images"  # This is where the photos will be saved to | The r is for "raw" file
    final_directory = os.path.join(directory, hashtag,timestamp)

    if not os.path.exists(final_directory):
        os.makedirs(final_directory,exist_ok=True)
    os.chdir(directory)
    for i in range(len(result)):                    # Iterates through the length of the data frame
        r = requests.get(result['display_url'][i])  # Find display_url and download the respective jpeg from the result data frame

        # outfile = result['shortcode'][i]+ "_" +hashtag +".jpg"
        # with open(os.path.join(directory, outfile), 'wb') as f:
        #     f.writer(r.content)
        with open(final_directory + '/' + result['shortcode'][i]+ "_" + hashtag + "_"+".jpg", 'wb') as f: # Save the images to the directory folder      # 'wb' stands for write binar
                        f.write(r.content)   # With their respective shortcode
    print(os.getcwd())
    print('Part 3 is complete')
    print('Fin')

if __name__ == '__main__':
    webscrapeIG()

'''
Open CSV --> Write JSON data to CSV --> Save the CSV
'''

'''
Run Time
29 sec 07/05/19 - 9:43 AM
73 sec 07/05/19 - 9:45 AM
67 sec 07/05/19 - 9:49 AM
89 sec 07/05/19 - 9:51 AM
45 sec 07/05/19 - 5:02 PM
58 sec 07/05/19 - 8:40 AM
'''
