"""
Course: cmps 4883
Assignemt: A03
Date: 2/13/19
Github username: JakobLopez
Repo url: https://github.com/JakobLopez/4883-SWTools-Lopez
Name: Jakob Lopez
Description: 
    If you do NOT  files.txt, RUN process_files.py.
    This program reads from a file called files.txt, which
    contains the file path to every game's data (./game_data/some_gameid.json).
    It creates 2 data structures: player_info.json and team_info.json.
    If you do not already have files, then uncomment the function calls
    writePlayerInfo and writeTeamInfo. These functions create the data structures,
    which makes the execution of the program faster when looking for stats.
    Functions read from these data structures to determine stats such as: finding
    the player who played for the most teams, who kicked longest field goal, etc...
    The output is written to screen and was saved to file from command line.
"""
import json
import os,sys
import pprint as pp
from process_files import openFileJson

"""
Name: getSeason
Description: 
    Computes NFL season year
    E.G. The superbowl is in year 2019 but in season 2018 
Params:
    fname - gameid
Returns:
    NFL season
"""
def getSeason(fname):
    #Seperate gameid from extension
    gameid,ext = os.path.basename(fname).split('.')

    #Year is first 4 characters
    year = int(gameid[:4])
    #Month is next 2 characters
    month = int(gameid[4:6])

    #If Jan. or Feb., then season is of previous year
    if month == 1 or month == 2:
        year = year - 1
       
    return year

"""
Name: writePlayerInfo
Description: 
    Stores all player information in a dictionary.
    Dictionary is written to json file to speed up execution
    If 1st time running program, this must be ran to create json file with information
Params:
    none
Returns:
    none
"""
def writePlayerInfo():
    #Empty dictionary
    players = {}

    #Opens a file for writing
    g = open("player_info.json","w")
    
    #Opens file containing file paths from game_data
    with open('files.txt') as f:
        #Read every file path (for every game)
        for line in f:
            #Truncates empty character at end of line
            line = line[:27]

            #Gets file data
            data = openFileJson(line)
            
            #Old season
            oldseason = 2009
            #Get current season year
            year = getSeason(line)
            newseason = False
            #If new season
            if oldseason != year:
                newseason = True
                oldseason = year

            # pull out the game id and game data
            for gameid,gamedata in data.items():
                if gameid != 'nextupdate':
                    # go straight for the drives
                    for driveid,drivedata in gamedata['drives'].items():
                        if driveid != 'crntdrv':
                            #For every play
                            for playid,playdata in drivedata['plays'].items():
                                #For every player in the play
                                for playerid, playerdata in playdata['players'].items():
                                    #For stats in player during play
                                    for info in playerdata:
                                        #Ignore when playerid is 0
                                        if playerid != '0':
                                            #If player is not in dictionary
                                            if playerid not in players:
                                                #Make player-id a key and empty ditionary as value
                                                players[playerid] = {}
                                                #Add name 
                                                players[playerid]['Name'] = info['playerName'] 
                                                #Add team they are playing for
                                                players[playerid]['Teams'] = []
                                                players[playerid]['Teams'].append(info['clubcode']) 
                                                #Create key with empty dictionary as value
                                                players[playerid]['TeamInfo'] = {}
                                                #Create list for current year
                                                players[playerid]['TeamInfo'][year] = []
                                                #Add team they are playing for in current year
                                                players[playerid]['TeamInfo'][year].append(info['clubcode']) 
                                                #Creating empty dictionaries    
                                                players[playerid]['RushYards'] = []
                                                players[playerid]['PassYards'] = []
                                                players[playerid]['MadeFieldGoals'] = []
                                                #Create a count initialized to 0
                                                players[playerid]['MissedFieldGoals'] = 0
                                                players[playerid]['DroppedPasses'] = 0
                                                #If player rushed
                                                if info['statId'] == 10:
                                                    players[playerid]['RushYards'].append(info['yards'])
                                                #If player passed the ball
                                                if info['statId'] == 15:
                                                    players[playerid]['PassYards'].append(info['yards'])
                                                #If player made a field goal
                                                if info['statId'] == 70:
                                                    players[playerid]['MadeFieldGoals'].append(info['yards'])
                                                #If player missed a field goal
                                                if info['statId'] == 69:
                                                    players[playerid]['MissedFieldGoals'] = players[playerid]['MissedFieldGoals'] + 1
                                                #If player dropped a passed ball
                                                if info['statId'] == 115 and 'pass' in playdata['desc'] and 'dropped' in playdata['desc']:
                                                    players[playerid]['DroppedPasses'] = players[playerid]['DroppedPasses'] + 1
                                            #If player already in dicitionary    
                                            else:   
                                                #If player is playing for new team
                                                if info['clubcode'] not in players[playerid]['Teams']:
                                                    players[playerid]['Teams'].append(info['clubcode'])
                                                #If its a new season create list for season year
                                                if newseason:
                                                    players[playerid]['TeamInfo'][year] = []  
                                                #If playing for new team in same year
                                                if info['clubcode'] not in players[playerid]['TeamInfo'][year]:               
                                                    players[playerid]['TeamInfo'][year].append(info['clubcode'])
                                                #If player rushed
                                                if info['statId'] == 10:
                                                    players[playerid]['RushYards'].append(info['yards'])
                                                #If player passed the ball
                                                if info['statId'] == 15:
                                                    players[playerid]['PassYards'].append(info['yards'])
                                                #If player made a field goal
                                                if info['statId'] == 70:
                                                    players[playerid]['MadeFieldGoals'].append(info['yards'])
                                                #If player missed a field goal
                                                if info['statId'] == 69:
                                                    players[playerid]['MissedFieldGoals'] = players[playerid]['MissedFieldGoals'] + 1
                                                #If player dropped a passed ball
                                                if info['statId'] == 115 and 'pass' in playdata['desc'] and 'dropped' in playdata['desc']:
                                                    players[playerid]['DroppedPasses'] = players[playerid]['DroppedPasses'] + 1
     #Writes all game IDs
    g.write(json.dumps(players))

