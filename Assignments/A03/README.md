# How to run
    1. If you don't have game data files under game_data folder, run nfl_scrap.py
    2. If you don't have files.txt, run process_files.py
    3. If you don't have player_info.json or team_info.json, uncomment line 684 or 685 in calculate_stats.py and then run


## nfl_scrape.py  
If beautifulscraper not installed run ```pip install beautifulscraper``` <br>
This program gets game-ids from http://www.nfl.com/schedules for post(except pro bowl) and regular season games from 2009 to 2018.<br>
The game-ids are needed to access a JSON item that contains all game data, where the url is in the form  
http://www.nfl.com/liveupdate/game-center/game-id/game-id_gtd.json <br>
Beautifulscraper is used to grab html tag attributes such as the game-id. <br>
Urllib is used to grab the game data JSON objects and write them to a local folder called game_data. CREATE FOLDER BEFORE RUNNING <br>
Each saved JSON file is written under the form game-id.json.<br>
The game-ids are also saved to a dictionary and written to gameIDs.json with top keys being POST and REG to organize the data.<br>
Json is imported to dump the game-id dictionary to a file called gameIDs.json.<br>
  
### game_data - 
Not uploaded to GitHub. Create this folder before running nfl_scrape.py. Contains all JSON game data as files
 
### gameIds.json
Not uploaded to GitHub. File created from dictionary in nfl_scrape.py. Contains all game-ids for POST and REG seasons.

## process_files.py
Gets path to game data json files assuming that nfl_scrape.py has already executed and stored files in game_data folder. <br>
Write all paths to files.txt
Opens and returns data from a specified json file
Verifies if a file is json
Used to help calculate_stats.py run faster

### files.txt
Contains path to every game data json file under game_data folder

## calculate_stats.py
Uses files.txt to get player and team information so it can be saved as a data structure.<br>
Data structures only need to be created once, and makes the execution of finding stats faster.<br>
If player_info.json or team_info.json not present, uncomment code to write the data structures in line 684 or 685. <br>
Functions find specified stats and writes them to the screen.<br>
REMEMBER: these stats only consider years 2009 - 2018 post and regular season game, excluding pro bowl.


### player_info.json
Data structure created from calculate_stats.py. <br>
Contains information for every player.

### team_info.json
Data structure created from calculate_stats.py. <br>
Contains information for every team.

### results.txt
Stats found
