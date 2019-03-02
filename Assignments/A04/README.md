## Required
```team_games.php``` ASSUMES you have a file called ```credentials.php``` containing username and password for the database as: $USERNAME, $PASSWORD
## How to View Code
http://cs2.mwsu.edu/~jlopez/software_tools/team_games.php
## .vscode
  - contains sftp.json
    - has credentials to connect to database
## team_games.php
  - This is the main program
  - It queries data from cs2 database
  - Uses queries to find: 
    - top 5 players who played for the most teams
    - top 5 players with most total seasonal rushing yards 
    - top 5 players with least total seasonal passing yards
    - top 5 players with most negative rushing yards per season
    - top 5 teams with the most penalties
    - average number of penalties per season
    - team with the least amount of penalties per year
    - top 5 players with field goals over 40 yards 
    - top 5 players with shortest avg field goal length
    - rank NFL by win:loss ratio 
    - top 5 most common NFL last names
## query_function.php
  - Helper function for team_games.php
  - Runs an sql query and returns data in associative array