"""
Name: writeTeamInfo
Description: 
    Stores all team information in a dictionary.
    Dictionary is written to json file to speed up execution
    If 1st time running program, this must be ran to create json file with information
Params:
    none
Returns:
    none
"""
def writeTeamInfo():
    teams = {}

    #Opens a file for writing
    g = open("team_info.json","w")

    #Corrected team abbreviations
    abbr = openFileJson('./team_abbrev.json')

    #Opens file containing file paths from game_data
    with open('files.txt') as f:
        #Read every file path
        for line in f:
            #Truncates empty character at end of line
            line = line[:27]

            #Gets file data
            data = openFileJson(line)

            # pull out the game id and game data
            for gameid,gamedata in data.items():
                if gameid != 'nextupdate':        
                    #Get home and away teams 
                    home = gamedata['home']['abbr']
                    away = gamedata['away']['abbr'] 
                    #Check for correct abbreviation  
                    home = abbr[home]                
                    away = abbr[away]

                    #If home team not in dictionary, add them & initialize values
                    if home not in teams:
                        teams[home] = {}
                        teams[home]['penalties'] = 0
                        teams[home]['penalty yards'] = 0
                        teams[home]['wins'] = 0
                        teams[home]['losses'] = 0
                    #Add to penalty counters of home team
                    teams[home]['penalties'] = teams[home]['penalties'] + gamedata['home']['stats']['team']['pen']
                    teams[home]['penalty yards'] = teams[home]['penalty yards'] + gamedata['home']['stats']['team']['penyds']
                    #If away team not in dictionary, add them & initialize values
                    if away not in teams:
                        teams[away] = {}
                        teams[away]['penalties'] = 0
                        teams[away]['penalty yards'] = 0
                        teams[away]['wins'] = 0
                        teams[away]['losses'] = 0
                    #Add to penalty counters of away team
                    teams[away]['penalties'] = teams[away]['penalties'] + gamedata['away']['stats']['team']['pen']
                    teams[away]['penalty yards'] = teams[away]['penalty yards'] + gamedata['away']['stats']['team']['penyds']

                    #Update counts for which teams won and loss
                    if gamedata['home']['score']['T'] > gamedata['away']['score']['T']:
                        teams[home]['wins'] = teams[home]['wins'] + 1
                        teams[away]['losses'] = teams[away]['losses'] + 1
                    elif gamedata['home']['score']['T'] < gamedata['away']['score']['T']:
                        teams[away]['wins'] = teams[away]['wins'] + 1
                        teams[home]['losses'] = teams[home]['losses'] + 1
     #Writes all game IDs
    g.write(json.dumps(teams))

