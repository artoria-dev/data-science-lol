import csv
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

apiKey = '<your api key>'

with open('matchIds.txt', 'r') as f:
    matches = f.read().splitlines()

def fetch_match_data(match_id):
    url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={apiKey}'
    try:
        response = requests.get(url)
        data = response.json()

        if 'info' not in data or 'frames' not in data['info']:
            return None

        lastEvent = data['info']['frames'][-1]['events'][-1]
        if lastEvent['timestamp'] <= 870000:
            return None

        # initialise required variables
        blueTeamKills = 0
        blueTeamWardsPlaced = 0
        blueTeamTotalJungleMinionsKilled = 0
        blueTeamTotalMinionsKilled = 0
        blueTeamAvgLevel = 0
        blueTeamCsPerMinute = 0
        blueTeamGoldPerMinute = 0

        redTeamKills = 0
        redTeamWardsDestroyed = 0
        redTeamTotalJungleMinionsKilled = 0
        redTeamTotalMinionsKilled = 0
        redTeamAvgLevel = 0
        redTeamCsPerMinute = 0
        redTeamGoldPerMinute = 0

        winningTeam = 2
        if 'winningTeam' in lastEvent:
            winningTeam = 1 if lastEvent['winningTeam'] == 100 else 0

        x = 0
        while x <= 15:
            events = data['info']['frames'][x]['events']
            participants = data['info']['frames'][x]['participantFrames']

            for event in events:
                if event['type'] == 'WARD_PLACED' and 1 <= event['creatorId'] <= 5:
                    blueTeamWardsPlaced += 1
                if event['type'] == 'WARD_KILL' and 6 <= event['killerId'] <= 10:
                    redTeamWardsDestroyed += 1
                if event['type'] == 'CHAMPION_KILL':
                    if 1 <= event['killerId'] <= 5:
                        blueTeamKills += 1
                    elif 6 <= event['killerId'] <= 10:
                        redTeamKills += 1

            for participant in participants.values():
                if participant['participantId'] <= 5:
                    blueTeamAvgLevel += participant['level']
                    blueTeamTotalMinionsKilled += participant['minionsKilled']
                    blueTeamTotalJungleMinionsKilled += participant['jungleMinionsKilled']
                    blueTeamGoldPerMinute += participant['totalGold']
                else:
                    redTeamAvgLevel += participant['level']
                    redTeamTotalMinionsKilled += participant['minionsKilled']
                    redTeamTotalJungleMinionsKilled += participant['jungleMinionsKilled']
                    redTeamGoldPerMinute += participant['totalGold']

            x += 1

        blueTeamTotalMinionsKilled /= 10
        redTeamTotalMinionsKilled /= 10
        blueTeamTotalJungleMinionsKilled /= 10
        redTeamTotalJungleMinionsKilled /= 10
        blueTeamAvgLevel /= 5
        blueTeamAvgLevel /= 10
        redTeamAvgLevel /= 5
        redTeamAvgLevel /= 10
        blueTeamCsPerMinute = (blueTeamTotalMinionsKilled + blueTeamTotalJungleMinionsKilled) / 15
        redTeamCsPerMinute = (redTeamTotalMinionsKilled + redTeamTotalJungleMinionsKilled) / 15
        blueTeamGoldPerMinute /= 15
        blueTeamGoldPerMinute /= 10
        redTeamGoldPerMinute /= 15
        redTeamGoldPerMinute /= 10

        return [winningTeam, blueTeamWardsPlaced, blueTeamKills, round(blueTeamTotalJungleMinionsKilled, 2),
                round(blueTeamTotalMinionsKilled, 2),
                round(blueTeamAvgLevel, 2), round(blueTeamCsPerMinute, 2), round(blueTeamGoldPerMinute, 2),
                redTeamWardsDestroyed, redTeamKills, round(redTeamTotalJungleMinionsKilled, 2),
                round(redTeamTotalMinionsKilled, 2),
                round(redTeamAvgLevel, 2), round(redTeamCsPerMinute, 2), round(redTeamGoldPerMinute, 2)]
    except Exception as e:
        print(f"Error fetching data for match {match_id}: {e}")
        return None


def main():
    with open('match-data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['winningTeam', 'blueTeamWardsPlaced', 'blueTeamKills', 'blueTeamTotalJungleMinionsKilled',
                         'blueTeamTotalMinionsKilled', 'blueTeamAvgLevel', 'blueTeamCsPerMinute',
                         'blueTeamGoldPerMinute',
                         'redTeamWardsDestroyed', 'redTeamKills', 'redTeamTotalJungleMinionsKilled',
                         'redTeamTotalMinionsKilled',
                         'redTeamAvgLevel', 'redTeamCsPerMinute', 'redTeamGoldPerMinute'])

        batches_processed = 0

        with ThreadPoolExecutor(max_workers=10) as executor:
            for i in range(0, len(matches), 50):
                batch = matches[i:i + 50]
                futures = [executor.submit(fetch_match_data, match_id) for match_id in batch]
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        writer.writerow(result)
                batches_processed += 1
                print(f"processed {batches_processed * 50} matches")
                time.sleep(1)


if __name__ == '__main__':
    t = time.time()
    main()
    print(f"took {round((time.time() - t * 60), 2)} minutes")
