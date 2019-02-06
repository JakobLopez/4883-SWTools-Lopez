This program gets game-ids from http://www.nfl.com/schedules for post and regular season games from 2009 to 2018. The game-ids
are needed to access a JSON item that contains all game data, where the url is in the form  
http://www.nfl.com/liveupdate/game-center/game-id/game-id_gtd.json

Beautifulscraper is used to grab html tag attributes such as the game-id. Urllib is used to grab the game data JSON objects
and write them to a local folder called game_data. Each saved JSON file is written under the form game-id.json.

The game-ids are also saved to a dictionary with top keys being POST and REG to organize the data. Json is imported to dump the 
game-id dictionary to a file called gameIDs.json.
