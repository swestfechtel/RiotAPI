from __future__ import division

import csv
import time
from multiprocessing import Pool, cpu_count
from os import getpid

import requests

API_KEY = "RGAPI-aa6adef0-bf2f-4af5-9971-de946dc62732"


def read_matches(filename):
    with open(filename, newline='') as input_file:
        cvs_reader = csv.reader(input_file, delimiter=',')
        return list(cvs_reader)


def extract_match_details(match_ids):
    print(f"Process {getpid()}: Extracting data for match id {match_ids}.")
    #for x in match_ids:
    x = match_ids
    url = "https://euw1.api.riotgames.com/lol/match/v4/matches/" + str(x) + "?api_key=" + API_KEY
    request = requests.get(url=url)
    while request.status_code != 200:
        if request.status_code == 429:
            retry = int(request.headers['Retry-After']) + 1
            print(f"Process {getpid()}: Response code {request.status_code}. Retrying in {retry}s..")
            time.sleep(retry)
            request = requests.get(url=url)
        else:
            print(f"Response code {request.status_code}. Ending query chain.")
            return None

    data = request.json()
    unique_summoners = set()
    summoner_games = {}
    game_duration = data['gameDuration']
    participant_ids = data['participantIdentities']
    participants = data['participants']
    teams = data['teams']
    for y in range(len(participant_ids)):
        current_summoner = participant_ids[y]['player']
        current_summoner_id = participant_ids[y]['participantId']
        current_summoner_name = current_summoner['summonerName']
        if current_summoner_name not in unique_summoners:
            unique_summoners.add(current_summoner_name)
            summoner_games[current_summoner_name] = list()
        current_summoner = next(item for item in participants if item['participantId'] == current_summoner_id)
        current_summoner_team = current_summoner['teamId']
        current_summoner_champion = current_summoner['championId']
        current_summoner_spell1 = current_summoner['spell1Id']
        current_summoner_spell2 = current_summoner['spell2Id']
        current_summoner_stats = current_summoner['stats']
        current_summoner_team = next(item for item in teams if item['teamId'] == current_summoner_team)
        current_summoner_data = dict(
            duration=game_duration,
            team=current_summoner_team,
            champion=current_summoner_champion,
            spell1=current_summoner_spell1,
            spell2=current_summoner_spell2,
            stats=current_summoner_stats,
        )
        summoner_games[current_summoner_name].append(current_summoner_data)

    return summoner_games


def write_games(game_collection, filename):
    with open(filename, mode='w', newline='') as output:
        fieldnames = ['player', 'games']
        csv_writer = csv.DictWriter(output, delimiter=',', fieldnames=fieldnames)
        csv_writer.writeheader()
        for key, value in game_collection.items():
            try:
                csv_writer.writerow({'player': key, 'games': value})
            except UnicodeEncodeError as e:
                print(f"Exception: {type(e)}")


if __name__ == '__main__':
    m_ids = read_matches('more_match_ids.csv')[0]
    m_ids = list(map(lambda k: int(k), m_ids))
    print(f"Fetched {len(m_ids)} matches.")
    del m_ids[:20000]
    print(f"Cut first 20,000 elements from m_ids, so there are {len(m_ids)} matches left.")

    # unique_summoners = set()
    # summoner_games = {}
    # Test:
    # m_ids = [4214995204, 4214949920, 4214946978, 4214953085, 4214901875, 4214818720, 4214478065, 4213764308]

    games = {}
    cpu_count = cpu_count()
    print(f"Detected {cpu_count} CPUs.")
    chunksize = len(m_ids)//cpu_count

    with Pool(processes=cpu_count) as pool:
        games = pool.map(func=extract_match_details, iterable=m_ids, chunksize=chunksize)

    games_dict = {}
    for game in games:
        if game is not None:
            for k, v in game.items():
                if k not in games_dict:
                    games_dict[k] = v
                else:
                    games_dict[k].extend(v)
                    print(f"Added {v} to {k}.")

    write_games(game_collection=games_dict, filename='more_player_games.csv')
