import requests
import time

apiKey = 'YOUR-RIOT-GAMES-API-KEY'
page = 1
playersGathered = 0

while playersGathered < 2000:
    response = requests.get(
        'https://euw1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/GRANDMASTER/I?page=' + str(
            page) + '&api_key=' + apiKey)
    with open('c_summoner-names.txt', 'a') as f:
        for summoner in response.json():
            try:
                f.write(summoner['summonerName'] + '\n')
                playersGathered += 1
                print(f'page: {page} | players gathered: {playersGathered} | summoner name: {summoner["summonerName"]}')
            except UnicodeEncodeError:
                pass
    time.sleep(1.3)  # 1.2 required for api rate limitation, 1.3 used for safety
    page += 1
