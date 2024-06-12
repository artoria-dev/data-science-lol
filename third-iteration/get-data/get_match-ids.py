import time
import requests
from concurrent.futures import ThreadPoolExecutor

api_key = '<your api key>'


def fetch_games(puuid):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&type=ranked&start=0&count=100&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"failed to fetch data for {puuid}, status code: {response.status_code}")
        return None


def main():
    with open('puuids.txt', 'r') as f:
        summoner_ids = f.read().splitlines()

    game_list = []
    batch_size = 50
    delay = 1

    for i in range(0, len(summoner_ids), batch_size):
        batch = summoner_ids[i:i + batch_size]

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fetch_games, game) for game in batch]
            for future in futures:
                game = future.result()
                if game:
                    game_list.append(game)
        print(f"processed {len(game_list)} puuids")
        time.sleep(delay)

    with open('matchIds.txt', 'a') as f:
        for games in game_list:
            for game in games:
                f.write(game + '\n')


if __name__ == "__main__":
    t = time.time()
    main()
    print(f"took {round(time.time() - t, 2)} seconds")
