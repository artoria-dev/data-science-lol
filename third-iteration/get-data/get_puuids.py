import time
import requests
from concurrent.futures import ThreadPoolExecutor

api_key = '<your api key>'


def fetch_puuid(summoner_id):
    url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('puuid')
    else:
        print(f"failed to fetch data for {summoner_id}, status code: {response.status_code}")
        return None


def main():
    with open('summonerIds.txt', 'r') as f:
        summoner_ids = f.read().splitlines()

    puuids = []
    batch_size = 50
    delay = 1

    for i in range(0, len(summoner_ids), batch_size):
        batch = summoner_ids[i:i + batch_size]

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fetch_puuid, summoner_id) for summoner_id in batch]
            for future in futures:
                puuid = future.result()
                if puuid:
                    puuids.append(puuid)
        print(f"processed {len(puuids)} summoner ids")
        time.sleep(delay)

    with open('puuids.txt', 'a') as f:
        for puuid in puuids:
            f.write(puuid + '\n')


if __name__ == "__main__":
    t = time.time()
    main()
    print(f"took {round(time.time() - t, 2)} seconds")
