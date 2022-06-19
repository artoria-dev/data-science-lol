import requests
import time

apiKey = 'YOUR-RIOT-GAMES-API-KEY'

with open('summoner-names.txt', 'r') as f:
    summonerNames = f.read().splitlines()

with open('puuids.txt', 'a') as f:
    for summonerName in summonerNames:
        print(summonerName)
        try:
            response = requests.get(
                'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonerName + '?api_key=' + apiKey)
        except KeyError:
            print('failed to get', summonerName)
            pass
        f.write(response.json()['puuid'] + '\n')
        time.sleep(1.3)  # 1.2 required for api rate limitation, 1.3 used for safety