"""
Name: getPlayersWithMostTeams
Description: 
    Finds player(s) who played for the most teams 
Params:
    none
Returns:
    List of tuples - each tuple has player name & number of teams played for
"""
def getPlayersWithMostTeams():
    #Empty list
    players = []
    #Open json with player info
    data = openFileJson('./player_info.json')

    #Get player-id with most teams
    max_key = max(data, key= lambda x: len(set(data[x]['Teams']))) 
    #Most number of teams a player has played for
    size = len(data[max_key]['Teams'])

    #For every player and their data
    for playerid,playerdata in data.items():
        #If they have played for the most number of teams
        if len(playerdata['Teams']) == size:
            #Pair their name and number of teams played for 
            tup = (playerdata['Name'],size)
            #And put in list
            players.append(tup)
    return players

"""
Name: getPlayersWithMostTeamsInSingleYear
Description: 
    Finds player(s) who played for the most teams in a single NFL season
Params:
    none
Returns:
    List of tuples - each tuple has player name & number of teams played for & year they played
"""
def getPlayersWithMostTeamsInSingleYear():
    #Empty list
    players = []
    #Open json with player info
    data = openFileJson('./player_info.json')

    #Set minimum size for teams played for in a year
    size = 1
    #For every player
    for playerid,playerdata in data.items():  
        #For every year they played         
        for year,yeardata in playerdata['TeamInfo'].items():
            #If they played for more teams than anyone else
            if len(yeardata) > size:
                #Update most number of teams played for
                size = len(yeardata)
                #Save their name, number of teams played for & in which year
                tup = (playerdata['Name'],size, year)
                players.append(tup)
    #Remove players that have played for less teams than the max
    players = list(filter(lambda x: x[1] == size, players))
    return players

"""
Name: getPlayerMostNegativeRush
Description: 
    Finds player(s) who rushed for the biggest loss in a play
Params:
    none
Returns:
    List of tuples - each tuple has player name & number of yards rushed
"""                  
def getPlayerMostNegativeRush():
    #Empty list
    players = []
    #Open json with player info
    data = openFileJson('./player_info.json')
    
    #Set maximum for negative yards rushed
    lowest = 0
    #For every player
    for playerid,playerdata in data.items():   
        #For every yard they rushed
        for yards in playerdata['RushYards']:
            #If current yard is less than current lowest
            if yards != None and yards <= lowest:
                #Update lowest yards rushed to current negative yards
                lowest = yards
                #Save player's name and yards rushed
                tup = (playerdata['Name'],lowest)
                players.append(tup)
    #Remove players who did not rush for the most negative yards
    players = list(filter(lambda x: x[1] == lowest, players))
    return players

"""
Name: getPlayerMostNegativeRushes
Description: 
    Finds player(s) who rushed for negative yards the most amount of times
Params:
    none
Returns:
    List of tuples - each tuple has player name & number of times they rushed negative yards 
"""   
def getPlayerMostNegativeRushes():
    #Empty dictionary
    players = {}
    #Open json with player info
    data = openFileJson('./player_info.json')
    
    #For every player
    for playerid,playerdata in data.items():   
        #Initialize every player in dictionary with 0 negative yards rushed
        players[playerid] = 0
        #For every yard they rushed
        for yards in playerdata['RushYards']:
            #If the current yard is negative
            if yards != None and yards < 0:
                #Increment their count in dictionary
                players[playerid] = players[playerid] + 1 

    #Get most number of negative yards rushed
    highest_count = players[max(players, key=players.get)]
    #Empty list
    player_list = []
    #For every player in dictionary
    for k in players:
        #If their count is equal to highest number of negative rushed yards
        if players[k] == highest_count:
            #Save their name and number of negative yards rushed
            tup = (data[k]['Name'], players[k])
            player_list.append(tup)       
    return player_list

