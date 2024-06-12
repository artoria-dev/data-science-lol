import requests
import time

api_key = '<your api key>'


def apex(elo, amount):
    gathered = 0
    summoner_ids = []

    while gathered < amount:
        response = requests.get(
            f'https://euw1.api.riotgames.com/lol/league/v4/{elo}leagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}')
        response_data = response.json()

        if 'entries' not in response_data:
            print("error: 'entries' key not found in the response")
            return

        for summoner in response_data['entries']:
            try:
                summoner_ids.append(summoner['summonerId'])
                gathered += 1
                print(f'summoner id: {summoner["summonerId"]}')
                if gathered >= amount:
                    break
            except UnicodeEncodeError:
                pass

    print(f'gathered {gathered} {elo} players')

    with open('summonerIds.txt', 'a') as f:
        for summoner_id in summoner_ids:
            f.write(summoner_id + '\n')


def casuals(elo, amount, page=1):
    gathered = 0
    summoner_ids = []

    while gathered < amount:
        response = requests.get(
            f'https://euw1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{elo}/III?page={page}&api_key={api_key}')

        for summoner in response.json():
            try:
                summoner_ids.append(summoner['summonerId'])
                gathered += 1
                print(f'summoner id: {summoner["summonerId"]}')
                if gathered >= amount:
                    break
            except UnicodeEncodeError:
                pass
        page += 1

    print(f'gathered {gathered} {elo} players')

    with open('summonerIds.txt', 'a') as f:
        for summoner_id in summoner_ids:
            f.write(summoner_id + '\n')


if __name__ == '__main__':
    t = time.time()
    apex('challenger', 1)
    apex('grandmaster', 2)
    apex('master', 16)
    casuals('DIAMOND', 236)
    casuals('EMERALD', 559)
    casuals('PLATINUM', 942)
    casuals('GOLD', 765)
    casuals('SILVER', 1000)
    casuals('BRONZE', 1471)
    casuals('IRON', 765)
    print(f'\ntook {round(time.time() - t, 2)} seconds')

