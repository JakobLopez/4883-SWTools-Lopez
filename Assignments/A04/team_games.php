<?php
//Contains login credentials for database;
require "credentials.php";

//Connect to mysql
$host = "localhost";             // because we are ON the server
$user = $USERNAME;        // user name

// Get username and password from slack
// The DB username and pass not the ones
// I sent you to log into the server.
$password = $PASSWORD;         // password 
$database = "nfl_data";              // database 
$mysqli = mysqli_connect($host, $user, $password, $database);

if (mysqli_connect_errno($mysqli)) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

// Helper function to run sql
require "query_function.php";

echo "<h3>Name: Jakob Lopez</h3>";
echo "<h3>Assignment: A04 - Nfl Stats</h3>";
echo "<h3>Date: March 1, 2019</h3>";


/******************************************************************************/
/*                  TOP 5 PLAYERS WHO PLAYED FOR THE MOST TEAMS               */
/******************************************************************************/

//Create table with headers
echo "<table border=1px width=50%>
<caption><strong>TOP 5 PLAYERS WHO PLAYED FOR THE MOST TEAMS</strong></caption>
<tr>
<th align='left'>Player ID</th>
<th align='left'>Name</th>
<th align='left'># Teams</th>
</tr>";

//Query
$sql = "SELECT id, name, COUNT(DISTINCT club) as `# Teams`
        FROM `players`
        GROUP BY id
        ORDER BY `# Teams` DESC
        LIMIT 10";

//Runs the query
$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters

//If query was successful
if($response['success']){
    //print each row to table
    foreach($response['result'] as $row){
        echo "\t<tr><td >".
        $row['id']."</td><td>".
        $row['name']."</td><td>".
        $row['# Teams'].
        "</td></tr>\n";
    }
    //End table
    echo "</table> \n";
    echo "<br>";
}


/******************************************************************************/
/*            TOP 5 PLAYERS WITH MOST TOTAL SEASONAL RUSHING YARDS           */
/******************************************************************************/

//Create a table with headers
echo "<table border=1px width=50%>
<caption><strong>TOP 5 PLAYERS WITH MOST TOTAL SEASONAL RUSHING YARDS</strong></caption>
<tr>
<th align='left'>Player ID</th>
<th align='left'>Name</th>
<th align='left'>Season</th>
<th align='left'># Yards</th>
</tr>";

//Query
$sql = "SELECT DISTINCT ps.playerid,p.name, ps.season, ps.`# Yards`
    FROM (SELECT playerid, statid, season, SUM(yards) as `# Yards`
        FROM `players_stats`
        WHERE statid = 10 
        GROUP BY playerid, season) AS ps
    INNER JOIN (SELECT id,name from `players`) AS p ON ps.playerid=p.id
    ORDER BY ps.`# Yards` DESC
    LIMIT 5";
//Run query
$response = runQuery($mysqli, $sql);

//If query was successful
if($response['success']){
    //print each row to table
    foreach($response['result'] as $row){
        echo "\t<tr><td>".
        $row['playerid']."</td><td>".
        $row['name']."</td><td>".
        $row['season']."</td><td>".
        $row['# Yards'].
        "</td></tr>\n";
    }
    //End table
    echo "</table> \n";
    echo "<br>";
}


/******************************************************************************/
/*            TOP 5 PLAYERS WITH LEAST TOTAL SEASONAL PASSING YARDS           */
/******************************************************************************/

//Create a table with headers
echo "<table border=1px width=50%>
<caption><strong>TOP 5 PLAYERS WITH LEAST TOTAL SEASONAL PASSING YARDS</strong></caption>
<tr>
<th align='left'>Player ID</th>
<th align='left'>Name</th>
<th align='left'>Season</th>
<th align='left'># Yards</th>
</tr>";

//Query
$sql = "SELECT DISTINCT ps.playerid,p.name,ps.season, ps.`# Yards`
    FROM (SELECT playerid, statid,season, SUM(yards) as `# Yards`
        FROM `players_stats`
        WHERE statid = 15 
        GROUP BY playerid, season) AS ps
    INNER JOIN (SELECT id,name from `players`) AS p ON ps.playerid=p.id
    ORDER BY `# Yards` ASC
    LIMIT 5";