"""
Name: getPlayerMostNegativePasses
Description: 
    Finds player(s) who passed for negative yards the most
Params:
    none
Returns:
    List of tuples - each tuple has player name & number of times they rushed negative yards 
"""  
def getPlayerMostNegativePasses():
    #Empty dictionary
    players = {}
    #Open json with player info
    data = openFileJson('./player_info.json')
    
    #For every player
    for playerid,playerdata in data.items():
        #Initialize count to 0 
        players[playerid] = 0  
        #For every yard they passed
        for yards in playerdata['PassYards']:
            #If they passed for negative yards
            if yards != None and yards < 0:
                #Increment their count in dictionary
                players[playerid] = players[playerid] + 1 

    #Get most number of negative yards passed
    highest_count = players[max(players, key=players.get)]
    #Empty list
    player_list = []
    #For every player in dictionary
    for k in players:
        #If their count is equal to highest number of negative rushed passed
        if players[k] == highest_count:
            #Save their name and count
            tup = (data[k]['Name'], players[k])
            player_list.append(tup)
    return player_list

"""
Name: getTeamMostPenalties
Description: 
    Finds team(s) who has the most penalties
Params:
    none
Returns:
    List of tuples - each tuple has team name & number of penalties 
"""  
def getTeamMostPenalties():
    #Empty list
    team = []
    #Open json with team info
    data = openFileJson('./team_info.json')

    #Most amount of penalties out of all teams
    most = data[max(data, key= lambda x: data[x]['penalties'])]['penalties']

    #For every team
    for t, tdata in data.items():
        #If they have the most amount of penalties
        if tdata['penalties'] == most:
            #Save team & number of penalties
            tup = (t,most)
            team.append(tup)
    return team

"""
Name: getTeamMostPenaltyYards
Description: 
    Finds team(s) who has the most total penalty yards
Params:
    none
Returns:
    List of tuples - each tuple has team name & number of yards in penalties 
"""  
def getTeamMostPenaltyYards():
    #Empty list 
    team = []
    #Open json with team info
    data = openFileJson('./team_info.json')

    #Most amount of total penalty yards out of all the teams
    most = data[max(data, key= lambda x: data[x]['penalty yards'])]['penalty yards']

    #For every team
    for t, tdata in data.items():
        #If they have the most amount of penalty yards
        if tdata['penalty yards'] == most:
            #Save team & number of penalty yards
            tup = (t,most)
            team.append(tup)
    return team

"""
Name: getHighestWinLossRatio
Description: 
    Finds team(s) who has the best win/loss ratio
Params:
    none
Returns:
    List of tuples - each tuple has team name & win/loss ratio
"""  
def getHighestWinLossRatio():
    #Empty list
    teams = []
    #Open json with team info
    data = openFileJson('./team_info.json')

    #Team with best win/loss ratio
    max_key = max(data, key= lambda x: data[x]['wins']/data[x]['losses'])
    #Best win/loss ratio
    max_wlr = data[max_key]['wins'] / data[max_key]['losses']

    #For every team
    for t,tdata in data.items():
        #Compute win/loss ratio
        ratio = tdata['wins']/tdata['losses']
        #If ratio is the highest win/loss ratio
        if ratio == max_wlr:
            #Save team & ratio
            tup = (t,ratio)
            teams.append(tup)
    return teams

"""
Name: getWinLossRatio
Description: 
    Computes win/loss ratio for specific team
Params:
    team - the team who get their win/loss ratio computed
Returns:
    win/loss ratio
"""  
def getWinLossRatio(team):
    #Open json with team info
    data = openFileJson('./team_info.json')

    #Calculate ratio
    ratio = data[team]['wins']/data[team]['losses']
    return ratio

