from beautifulscraper import BeautifulScraper
import urllib
import os, os.path

scraper = BeautifulScraper()

#Url with emojis
url = 'https://www.webfx.com/tools/emoji-cheat-sheet/'

#Goes to url
page = scraper.go(url)

#List of all spans with class='emoji'
spans = page.find_all("span",{"class":"emoji"})

#For every emoji in the list of spans
for emoji in spans:
    #Get path for emoji picture
    image_path = emoji['data-src']

    #Split path for every '/'
    parts = image_path.split("/")

    #Grab the picture and save in emoji folder under its picture name
    urllib.request.urlretrieve(url + image_path, 'emojis/'+parts[-1])