//Run query
$response = runQuery($mysqli, $sql);

//If query was successful
if($response['success']){
    //Print each row to table
    foreach($response['result'] as $row){
        echo "\t<tr><td>".
        $row['playerid']."</td><td>".
        $row['name']."</td><td>".
        $row['season']."</td><td>".
        $row['# Yards'].
        "</td></tr>\n";
    }
    //End table
    echo "</table> \n";
    echo "<br>";
}

/******************************************************************************/
/*      TOP 5 PLAYERS WITH MOST NEGATIVE RUSHING YARDS PER SEASON             */
/******************************************************************************/

//Create table with headers
echo "<table border=1px width=50%>
<caption><strong>TOP 5 PLAYERS WITH MOST NEGATIVE RUSHING YARDS PER SEASON</strong></caption>
<tr>
<th align='left'>Player ID</th>
<th align='left'>Name</th>
<th align='left'># Negative Rushes</th>
</tr>";

//Query
$sql = "SELECT DISTINCT ps.playerid,p.name, ps.`# Negative Rushes`
    FROM (SELECT playerid, statid, season, COUNT(yards) as `# Negative Rushes`
        FROM `players_stats`
        WHERE statid = 10 AND yards < 0
        GROUP BY playerid
        ) AS ps
    INNER JOIN (SELECT id,name from `players`) AS p ON ps.playerid=p.id
    ORDER BY `# Negative Rushes` DESC
    LIMIT 5";
//Run query
$response = runQuery($mysqli, $sql);

//If query was a success
if($response['success']){
    //print each row to table
    foreach($response['result'] as $row){
        echo "\t<tr><td>".
        $row['playerid']."</td><td>".
        $row['name']."</td><td>".
        $row['# Negative Rushes'].
        "</td></tr>\n";
    }
    //End table
    echo "</table> \n";
    echo "<br>";
}

/******************************************************************************/
/*                  TOP 5 TEAMS WITH THE MOST PENALTIES                       */
/******************************************************************************/

//Create a table with headers
echo "<table border=1px width=50%>
<caption><strong>TOP 5 TEAMS WITH THE MOST PENALTIES</strong></caption>
<tr>
<th align='left'>Club</th>
<th align='left'># Penalties</th>
</tr>";

//Query
$sql = "SELECT club, SUM(pen) as pen
    FROM `game_totals`
    GROUP BY club
    ORDER BY pen DESC
    LIMIT 5";
//Run query
$response = runQuery($mysqli, $sql);

//If query was a success
if($response['success']){
    //print each row to table
    foreach($response['result'] as $row){
        echo "\t<tr><td>".
        $row['club']."</td><td>".
        $row['pen']."</td>".
        "</tr>\n";
    }
    //End table
    echo "</table> \n";
    echo "<br>";
}

/******************************************************************************/
/*                  AVERAGE NUMBER OF PENALTIES PER SEASON                    */
/******************************************************************************/

//Create a table with headers
echo "<table border=1px width=50%>
<caption><strong>AVERAGE NUMBER OF PENALTIES PER SEASON</strong></caption>
<tr>
<th align='left'>Season</th>
<th align='left'>Total Penalties</th>
<th align='left'>Average Penalties</th>
</tr>";

//Query
$sql = "SELECT season, SUM(pen) AS `Total Penalties`, SUM(pen)/count(DISTINCT gameid) as `Avg Penalties`
    FROM `game_totals`
    GROUP BY season
    ORDER BY `Avg Penalties` DESC";
//Run query
$response = runQuery($mysqli, $sql);

//If query was successful
if($response['success']){
    //print each row to table
    foreach($response['result'] as $row){
        echo "\t<tr><td>".
        $row['season']."</td><td>".
        $row['Total Penalties']."</td><td>".
        $row['Avg Penalties']."</td>".
        "</tr>\n";
    }
    //End table
    echo "</table> \n";
    echo "<br>";
}

/******************************************************************************/
/*            TEAM WITH THE LEAST AMOUNT OF PENALTIES PER YEAR                */
/******************************************************************************/

