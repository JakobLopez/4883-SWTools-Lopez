from beautifulscraper import BeautifulScraper
from pprint import pprint
import json
import urllib
import requests

scraper = BeautifulScraper()

#Years 2009 to 2018
years = list(range(2009, 2018))

weeks = list(range(1,18))

#Dictionary of REG & POST keys that have list values 
gameIDs = {
    'REG': [],
    'POST': []
}

f = open("gameIDs.json","w")

"""
Gets gameID for every game
Params:
    year - year to get gameIDs from
    stype - season type: REG or POST
    week - week to get gameIDs from (only for REG season)
"""
def scrape_data(year, stype, week = None):
    #URL is different depending on season type
    if stype == 'POST':
        url = 'http://www.nfl.com/schedules/%d/%s' % (year,stype)
    else:
        url = 'http://www.nfl.com/schedules/%d/%s%s' % (year,stype,str(week))

    #Go to URL
    page = scraper.go(url)

    #Get list of div tags where 'class' = 'schedules-list-content'
    divs = page.find_all('div',{'class':'schedules-list-content'})
    #Appends every game's gameID to list in dictionary from URL
    for div in divs:
        gameIDs[stype].append(div['data-gameid'])
        url = 'http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json' % (div['data-gameid'],div['data-gameid'])
        urllib.request.urlretrieve(url, 'game_data/'+div['data-gameid']+'.json')


#Loop through NFL years
for year in years:
    scrape_data(year, 'POST')
    #Loop through REG season weeks each year
    for week in weeks:
        scrape_data(year, 'REG', week)

f.write(json.dumps(gameIDs))