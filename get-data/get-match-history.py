import requests
import time

apiKey = 'YOUR-RIOT-GAMES-API-KEY'

with open('puuids.txt', 'r') as f:
    puuids = f.read().splitlines()

with open('matches.txt', 'a') as f:
    idx = 1
    for puuid in puuids:
        print(idx)
        response = requests.get(
            'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid + '/ids?type=ranked&start=0&count=100&api_key=' + apiKey)
        for match in response.json():
            f.write(match + '\n')
        idx += 1
        time.sleep(1.3)  # 1.2 required for api rate limitation, 1.5 used for safety