//Create table with headers
echo "<table border=1px width=50%>
<caption><strong>TEAM WITH THE LEAST AMOUNT OF PENALTIES PER YEAR</strong></caption>
<tr>
<th align='left'>Season</th>
<th align='left'>Club</th>
<th align='left'>Average Plays</th>
</tr>";

//Query
$sql = "SELECT club, season, COUNT(playid)/COUNT(DISTINCT gameid) AS `Avg Plays`
    FROM `players_stats` 
    GROUP BY club, season
    ORDER BY `Avg Plays` ASC";
//run query
$response = runQuery($mysqli, $sql);

//Empty array
$stats = []; 
//If query successful
if($response['success']){
    //Add each row to the empty array
    foreach($response['result'] as $row){
        //Season from row
        $season = $row['season']; 
        //Club from row
        $club = $row['club'];
        //Avg from row
        $avg = $row['Avg Plays'];

        //If season is not already in array
        if(!array_key_exists($season,$stats)){
            //Add it as a key with an empty array as its value
            $stats[$season] = [];
        }
        //If club is not in season
        if(!array_key_exists($club,$stats[$season])){
            //Add it as a key with an empty array its value
            $stats[$season][$club] = [];
        }
        //Add avg to club's seasonal avg array
        $stats[$season][$club]['Avg'] = $avg;
    }
}

//Empty array
$avgs = [];
//Loop through years associative array $stats
foreach($stats as $year => $yearly_stat){
    //Find minimum average per year
    $min = min(array_column($stats[$year], 'Avg'));

    //For every team
    foreach($yearly_stat as $team => $avg)
    {
        //If team's average is the minimum average for the year
        if($avg['Avg'] == $min){
            //Add the year, team and average to array
            $avgs[$year][$team] = $avg['Avg'];
        }
    }
}

//Alphabetize teams
ksort($avgs);
//Loop through years in associative array $avgs
foreach($avgs as $year => $yearly_stat){
    //Loop through teams
    foreach($yearly_stat as $team => $avg)
    {
        //Output year, team and their avg to table
        echo "\t<tr><td>".
        $year."</td><td>".
        $team."</td><td>".
        $avg."</td>".
        "</tr>\n";
    }
}
//End table
echo "</table> \n";
echo "<br>";


/******************************************************************************/
/*          TOP 5 PLAYERS WITH FIELD GOALS OVER 40 YARDS                      */
/******************************************************************************/

//Create table with headers
echo "<table border=1px width=50%>
<caption><strong>TOP 5 PLAYERS WITH FIELD GOALS OVER 40 YARDS</strong></caption>
<tr>
<th align='left'>Player ID</th>
<th align='left'>Name</th>
<th align='left'>Season</th>
<th align='left'>Yards</th>
</tr>";

//Query
$sql = "SELECT DISTINCT ps.playerid,p.name, ps.season ,ps.yards
    FROM (SELECT playerid,season,yards
        FROM `players_stats`
        WHERE statid = 70 AND yards > 40
        ) AS ps
    INNER JOIN (SELECT id,name from `players`) AS p ON ps.playerid=p.id
    ORDER BY ps.yards DESC
    LIMIT 5";
//Run query
$response = runQuery($mysqli, $sql);

//If query successful
if($response['success']){
    //Print each row to table
    foreach($response['result'] as $row){
        echo "\t<tr><td>".
        $row['playerid']."</td><td>".
        $row['name']."</td><td>".
        $row['season']."</td><td>".
        $row['yards']."</td>".
        "</tr>\n";
    }
    //End table
    echo "</table> \n";
    echo "<br>";
}

/******************************************************************************/
/*          TOP 5 PLAYERS WITH SHORTEST AVG FIELD GOAL LENGTH                 */
/******************************************************************************/

//Create table with headers
echo "<table border=1px width=50%>
<caption><strong>TOP 5 PLAYERS WITH SHORTEST AVG FIELD GOAL LENGTH</strong></caption>
<tr>
<th align='left'>Player ID</th>
<th align='left'>Name</th>
<th align='left'>Average Yards</th>
</tr>";

