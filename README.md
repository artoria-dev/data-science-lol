(This README is still WIP)

3 a.m. productions presents:

# Data Science Project On League Of Legends

***

## Table of Content

- [Disclaimer](#disclaimer)
- [Project Object](#project-object)
- [Acquiring Data](#acquiring-data)
- [The Match Data](#the-match-data)
- [The Actual Match Data I Was Able To Acquire](#the-actual-match-data-i-was-able-to-acquire)
- [Why My Data Could Be Biased](#why-my-data-could-be-biased)
- [Data Cleaning](#data-cleaning)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Feature Engineering](#feature-engineering)
- [Dealing With Multicollinearity](#dealing-with-multicollinearity)
- [Building Classifier Models](#building-classifier-models)
- [Evaluation](#evaluation)
- [Testing](#testing)

***

## Disclaimer

This project was a uni assignment.

All information given are up-to-date as of June 2022.

Feel free to use this project as a guide or for your own assignment in case you are too 'busy'.

Please note, I wrote this README *while* working on this project, which is why I might miss some preliminary considerations for later chapters.

Only 1 animal (me) was harmed during the realisation of this project.

In case you wish to contact me for whatever reason, please use discord and find me by my tag (Artoria#8809).

## Project Object

Main target for this project will be able to predict the outcome of a game based on in-game values at the 15-minute mark.
As bonus, I will try to determine the most influential factors in League of Legends in order to win a game.

## Acquiring Data

I have two options on acquiring my data to use.

```mermaid
  flowchart LR;
      Getting-data-->Use-premade-data;
      Getting-data-->Acquire-own-data;
      Use-premade-data-->Use-data;
      Acquire-own-data-->Use-data;
```

Using pre-made data surely saves a lot of time. Unfortunately League Of Legends changes a lot within a short amount of time.
Hence, pre-made data might not be up-to-date which is why I will use my own data.
Luckily, [Riot Games](https://developer.riotgames.com/apis) offers an API with lots of different endpoints I can use and even a [documentation](https://riot-api-libraries.readthedocs.io/en/latest/collectingdata.html) on collecting data.

The actual game data for a game can be read via Riot Game's '[Match-V5](https://developer.riotgames.com/apis#match-v5)' (specifically, /lol/match/v5/matches/{matchId}) endpoint.
Since I am trying to read the data of a game at the 15-minute mark, I will have to use the '/lol/match/v5/matches/{matchId}/timeline'-endpoint.
Both require the corresponding game id as input.

The game id can be acquired by reading a player's match history.
I can do that by using the same endpoint (Match-V5, specifically '/lol/match/v5/matches/by-puuid/{puuid}/ids') as mentioned before.
This does require a player's PUUID (Player Universally Unique Identifiers) which is, according to an [article](https://www.riotgames.com/en/DevRel/player-universally-unique-identifiers-and-a-new-security-layer) posted on [riotgames.com](https://www.riotgames.com/en), a unique and consistent identifier across regions, nations and games.

Now, the last step (actually the first, since I for some reason started this list the other way around..) is getting a player's PUUID.
I can get that by using the '[Summoner-V4](https://developer.riotgames.com/apis#summoner-v4)' (specifically, /lol/summoner/v4/summoners/by-name/{summonerName}) by entering a player's summoner name and their region.

    Sidenote:
    There are different regions players can play on, such a north american, europe west or asia.
    The summoner name represents the player's nickname which will be displayed in the game.

Great. Now that I know how to get the data I can get it. Or do I?

Unfortunately, Riot Games limited the API access rates to:

- 20 requests every 1 seconds(s)
- 100 requests every 2 minutes(s)

Since I am aiming for a data set including up to 100k (one-hundred thousand) matches, I would have my script running for 33,3 hours.
Sadly, Riot Games API keys are only valid for 24 hours.
Hence, I will have to reduce my data to around 72k (seventy-two thousand) entries (you can do the math by yourself, who am I to note down literally everything is this README).

The next issues will be getting the right amount of PUUIDs and an even distribution of the player's elo.

    Sidenote:
    A player's 'elo' determines a player's skill.
    Has a player a higher elo than average they are better than the average League Of Legends player.

Since I want my solution to be able to predict the outcome of the *majority* of the games, I will my need data to represent the rank distribution.

Surely I could only use data from the average League of Legends player, but where's the fun in that?

League of Legends rank distribution (according to [League of Graphs](https://www.leagueofgraphs.com/rankings/rank-distribution) as of June 2022) is as follows:

![rank-distribution](readme-files/rank_distribution.png)

That means my data *should* consist of the following amount of games per elo:

| Rank | Challenger | Grandmaster | Master | Diamond | Platinum | Gold | Silver | Bronze | Iron | **Total** |
|------|------------|-------------|--------|---------|----------|------|--------|--------|------|-----------|
| %    | 1          | 1           | 1      | 2       | 9        | 23   | 33     | 25     | 5    | **100**   |

Note that this is not perfect rounding, but now I can use data from Challenger, Grandmaster and Master player aswell.

If I used the same amount of games for e.g. 1 Challenger player and 33 Silver player for the entire list, I would end up with 720 matches per player.
That is a huge number considering Riot Game's miserable transparency for player's match history.
In order to reduce that number, I will have to increase the amount of player I am querying relative to their percentage as seen in the table above.

That results in:

| Rank            | Challenger | Grandmaster | Master | Diamond | Platinum | Gold   | Silver | Bronze | Iron  |
|-----------------|------------|-------------|--------|---------|----------|--------|--------|--------|-------|
| Players Tracked | 4          | 4           | 4      | 8       | 36       | 92     | 132    | 100    | 20    |
| Games Tracked   | 720        | 720         | 720    | 1.440   | 6.480    | 16.560 | 23.760 | 18.000 | 3.600 |

and reducing the original 720 matches per player down to 180.

That is a lot of player to query.. Unfortunately Riot Game's match history endpoint got a maximum of 100 matches per player.
Thats means I have to reduce the matches per player even more and increase the number of player to query.. yay.

That results in:

| Rank            | Challenger | Grandmaster | Master | Diamond | Platinum | Gold   | Silver | Bronze | Iron  | **Total**  |
|-----------------|------------|-------------|--------|---------|----------|--------|--------|--------|-------|------------|
| Players Tracked | 8          | 8           | 8      | 14      | 65       | 166    | 238    | 180    | 36    | **723**    |
| Games Tracked   | 800        | 800         | 800    | 1.400   | 6.500    | 16.600 | 23.800 | 18.000 | 3.600 | **72.300** |

This surpasses the 72k (seventy-two thousand) matches, but I can fix that by reducing the amount of silver player tracked by 2 and the amount of bronze player tracked by 1.

Resulting in:

| Rank            | Challenger | Grandmaster | Master | Diamond | Platinum | Gold   | Silver | Bronze | Iron  | **Total**  |
|-----------------|------------|-------------|--------|---------|----------|--------|--------|--------|-------|------------|
| Players Tracked | 8          | 8           | 8      | 14      | 65       | 166    | 236    | 179    | 36    | **720**    |
| Games Tracked   | 800        | 800         | 800    | 1.400   | 6.500    | 16.600 | 23.600 | 17.900 | 3.600 | **72.000** |
(Don't worry, that's the last table for this section)

Here is the final graph which surely is not 100 % in compliance with the rank distribution as seen in the picture above, but it is the closest I can get:

![games-tracked-per-elo-adjusted](readme-files/games-tracked-per-elo-adjusted.png)

Since I cannot divide 8 player by 11 different regions, and I can only test it on my own region, I will only use data from EU West (EUW1).

The very last issue to handle is getting such an amount of player. Remember, each has to have at least 100 ranked games played.
I could grab myself a few player, iterate over their matches played and read the other 9 player in their game and iterate over their games aswell.
That sounds like a nice way to do. Sadly I cannot ensure that every player has more than 100 ranked games played when doing it this way.
Therefore, I will grab all player by hand. Yes, all 720.

    Sidenote:
    There are different game modes player can play in League of Legends.
    I will focus on ranked games.
    That will reduce the number of unconventionally playstyles and ensures healthy stats as people tend to play more serious.

In case one is too lazy to gather all the summoner names by hand, Riot Games offers the [LEAGUE-V4-endpoint](https://developer.riotgames.com/apis#league-v4) to get various player by elo.
The script for this could look like this:

    import requests
    
    with open('summoner-names.txt', 'a') as f:
        response = requests.get(
            'https://euw1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/SILVER/III?page=5&api_key=YOUR-RIOT-GAMES-API-KEY')
        res = response.json()
        for x in range(300):
            try:
                f.write(res[x]['summonerName'] + '\n')
            except:
                pass

***To summarise:***

- I will use my own data
- I will get the data with Riot Game's API using different endpoints
- If my calculations are correct, I will end up with around 72000 match entries in my data set
- I will use a different amount of player per elo according to the rank distribution
- I will use 100 games per player out of 720 player
- I will gather all the player/summoner names to track by myself

Great. I need a coffee after that section..

***

## The Match Data

This section should be added up the prior one as it is part of acquiring data, but I decided to split them since this section is more about designing the data frame out of the Riot Game's API and less mathematically.

The average game duration of the region EUW (including the games being surrendered) for all tiers is 28,8 minutes repetend (according to [League of Graphs](https://www.leagueofgraphs.com/de/rankings/game-durations/euw) as of June 2022).

When querying a match with a timeline with the average game duration, the returning JSON file includes about 35k (thirty-five thousand) lines which would be too much to display for this README.
Therefore, I will display a simplified 'pseudo'-version of it for you to be able to follow up:

    metadata
        match id
        participants
    info
        event
            event type
            timestamp
            additional event info
        stats
            player 1
            player 2
            ...
            player 10
            timestamp
        event
            event type
            timestamp
            additional event info
        stats
            player 1
            player 2
            ...
            player 10
            timestamp
        ...

Note that there will be new 'event' and 'stats' entries every minute. That means, including the 0th minute, there will be 1 + 28 'event'/'stats' entries in a match with a duration of 28 minutes.

I will focus on only the 'stats' at the 15-minute timestamp since that includes the values I want.

The timestamps are in milliseconds and sadly there is not always the same timestamp at the 15-minute mark.
Here are some examples of the 15-minute timestamp of a couple of games:

| Game ID      | EUW1_5918185545 | EUW1_5852386422 | EUW1_5847243069 |
|--------------|-----------------|-----------------|-----------------|
| Milliseconds | 900207          | 900231          | 900276          |
| Minutes      | 15.00345        | 15.00385        | 15.0046         |

That means I will have to query for a range of integers.
Since I cannot look at a decent amount of games to be able to confidently define the average of the 15-minute timestamp, I will use 900000-901000 milliseconds (or 15-15,0166667 minutes).

Here is an example the 'stats' of one player at a certain timestamp:

    "1": {
        "championStats": {
            "abilityHaste": 0,
            "abilityPower": 0,
            "armor": 42,
            "armorPen": 0,
            "armorPenPercent": 0,
            "attackDamage": 73,
            "attackSpeed": 127,
            "bonusArmorPenPercent": 0,
            "bonusMagicPenPercent": 0,
            "ccReduction": 5,
            "cooldownReduction": 0,
            "health": 685,
            "healthMax": 685,
            "healthRegen": 17,
            "lifesteal": 0,
            "magicPen": 0,
            "magicPenPercent": 0,
            "magicResist": 32,
            "movementSpeed": 350,
            "omnivamp": 0,
            "physicalVamp": 0,
            "power": 339,
            "powerMax": 339,
            "powerRegen": 15,
            "spellVamp": 0
        },
        "currentGold": 98,
        "damageStats": {
            "magicDamageDone": 0,
            "magicDamageDoneToChampions": 0,
            "magicDamageTaken": 0,
            "physicalDamageDone": 440,
            "physicalDamageDoneToChampions": 0,
            "physicalDamageTaken": 0,
            "totalDamageDone": 440,
            "totalDamageDoneToChampions": 0,
            "totalDamageTaken": 0,
            "trueDamageDone": 0,
            "trueDamageDoneToChampions": 0,
            "trueDamageTaken": 0
        },
        "goldPerSecond": 0,
        "jungleMinionsKilled": 0,
        "level": 1,
        "minionsKilled": 4,
        "participantId": 1,
        "position": {
            "x": 2206,
            "y": 12847
        },
        "timeEnemySpentControlled": 0,
        "totalGold": 598,
        "xp": 211
    }

and a list of data I want to gather:

| **Value**                | **Explanation**                                                                    | **Where/How to get**                                                                        |
|--------------------------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| win                      | Which team did win                                                                 | 'GAME_END'-event                                                                            |
| wardsPlaced              | A ward provides vision and might prevent death                                     | Iterate over each 'WARD_PLACED'-event and add up                                            |
| wardsDestroyed           |                                                                                    | Iterate over each 'WARD_KILL'-event and add up                                              |
| firstBlood               | The first kill in a game provides extra gold                                       | 'killType': 'KILL_FIRST_BLOOD'                                                              |
| kills                    | Provides gold and experience and prevents enemy from gathering gold and experience | Iterate over each 'type': 'CHAMPION_KILL' and add for each 'killerID'                       |
| deaths                   |                                                                                    | Iterate over each 'type': 'CHAMPION_KILL' and add for each 'victimID'                       |
| assists                  | Provides a tiny bit of gold and experience                                         | Iterate over each 'type': 'CHAMPION_KILL' and add 'assistingParticipantIds' for each player |
| dragons                  | Provides team-wide buff, gold and experience                                       | Iterate over each 'mosterType': 'DRAGON' and read 'killerTeamId'                            |
| heralds                  | Once killed, a herald can be placed to destroy buildings                           | Iterade over each 'monsterType': 'RIFTHERALD' and read 'killerTeamId'                       |
| towerDestroyed           | Provides gold, opens the map                                                       | Iterate over each 'type': 'BUILDING_KILL' where 'buildingType': 'TOWER_BUILDING'            |
| totalGold                | Gold is required to purchase items                                                 | Read 'totalGold' from 'stats' per player                                                    |
| avgLevel                 | Player get better stats when advancing to the next level                           | Read 'level' for each summoner and divide by 5                                              |
| totalMinionsKilled       | Minions provide gold and experience                                                | Read 'minionsKilled' and add up for each player                                             |
| totalJungleMonsterKilled | Jungle monster provide gold and experience                                         | Read 'jungleMinionsKilled' and add up for each player                                       |
| csPerMinute              | Amount of minions killed per minute                                                | Add totalMinionsKilled for each player, divide by 5, divide by 15                           |
| goldPerMinute            | Amount of gold acquired per minute                                                 | Read 'goldPerSecond' for each player, add up and divide by 5                                |
| gameDuration             |                                                                                    | 'GAME_END'-event                                                                            |

(Sorry for that huge table!)

Please note that the explanation and how-to-get column might be a bit 'thin', explanation-wise.
That is to not overload the table.
Also, iterating and adding up means to add up for each player of *one* team.
(More explanation might follow)

The table below shows my variables and their data types:

| **Variable**                     | **Datatype** |
|----------------------------------|--------------|
| blueTeamWin                      | integer      |
| blueTeamWardsPlaced              | float        |
| blueTeamWardsDestroyed           | float        |
| blueTeamFirstBlood               | integer      |
| blueTeamKills                    | integer      |
| blueTeamDeaths                   | integer      |
| blueTeamAssists                  | integer      |
| blueTeamDragons                  | integer      |
| blueTeamHeralds                  | integer      |
| blueTeamTowerDestroyed           | integer      |
| blueTeamTotalGold                | integer      |
| blueTeamAvgLevel                 | float        |
| blueTeamTotalMinionsKilled       | integer      |
| blueTeamTotalJungleMonsterKilled | integer      |
| blueTeamCsPerMinute              | float        |
| blueTeamGoldPerMinute            | float        |
| gameDuration (in seconds)        | integer      |

Please note, there will be the same variables for the red team aswell.

    Sidenote:
    blueWin (and redWin) will be a numeric value to simplify the handling in the dataframe later

The participant's ids (which are not shown in the sample above) are sorted so that the first 5 ids are player from the blue team, while the last 5 ids are from the red team.
That is required to know since the events I will iterate over are assigned to these participant ids.
Also, the 'winningTeam'-variable is an integer, either set to 100 if the blue team won, or 200 if the red team won.
This is required to determine which team won the game, obviously.

Performance-wise I will filter all the necessary values and store them a csv file for each API call.

***

## The Actual Match Data I Was Able To Acquire

Unlike the prior section, where I covered the theoretical way to get the data, this chapter is about the issues I faced when *practically* getting the data.

I made some smaller mistakes in the script which lead my data to be incorrect.
These include not resetting variables which resulted in things like 300 towers destroyed in a single game (which is not impossible but highly unlikeable).

A major issue was probably with the Riot Games API (probably because I don't know exactly what produces the issue).
When querying for a match, eventually the script threw a KeyError exception (as if the JSON file being returned by the API does not contain a specific key in the JSON-dictionary).

After some code-tweaking I ended up on a script I was able to run for hours, here is a simplified pseudo-version of it:

    reads matches from file in a list
    while len(listOfMatches) > 0:
        reset data variables
        get JSON dictionary from Riot Games API for listOfMatches[0]
        read out data from that specifc game and store them in a list
        delete first item of listOfMatches
        append list of data to csv
        delay
        
This way, if a match returns a KeyError, I can ensure that the script won't break and still iterates over the same match.
The real code (and all other scripts used for this project) will be available in the GitHub.

    Sidenote:
    As of writing this sidenote (after debugging, exploring the data I got and retrying until I was happy with
    how the data gets stored) I fetched only around 5.5k (five-thousand five-hundred) games... Yay, only a bit
    more to go.

Also, if you wish to recreate this project, I highly recommend using sub-dictionaries for such huge JSON-dictionaries:

    events = data['info']['frames'][x]['events']

and iterate over 'events' instead of the whole JSON-dictionary.
By using the python module '[timeit](https://docs.python.org/3/library/timeit.html)' I figured using sub-dictionaries is more than twice as efficient performance-wise:

- 33.92717879999999 time units on average without sub-dictionaries
- 14.90106932 time units on average with sub-dictionaries

resulting in a time reduction of 56.08 % per iteration.  
(Tested on a modified version of 'get-match-data.py' with 100000 iterations each.)

You cannot imagine how happy I was when the console finally printed:

    Process finished with exit code 0

Since I might have messed up something with gathering the gameIds, I had 71.7k (seventy-one thousand seven-hundred) games to get their game data from (which is more than fine, as I know the missing 300 games must be silver games).  
Now the final csv-file contains 71.708 (seventy-one thousand seven-hundred and eight) lines of raw match data, hence containing eight duplicates due to debugging.

The last step for this chapter will be to save and backup the raw match data I got.

Now there are different ways of storing dataframes. The direct comparison shows [feather](https://arrow.apache.org/docs/python/feather.html) to be the optimal storage file-format:

![dataframes-storage-comparison](readme-files/dataframes-storage-comparison.png)

([Source](https://towardsdatascience.com/the-best-format-to-save-pandas-data-414dca023e0d), please take a look at this. There are several interesting comparisons made)

Hence, I will store my data with the feather-file-format by reading the match-data from the csv into a pandas dataframe and saving it as feather:

    import pandas as pd

    df = pd.read_csv('linkToDataFile.csv')
    df.to_feather('nameOfFileToSave.feather')

I could've saved the data from the csv directly into a feather, but I prefer my way due to convenience reasons.

***

## Why My Data Could Be Biased

This is a rather theoretical side-chapter for disclaimer reasons.

The main issues here are the different playstyles and ability to realise enemy mistakes to abuse for each tier/ELO.
A player can always outplay another player despite him having less gold, experience or stats.
That is why the stats I acquired become less important the lower the elo.

    Sidenote:
    Outplaying means to win a fight (usually 1 versus 1 or 2 versus 2) which originally does not seem to be winnable.
    The better the player, the less frequent is outplaying. Note that outplaying also happens in higher ELOs.
    But a, for example, masters player will be able to outplay more silver player than other masters player simply
    because lower elo player do more mistakes and higher elo player know how to punish these.

Now on the other side, I wanted my data to be represent for all player in relation to the rank distribution which is why a data set consisting only of challenger player is not applicable for the majority for player (the ones who are not challenger tier).

Another factor is that I fetched games from different patches.
Every two weeks Riot Games patches their game to adjust champion, items, runes and more to balance the game.
Some patches have more impact, some less.  
Small patches barely got any impact in my data.
Sadly, there has been a huge change in the champions stats in a recent patch (the 'durability patch', patch 12.10) probably resulting in different importance of values within a game.

    Sidenote:
    For example, items which increase a champion's sustainability and durability are usually more cost
    efficient and effective than items which increase a champion's damage.
    Now, after that durability patch, a champion needs to spend less gold to get a decent amount of durability
    while a different type of champion requires more gold to get the equivalent amount of damage-stats.

***

## Data Cleaning

At some point I regret choosing to use my own data, but now I am happy to finally be able to start the actual project.

Now I know for sure there will be two types of falsy data I will have to sort out:

- the duplicates due to debugging (should be eight as I covered in a previous chapter)
- falsy data returned by the Riot Games API

Falsy data returned by the Riot Games API is marked by having a '2' in both, blueTeamWin and readTeamWin, to easily sort them out.

I can get rid of these lines by doing:

    df = df[df.blueTeamWin != 2]

resulting in 70.474 (seventy-thousand four-hundred and seventy-four) matches left in my data.

Getting rid of duplicates is a bit more complex as there can completely the same data be acquired from different games..  
I will have to do some math to sort this out.

If I check for duplicates in my dataframe (after removing all the falsy data returned by Riot Games API of course) I end up 70.419 (seventy-thousand four-hundred and nineteen) matches resulting in 55 duplicates.
The reason for this could be due to debugging the script, especially in the early stages.

In order to calculate the possibility of natural duplicates I ran:

    print(df.agg([min, max]))

to get a table of the minimum and maximum value for each column. The result looks like this:

         blueTeamWin  blueTeamWardsPlaced  ...  redTeamGoldPerMinute  gameDuration
    min            0                    1  ...                     0           870
    max            1                  116  ...                  2701         50687

Now, since I know you read the previous chapters carefully, you should note that the gameDuration value is in seconds, meaning some games took up to 844 minutes (which is impossible).
Also, in the preview above the minimum for redTeamGoldPerMinute equals zero, which also shouldn't be the case.

To get a list of data to find out weird values I can do:
    
    df2 = df.agg([min, max])
    for index, row in df2.iterrows():
        print(row)

Now I can see each column's minimum and maximum value in a list. It turns out only, gameDuration, blueTeamGoldPerMinute and redTeamGoldPerMinute got inaccurate or falsy data (I don't know about gameDuration but blueTeamGoldPerMinute and redTeamGoldPerMinute might be inaccurate due to a mistake I made in my script (please see [Integer Division](https://mathworld.wolfram.com/IntegerDivision.html) for more details)).  
I will have to remove these dates from my data table.

gameDuration:

    df = df[df.gameDuration < 6000]  # get rid of all games longer than 100 minutes

blueTeamGoldPerMinute:

    df = df[df.blueTeamGoldPerMinute != 0]

redTeamGoldPerMinute:

    df = df[df.redTeamGoldPerMinute != 0]

While browsing the data, I figured I made a huge mistake in my script resulting the red team to never have first blood.
I could fix this by looking at blueTeamFirstBlood and change redTeamFirstBlood respectively.
The problem with this solution is that there can be games without first blood within the first 15 minutes.
I can check how many there are by doing:

    print(df.loc[(df.blueTeamKills == 0) & (df.blueTeamKills == 0)])

resulting in 26 games without first blood.
I decided to remove these to fix the issue with the redTeamFirstBlood-value always being 0:

    df = df.loc[(df.blueTeamKills != 0) & (df.blueTeamKills != 0)]

Note that I can filter by kills since a first blood is only possible when there is at least one kill.
Now I can change the redTeamFirstBlood-value depending on the blueTeamFirstBlood:

    df.loc[df.blueTeamFirstBlood == 0, 'redTeamFirstBlood'] = 1

At this point my data still contains 70.288 (seventy-thousand two-hundred and eighty-eight) entries which should still suffice.

Here is the overview for each variable's min and max value:

| **Variable**                     | **Min Value** | **Max Value** |
|----------------------------------|---------------|---------------|
| blueTeamWin                      | 0             | 1             |
| blueTeamWardsPlaced              | 1             | 116           |
| blueTeamWardsDestroyed           | 0             | 10            |
| blueTeamTowerDestroyed           | 0             | 9             |
| blueTeamDragonsKilled            | 0             | 2             |
| blueTeamHeraldsKilled            | 0             | 2             |
| blueTeamKills                    | 0             | 41            |
| blueTeamDeaths                   | 0             | 39            |
| blueTeamAssists                  | 0             | 47            |
| blueTeamFirstBlood               | 0             | 1             |
| blueTeamTotalGold                | 13808         | 41110         |
| blueTeamAvgLevel                 | 5             | 11            |
| blueTeamTotalMinionsKilled       | 62            | 452           |
| blueTeamTotalJungleMonsterKilled | 0             | 151           |
| blueTeamCsPerMinute              | 6             | 38            |
| blueTeamGoldPerMinute            | 921           | 2741          |
| redTeamWin                       | 0             | 1             |
| redTeamWardsPlaced               | 1             | 151           |
| redTeamWardsDestroyed            | 0             | 12            |
| redTeamTowerDestroyed            | 0             | 8             |
| redTeamDragonsKilled             | 0             | 2             |
| redTeamHeraldsKilled             | 0             | 2             |
| redTeamKills                     | 0             | 39            |
| redTeamDeaths                    | 0             | 41            |
| redTeamAssists                   | 0             | 50            |
| redTeamFirstBlood                | 0             | 1             |
| redTeamTotalGold                 | 15749         | 40514         |
| redTeamAvgLevel                  | 6             | 11            |
| redTeamTotalMinionsKilled        | 96            | 438           |
| redTeamTotalJungleMonsterKilled  | 0             | 152           |
| redTeamCsPerMinute               | 10            | 37            |
| redTeamGoldPerMinute             | 1050          | 2701          |
| gameDuration                     | 900           | 3704          |

Now I can get to do the math as I still need to figure out the issue with the duplicates as mentioned before.
To calculate the different combinations of stats, I will have to multiply each range of stats:

    max(blueTeamWin) + 1 * max(blueTeamWardsPlaced) * max(blueTeamWardsDestroyed) + 1 * ...
        
    or:
    
    1 + 1 * 116 * 10 + 1 * ...

Note that I have to add a 1 to each variable if the variable's minimum is 0 to include the 0 in the value range.

That results in 1360909601332731015410873662102557475907671047536640000, or 1.36 septendecillion different combinations.

Therefore, the probability to have the same exact game out of the different given combination is 0.000000000000000000000000000000000000000000000005164780962024764 % or 5.164780962024764e-48 %.

Hence, I can proudly say it's *highly* unlikeable to have the same data for different games and can safely remove the 55 duplicates.  
(My data still contains 70.288 (seventy-thousand two-hundred and eighty-eight) entries as I removed the duplicates before).

Another mistake I made was with rounding the values incorrectly, resulting in *all* variables to be of type integer.

***

## Exploratory Data Analysis

In this chapter I want to explore my data (obviously), want to take a look at the main characteristics and compare certain values.

The corresponding python script can also be found in the GitHub under the name 'exploratory-data-analysis.py'.

The very first thing to show is of course the win rate for each team:

![winrate](readme-files/winrate.png)

The actual win rate overall in EU West for the blue team is 50.8 % as of [League Of Graphs](https://www.leagueofgraphs.com/de/rankings/blue-vs-red/euw) in the current patch as of writing this (12.11).
I am proud my data can represent that.

We can also take a look at the team's win rate depending on having first blood:

![winrate-per-firstblood](readme-files/winrateperfirstblood.png)

The red team seems to better at winning games when playing from behind while the blue team should prefer building an advantage in the early stage of the game.

    Sidenote:
    When a champion or a team has less gold, experience or stats than the opponent,
    they are playing from 'behind'.

Another thing I want to show is the correlation between the gold and cs per minute:

![cspm-gpm-correlation](readme-files/cspmgpmcorrelation.png)

Out of appearance reasons I only used the data from the blue team if they win and the game duration is over 2.500 (two-thousand five-hundred) seconds.
Note, that the gold per minute value *should* be higher than the cs per minute value. I divided the gold per minute value by 10 for appearance.  
Cs'ing is not the only source of gold income, but it obviously takes a great part of it.

    Sidenote:
    'Cs-ing' describes the procedure of farming minions.

But I am sure the most interesting view is a heatmap:

![heatmap](readme-files/heatmap.png)

(I hope you can even recognise something on that picture..)  
The labels on the x-axis are a bit off, I couldn't find a way to fix this.
Please orientate on the y-axis.
Also, these are the values from the blue team, excluding the game duration.

This view is the best to show correlations for variables (I will cover that in a later topic).
I can for example see that the assists and kills are strongly positively correlated, obviously.
So is the amount of total minions killed and the cs per minute.

For me, the most confusing discovery is the correlation between the kills and the gold income.
I haven't heard a single skilled player saying killing enemy champions is more important than killing enemy minions (including me. Yes, I consider myself as a decent player).
Now that could be due to the fact my data mostly consists of lower elo games (gold tier and below) whereas killing champions has a higher priority than killing minions.
I tried to find a different source to proof this but couldn't find a decent one (sorry!).  
In the sake of science, I still try to proof this by showing a table of the total gold which can be acquired of one wave per game time (as of [League of Legends Wiki](https://leagueoflegends.fandom.com/wiki/Minion_(League_of_Legends)), June 2022):

| **Game Time** | **Average Gold Per Wave** | **Calculations**               | **Average Gold Per CS** |
|---------------|---------------------------|--------------------------------|-------------------------|
| 0:00          | 125                       | (3 * 21) + (3 * 14) + (60 / 3) | 19.8                    |
| 15:00         | 147                       | (3 * 21) + (3 * 14) + (84 / 2) | 22.6                    |
| 17:15         | 150                       | (3 * 21) + (3 * 14) + (90 / 2) | 23                      |
| 25:00         | 195                       | (3 * 21) + (3 * 14) + (90)     | 27.6                    |

    Sidenote:
    Minions spawn in 'waves' every 30 seconds. It consists of 3 melee and 3 caster minions.
    Every third wave, there is also a cannon minion which has way better stats than the other minion types.
    In later stages of the game, the cannon spawns more often.
    A melee minions is worth 21 gold, a caster 14 and a cannon 60 to 90 depending on game time.

A kill is worth 400 gold. To compensate the gold acquired by killing minions, one would have to kill a champion every ~1.5 minutes (calculated with values at 15 minute mark).
Now, as a prerequisite for the next part, the average level at the 15-minute mark is 9.1240395 (taken from my data).
Next up, I calculate the total death time of a champion with this level (death time increases over time):

    Formulas:
    BRW = Level × 2.5 + 7.5
    Total respawn time = BRW + ( (BRW / 100) × (current minutes - 15) × 2 × 0.425)
    
    Calculations:
    BRW = 9 × 2.5 + 7.5 = 30
    Total respawn time = 30 + ( (30 / 100) × (15 - 15) × 2 × 0.425) = 30

    Sidenote:
    'BRW' stands for 'Base Respawn Time'

Okay, so a champion needs 30 seconds to respawn.
Now I will have to guess the average movement speed (according to [League of Legends Wiki](https://leagueoflegends.fandom.com/wiki/Movement_speed)) as there is no average value for it and calculating it would take me too long (sorry!).
So I tested some champions with different boots (they provide a different amount of bonus movement speed) and came to the average of approx. 30 seconds from the fountain (a team's respawn point) to the middle of the map.
Not every fight happens in the center of the map, but I decided to take this as average.

Now I add the 30 seconds (movement) to the 30 seconds (respawn time) which equals in a minute until a champion can join the same fight.

Next, at the 15-minute mark, players usually still are on their dedicated lanes and there barely are any big fights yet.

In order for one champion to compensate not killing minions, they would need to kill the opponent laner soon as they show up.
That does not work for a solo-lane (a laner where only one champion takes place (excluding the opponent)) but it could work for the bottom lane (where there are two champions per team). 
This would require the loosing side of the bottom lane to keep dying over and over soon as they reach the enemy champions (with a 30 seconds buffer).

Thankfully, unlike the general opinion of league of legends player, player know that they should not fight again if they just lost against the enemy champions.
This results in a player not being able to keep the required 0.67 kills per minute.

Therefore, it is highly unlikeable that a player can compensate the gold income with kills without killing minions. Hence, the correlation between kills and gold income in the above heatmap is still questionable.

(Sorry for this long digression, I kind of got lost in it.. I might update this section.)

For more information on how to read a correlation matrix, please see [statology.org](https://www.statology.org/how-to-read-a-correlation-matrix/).

***

## Feature Engineering

This chapter covers the creation of variables which are most likely going to have an impact of the probability of winning.
This also is where I divide my testing and training data from my whole data set.

I will start off with separating my testing and training data:

    import pandas as pd

    df = pd.read_feather('data-final/data.feather')

    df_train = df.sample(frac=0.85, random_state=0)  # len 59745
    df_test = df.drop(df_train.index)  # len 10543

Now my training data consist of 85 % of the whole data set while the testing data takes the left over 15 %.

Next I will add variables to simplify my model for later learning purposes:

| **Variable**                    | **Calculation**                                                     |
|---------------------------------|---------------------------------------------------------------------|
| blueTeamWardRetentionRatio      | (blueTeamWardsPlaced - redTeamWardsDestroyed) / blueTeanWardsPlaced |
| blueTeamNetKills                | blueTeamKills - redTeamKills                                        |
| blueTeamJungleMinionsKilledDiff | blueTeamTotalJungleMinionsKilled - redTeamTotalJungleMinionsKilled  |
| blueTeamMinionsKilledDiff       | blueTeamTotalMinionsKilled - redTeamTotalMinionsKilled              |
| blueTeamAvgLevelDiff            | blueTeamAvgLevel - redTeamAvgLevel                                  |
| blueTeamCsPerMinuteDiff         | blueTeamCsPerMinute - redTeamCsPerMinute                            |
| blueTeamGoldPerMinuteDiff       | blueTeamGoldPerMinute - redTeamGoldPerMinute                        |

Note that I only need these variables for one team (in this case blue team), since red team wins if blue team does not.

I can add these variables simply by doing:

    df_train['blueTeamWardRetentionRatio'] = (df_train.blueTeamWardsPlaced - df_train.redTeamWardsDestroyed)/df_train.blueTeamWardsPlaced
    df_train['blueTeamNetKills'] = (df_train.blueTeamKills - df_train.redTeamKills)
    df_train['blueTeamJungleMinionsKilledDiff'] = (df_train.blueTeamTotalJungleMonsterKilled - df_train.redTeamTotalJungleMonsterKilled)
    df_train['blueTeamMinionsKilledDiff'] = (df_train.blueTeamTotalMinionsKilled - df_train.redTeamTotalMinionsKilled)
    df_train['blueTeamAvgLevelDiff'] = (df_train.blueTeamAvgLevel - df_train.redTeamAvgLevel)
    df_train['blueTeamCsPerMinuteDiff'] = (df_train.blueTeamCsPerMinute - df_train.redTeamCsPerMinute)
    df_train['blueTeamGoldPerMinuteDiff'] = (df_train.blueTeamGoldPerMinute - df_train.redTeamGoldPerMinute)

By checking the training dataframe's head:

    print(df_train.head())

I get in return:

           blueTeamWin  ...  blueTeamGoldPerMinuteDiff
    16538            1  ...                        616
    47472            1  ...                        144
    27040            0  ...                       -349
    36878            1  ...                        441
    860              1  ...                         75

***

## Dealing With Multicollinearity

Multicollinearity describes the issue with multiple variables correlating when predicting the same outcome.

Say the blue team got first blood, have lots of early-game-champions in their team, decent player and an understanding of extending the advantage they acquired.
Now surely the blue team will have more options to actively control the game. That results in blue team having more gold and experience.
If the blue team now wins the game, it's not easy to say which factors (for example gold or experience) had more impact to that.

    Sidenote:
    A match can be classified in three stages: early-, mid- or late-game.
    An 'early-game-champion' performs well in the earlier stage of the game,
    while a late-game-champion often suffers early on against early-game-champions.

A simple example (with barely any matches to be able to visualise the problem):

![multicollinearity](readme-files/multicollinearity.png)

(Note, the values are unified for appearance reasons)

As seen in the plot, the two values do correlate quiet often.
Now I cannot tell which value induces the other as both seem to be valuable yet similar.

I will deal with it for now.
If I am not happy with the result of the model I might tweak the values later.

***

## Building Classifier Models

tbd

***

## Evaluation

***

tbd

***

## Testing

WIP

10 oder 20% von den matches kommen nicht ins model und werden zum testen verwendet

unterscheidung zwischen unbiased und biased data:
- unbiased mit den 10 oder 20% der games (elo unbekannt, weil matches sortiert werden)
- biased mit neuen games, bei denen ich die elo weiß

(ROC-Curve !)