"""
Name: getPenalties
Description: 
    Gets number of penalties for a specific team
Params:
    team - team that gets number of penalties searched
Returns:
    number of penalties
"""  
def getPenalties(team):
    data = openFileJson('./team_info.json')

    pens = data[team]['penalties']
    return pens

"""
Name: getAvgNumPlays
Description: 
    Gets average number of plays in a game
Params:
    none
Returns:
    average number of plays
"""  
def getAvgNumPlays():
    #Initialize counters
    count = 0
    plays = 0

    #Opens file containing file paths from game_data
    with open('files.txt') as f:
        #Read every file path (for every game)
        for line in f:
            #Truncates empty character at end of line
            line = line[:27]

            #Gets file data
            data = openFileJson(line)
            #Increment number of games
            count = count + 1

            # pull out the game id and game data
            for gameid,gamedata in data.items():
                if gameid != 'nextupdate':
                    # go straight for the drives
                    for driveid,drivedata in gamedata['drives'].items():
                        if driveid != 'crntdrv':
                            #Adds number of plays in game to total
                            plays = plays + drivedata['numplays']
    #Return mean
    return round(plays/count)

"""
Name: getLongestFieldGoal
Description: 
    Finds player(s) with longest field goal
Params:
    none
Returns:
    List of tuples - each tuple has player name & yards of longest field goal
"""  
def getLongestFieldGoal():
    #Empty list
    players = []
    #Open json with player info
    data = openFileJson('./player_info.json')
    
    #Sets minimum distance for furthest field goal
    furthest = 0
    #For every player
    for player,playerdata in data.items():
        #For every yard they kicked a successful field goal
        for yard in playerdata['MadeFieldGoals']:
            #If current yard is greater than or equal to previous furthest field goal
            if yard and yard >= furthest:
                #Update furthest field goal
                furthest = yard
                #Save player name & yards of furthest field goal
                tup = (playerdata['Name'],furthest)
                players.append(tup)
    #Remove every player in list whose field goal is less than furthest
    players = list(filter(lambda x: x[1] == furthest, players))
    return players

"""
Name: getMostMadeFieldGoals
Description: 
    Finds player(s) with most made field goals
Params:
    none
Returns:
    List of tuples - each tuple has player name & number of successful field goals
"""  
def getMostMadeFieldGoals():
    #Empty list
    players = []
    #Open json with player info
    data = openFileJson('./player_info.json')

    #Set minimum number of field goals to find the most
    most = 0
    #For every player
    for player,playerdata in data.items():
        #If the number of made field goals is greater than or equal to previous most
        if len(playerdata['MadeFieldGoals']) >= most:
            #Update most number of field goals
            most = len(playerdata['MadeFieldGoals'])
            #Save player name & number of field goals made
            tup = (playerdata['Name'],most)
            players.append(tup)
    #Remove players from list who have less successful field goals than the most number of field goals made
    players = list(filter(lambda x: x[1] == most, players))
    return players

"""
Name: getMostMissedFieldGoals
Description: 
    Finds player(s) with most missed field goals
Params:
    none
Returns:
    List of tuples - each tuple has player name & number of failed field goals
"""  
def getMostMissedFieldGoals():
    #Empty list
    players = []
    #Open json with player info
    data = openFileJson('./player_info.json')

    #Most number of missed field goals
    max_val = data[max(data, key = lambda x: data[x]['MissedFieldGoals'])]['MissedFieldGoals']

    #For every player
    for player,playerdata in data.items():
        #If they missed as many field goals as the most missed
        if playerdata['MissedFieldGoals'] == max_val:
            #Save player name & field goals missed
            tup = (playerdata['Name'],max_val)
            players.append(tup)
    return players