//Query
$sql = "SELECT DISTINCT ps.playerid,p.name ,ps.`Avg Yards`
    FROM (SELECT playerid, SUM(yards)/COUNT(statid) as `Avg Yards`
        FROM `players_stats`
        WHERE statid = 70 
        GROUP BY playerid
        ) AS ps
    INNER JOIN (SELECT id,name from `players`) AS p ON ps.playerid=p.id
    ORDER BY ps.`Avg Yards` ASC
    LIMIT 5";
//Run query
$response = runQuery($mysqli, $sql);

//If query successful
if($response['success']){
    //Print each row to table
    foreach($response['result'] as $row){
        echo "\t<tr><td>".
        $row['playerid']."</td><td>".
        $row['name']."</td><td>".
        $row['Avg Yards']."</td>".
        "</tr>\n";
    }
    //End table
    echo "</table> \n";
    echo "<br>";
}

/******************************************************************************/
/*                        RANK NFL BY WIN:LOSS RATIO                          */
/******************************************************************************/

//Create table with headers
echo "<table border=1px width=50%>
<caption><strong>RANK NFL BY WIN:LOSS RATIO</strong></caption>
<tr>
<th align='left'>Club</th>
<th align='left'>Win Loss Ratio</th>
</tr>";

//Query
$sql = "SELECT club, 
        COUNT(IF(wonloss LIKE 'won',1,null)) as wins,
        COUNT(IF(wonloss LIKE 'loss',1,null)) as losses
    FROM `game_totals`
    GROUP BY club";
//Run query
$response = runQuery($mysqli, $sql);

//Empty array
$stats = [];
//If query successful
if($response['success']){
    //Add each row to array
    foreach($response['result'] as $row){
        //Club in row
        $club = $row['club'];
        //Wins in row
        $wins = $row['wins'];
        //losses in row
        $losses = $row['losses'];

        //If club is not in associative array $stats
        if(!array_key_exists($club,$stats)){
            //Add them with empty list as its value
            $stats[$club] = [];
        }
        //Add # number of wins to club
        $stats[$club]['wins'] = $wins;
        //Add # of losses to club
        $stats[$club]['losses'] = $losses;
    }
}

//Empty array
$ratio = [];
//Loop through every team in associative array $stats
foreach($stats as $team => $team_data){
    //Calculate win loss ratio 
    //Store in associate array $ratio
    $ratio[$team] = ($team_data['wins'] / $team_data['losses']);
}

//Sort win loss ratio from worst to best
asort($ratio);
//Loop through every team in associate array $ratio
foreach($ratio as $team => $data){
    //Output team and ratio to table
    echo "\t<tr><td>".
    $team."</td><td>".
    $data."</td>".
    "</tr>\n";
}
//End table
echo "</table> \n";
echo "<br>";

/******************************************************************************/
/*                        TOP 5 MOST COMMON NFL LAST NAMES                    */
/******************************************************************************/

//Create table with headers
echo "<table border=1px width=50%>
<caption><strong>TOP 5 MOST COMMON NFL LAST NAMES</strong></caption>
<tr>
<th align='left'>Name</th>
<th align='left'>Count</th>
</tr>";

//Query
$sql = "SELECT DISTINCT id, name
    FROM `players`";
//Run query
$response = runQuery($mysqli, $sql);

//empty array
$stats = [];
//If query successful
if($response['success']){
    //Add each row to array 
    foreach($response['result'] as $row){
        //Name in row
        $name = $row['name'];
        //Seperate name on "."
        $names = explode(".", $name);

        //names[1] is the last name of player
        //If last name is not in array
        if(!array_key_exists($names[1],$stats)){
            //Add it to array with value 0
            $stats[$names[1]] = 0;
        }
        //Increment counter for last name
        $stats[$names[1]] = $stats[$names[1]] + 1;
    }
}

//Sort values from highest to lowest
arsort($stats);
//Get the top five names
$top_five = array_slice($stats, 0, 5, true);

//Loop through names in associative array $top_five
foreach($top_five as $name => $count){
    //Output name and count to table
    echo "\t<tr><td>".
    $name."</td><td>".
    $count."</td>".
    "</tr>\n";
}
//End table
echo "</table>";
