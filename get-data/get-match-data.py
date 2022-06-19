import csv

import requests
import time

apiKey = 'YOUR-RIOT-GAMES-API-KEY'


# get matches
with open('matches.txt', 'r') as f:
    matches = f.read().splitlines()


def main():

    with open(r'match-data.csv', 'a') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')

        # iterate over matches while there are still matches to iterate over
        while len(matches) > 0:

            # api call sometimes returns error for no reason at all
            # when querying the same game again it works
            try:

                # reset values, some add up over iterations
                blueTeamTotalGold = 0
                blueTeamAvgLevel = 0
                blueTeamTotalMinionsKilled = 0
                blueTeamTotalJungleMonsterKilled = 0

                redTeamTotalGold = 0
                redTeamAvgLevel = 0
                redTeamTotalMinionsKilled = 0
                redTeamTotalJungleMonsterKilled = 0

                blueTeamWardsPlaced = 0
                blueTeamWardsDestroyed = 0
                blueTeamTowerDestroyed = 0
                blueTeamDragonsKilled = 0
                blueTeamHeraldsKilled = 0
                blueTeamKills = 0
                blueTeamDeaths = 0
                blueTeamAssists = 0

                redTeamWardsPlaced = 0
                redTeamWardsDestroyed = 0
                redTeamTowerDestroyed = 0
                redTeamDragonsKilled = 0
                redTeamHeraldsKilled = 0
                redTeamKills = 0
                redTeamDeaths = 0
                redTeamAssists = 0

                gameDuration = 0

                # in case no first blood in first 15 min, later to sort out in the df
                blueTeamFirstBlood = 2
                redTeamFirstBlood = 2

                blueTeamWin = 2
                redTeamWin = 2

                print(matches[0])  # debug printer

                response = requests.get(
                    'https://europe.api.riotgames.com/lol/match/v5/matches/' + matches[0] + '/timeline?api_key=' + apiKey)
                data = response.json()

                lastEvent = data['info']['frames'][-1]['events'][-1]  # so python doesnt have to iterate over the whole dictionary each time

                # check if game is longer than 14.5 minutes (in case of ff or buggy return values)
                if lastEvent['timestamp'] > 870000:
                    # blueTeamWin redTeamWin
                    try:
                        if lastEvent['winningTeam'] == 100:
                            blueTeamWin = 1
                            redTeamWin = 0
                        elif lastEvent['winningTeam'] == 200:
                            blueTeamWin = 0
                            redTeamWin = 1
                        else:  # in case something is messed up to check after
                            blueTeamWin = 2
                            redTeamWin = 2
                    except KeyError:
                        blueTeamWin = 2
                        redTeamWin = 2

                    # game duration, will be saved in seconds
                    gameDuration = (lastEvent['timestamp']) / 1000

                    x = 0  # x equals every minute in the game
                    while x <= 15:  # get all infos until (including) 15th minute

                        events = data['info']['frames'][x]['events']  # so python doesnt have to iterate over the whole dictionary each time

                        # iterates over each event in a game
                        for y in range(len(events)):
                            # wards placed check
                            if events[y]['type'] == 'WARD_PLACED':
                                if 1 <= events[y]['creatorId'] <= 5:
                                    blueTeamWardsPlaced += 1
                                elif 6 <= events[y]['creatorId'] <= 10:
                                    redTeamWardsPlaced += 1
                            # wards destroyed check
                            if events[y]['type'] == 'WARD_KILL':
                                if 1 <= events[y]['killerId'] <= 5:
                                    blueTeamWardsDestroyed += 1
                                elif 6 <= events[y]['killerId'] <= 10:
                                    redTeamWardsDestroyed += 1
                            # towers destroyed check
                            if events[y]['type'] == 'BUILDING_KILL':
                                if events[y]['buildingType'] == 'TOWER_BUILDING':
                                    if 1 <= events[y]['killerId'] <= 5:
                                        blueTeamTowerDestroyed += 1
                                    elif 6 <= events[y]['killerId'] <= 10:
                                        redTeamTowerDestroyed += 1
                            # elite jungle monster check (dragon / herald)
                            if events[y]['type'] == 'ELITE_MONSTER_KILL':
                                # dragon
                                if events[y]['monsterType'] == 'DRAGON':
                                    if 1 <= events[y]['killerId'] <= 5:
                                        blueTeamDragonsKilled += 1
                                    elif 6 <= events[y]['killerId'] <= 10:
                                        redTeamDragonsKilled += 1
                                # herald
                                if events[y]['monsterType'] == 'RIFTHERALD':
                                    if 1 <= events[y]['killerId'] <= 5:
                                        blueTeamHeraldsKilled += 1
                                    elif 6 <= events[y]['killerId'] <= 10:
                                        redTeamHeraldsKilled += 1
                            # kills / deaths
                            if events[y]['type'] == 'CHAMPION_KILL':
                                if 1 <= events[y]['killerId'] <= 5:
                                    blueTeamKills += 1
                                    redTeamDeaths += 1
                                    if 'assistingParticipantIds' in events[y]:
                                        blueTeamAssists += len(
                                            events[y]['assistingParticipantIds'])
                                elif 6 <= events[y]['killerId'] <= 10:
                                    blueTeamDeaths += 1
                                    redTeamKills += 1
                                    if 'assistingParticipantIds' in events[y]:
                                        redTeamAssists += len(
                                            events[y]['assistingParticipantIds'])
                            # first blood check
                            if 'killType' in events[y]:
                                if events[y]['killType'] == 'KILL_FIRST_BLOOD':
                                    if 1 <= events[y]['killerId'] <= 5:
                                        blueTeamFirstBlood = 1
                                        redTeamFirstBlood = 0
                                    elif 6 <= events[y]['killerId'] <= 10:
                                        blueTeamFirstBlood = 0
                                        redTeamFirstBlood = 1

                        participants = data['info']['frames'][x]['participantFrames']  # so python doesnt have to iterate over the whole dictionary each time

                        # check timestamp values
                        if 900000 < data['info']['frames'][x]['timestamp'] < 901000:  # see readme for range explanation
                            for participant in participants:
                                # blue team
                                if int(participant) <= 5:
                                    blueTeamTotalGold += participants[participant][
                                        'totalGold']
                                    blueTeamAvgLevel += participants[participant]['level']
                                    blueTeamTotalMinionsKilled += participants[participant][
                                        'minionsKilled']
                                    blueTeamTotalJungleMonsterKilled += participants[participant][
                                        'jungleMinionsKilled']
                                # red team
                                else:
                                    redTeamTotalGold += participants[participant][
                                        'totalGold']
                                    redTeamAvgLevel += participants[participant]['level']
                                    redTeamTotalMinionsKilled += participants[participant][
                                        'minionsKilled']
                                    redTeamTotalJungleMonsterKilled += participants[participant][
                                        'jungleMinionsKilled']
                        x += 1  # increase to check next timestamp

                # get avg team level
                blueTeamAvgLevel = blueTeamAvgLevel / 5
                redTeamAvgLevel = redTeamAvgLevel / 5
                # get avg team cs
                blueTeamCsPerMinute = (blueTeamTotalMinionsKilled + blueTeamTotalJungleMonsterKilled) / 15
                redTeamCsPerMinute = (redTeamTotalMinionsKilled + redTeamTotalJungleMonsterKilled) / 15
                # get avg team gold
                blueTeamGoldPerMinute = blueTeamTotalGold / 15
                redTeamGoldPerMinute = redTeamTotalGold / 15
                # get avg wards placed
                blueTeamWardsPlaced = blueTeamWardsPlaced / 5
                redTeamWardsPlaced = redTeamWardsPlaced / 5
                # get avg wards destroyed
                blueTeamWardsDestroyed = blueTeamWardsDestroyed / 5
                redTeamWardsDestroyed = redTeamWardsDestroyed / 5

                # this will be written to csv file, some values rounded for data readability
                writeToFile = [blueTeamWin, round(blueTeamWardsPlaced), round(blueTeamWardsDestroyed),
                               blueTeamTowerDestroyed,
                               blueTeamDragonsKilled,
                               blueTeamHeraldsKilled, blueTeamKills, blueTeamDeaths, blueTeamAssists, blueTeamFirstBlood,
                               blueTeamTotalGold, round(blueTeamAvgLevel), blueTeamTotalMinionsKilled,
                               blueTeamTotalJungleMonsterKilled, round(blueTeamCsPerMinute),
                               round(blueTeamGoldPerMinute),
                               redTeamWin,
                               round(redTeamWardsPlaced), round(redTeamWardsDestroyed), redTeamTowerDestroyed,
                               redTeamDragonsKilled,
                               redTeamHeraldsKilled, redTeamKills, redTeamDeaths, redTeamAssists, redTeamFirstBlood,
                               redTeamTotalGold,
                               round(redTeamAvgLevel), redTeamTotalMinionsKilled, redTeamTotalJungleMonsterKilled,
                               round(redTeamCsPerMinute),
                               round(redTeamGoldPerMinute), round(gameDuration)]

                matches.pop(0)  # removes current checked game from list
                writer.writerow(writeToFile)
                time.sleep(1.3)  # *must* be over 1.2, higher values better in cost of time efficiency
            except KeyError:
                print(' error')
                time.sleep(5)


if __name__ == '__main__':
    main()