"""
Name: getPlayerMostDroppedPasses
Description: 
    Finds player(s) with most dropped passes
Params:
    none
Returns:
    List of tuples - each tuple has player name & number of dropped passes
"""  
def getPlayerMostDroppedPasses():
    #Empty list
    players = []
    #Open json with player info
    data = openFileJson('./player_info.json')

    #Most number of dropped passes 
    max_val = data[max(data, key = lambda x: data[x]['DroppedPasses'])]['DroppedPasses']

    #For every player
    for player,playerdata in data.items():
        #If they dropped as many passes as the most dropped
        if playerdata['DroppedPasses'] == max_val:
            #Save player name and number of dropped passes
            tup = (playerdata['Name'],max_val)
            players.append(tup)
    return players
    
#RUN THESE WHEN RUNNING FOR FIRST TIME 
#Writes player info to JSON file
#writePlayerInfo()
#writeTeamInfo()

print('Name: Jakob Lopez')
print('Assignment: A03 - Nfl Stats ')
print('Date: February 12, 2019')
print()

print('=================================================================')
print('1. Find the player(s) that played for the most teams.')
players = getPlayersWithMostTeams()
for player in players:    
    print('%s played for %d teams' % (player[0], player[1]))
print('=================================================================') 
print()


print('=================================================================')
print('2. Find the player(s) that played for the most teams in a year.')
players = getPlayersWithMostTeamsInSingleYear()
for player in players:
    print('%s played for %d teams in %s' % (player[0], player[1], player[2]))
print('=================================================================')
print() 


print('=================================================================')
print('3. Find the player(s) that had the most yards rushed for a loss.')
players = getPlayerMostNegativeRush()
for player in players:
    print('%s had a rush of  %d yards' % (player[0], player[1]))
print('=================================================================') 
print()

print('=================================================================')
print('4. Find the player(s) that had the most rushes for a loss.')
players = getPlayerMostNegativeRushes()
for player in players:
    print('%s has rushed for negative yards %d times' % (player[0], player[1]))
print('=================================================================') 
print()

print('=================================================================')
print('5. Find the player(s) that had the most rushes for a loss.')
players = getPlayerMostNegativePasses()
for player in players:
    print('%s has passed for negative yards %d times' % (player[0], player[1]))
print('=================================================================') 
print()

print('=================================================================')
print('6. Find the team with the most penalties.')
teams = getTeamMostPenalties()
for team in teams:
    print('%s has a total of %d penalties' % (team[0], team[1]))
print('=================================================================') 
print()

print('=================================================================')
print('7. Find the team with the most yards in penalties.')
teams = getTeamMostPenaltyYards()
for team in teams:
    print('%s has a total of %d penalty yards' % (team[0], team[1]))
print('=================================================================') 
print()

print('=================================================================')
print('8. Find the correlation between most penalized teams and games won / lost.')
teams = getTeamMostPenalties()
for team in teams:
    ratio = getWinLossRatio(team[0])
    print('%s has the most penalties(%d) and a win/loss ratio of %f' % (team[0], team[1], ratio))
teams = getHighestWinLossRatio()
for team in teams:
    pens = getPenalties(team[0])
    print('%s has the best win/loss ratio(%f) and %d penalties' % (team[0], team[1], pens))
print('=================================================================') 
print()

print('=================================================================')
print('9. Average number of plays in a game.')
avg = getAvgNumPlays()
print('On average, there are %d plays in a game' % (avg))
print('=================================================================') 
print()

print('=================================================================')
print('10. Longest field goal.')
players = getLongestFieldGoal()
for player in players:
    print('%s kicked a successful field goal for %d yards' % (player[0],player[1]))
print('=================================================================') 
print()

print('=================================================================')
print('11. Longest field goal.')
players = getMostMadeFieldGoals()
for player in players:
    print('%s has kicked %d successful field goals' % (player[0],player[1]))
print('=================================================================') 
print()

print('=================================================================')
print('12. Most missed field goals.')
players = getMostMissedFieldGoals()
for player in players:
    print('%s has missed %d field goals' % (player[0],player[1]))
print('=================================================================') 
print()

print('=================================================================')
print('13. Most dropped passes')
players = getPlayerMostDroppedPasses()
for player in players:
    print('%s has dropped %d passes' % (player[0],player[1]))
print('=================================================================') 
print()
