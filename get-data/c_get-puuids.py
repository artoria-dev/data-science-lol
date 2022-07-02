import requests
import time

apiKey = 'YOUR-RIOT-GAMES-API-KEY'

with open('c_summoner-names.txt', 'r') as f:
    summonerNames = f.read().splitlines()

with open('c_puuids.txt', 'a') as f:
    for summonerName in summonerNames:
        print(summonerName)
        try:
            response = requests.get(
                'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonerName + '?api_key=' + apiKey)
            f.write(response.json()['puuid'] + '\n')
        except KeyError:
            print(' failed to get', summonerName)
            pass
        time.sleep(1.3)  # 1.2 required for api rate limitation, 1.3 used for safety
