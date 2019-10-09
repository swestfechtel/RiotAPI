import time
import requests
import csv
import sys

API_KEY = "RGAPI-45ea7437-01e9-4b30-b710-147df3804c01"


def read_players(filename, max_count):
    names = list()
    with open(filename, mode='r', newline='') as input_file:
        csv_reader = csv.DictReader(input_file)
        name_count = 0
        for row in csv_reader:
            name_count += 1
            names.append(row['player'])
            if name_count == max_count:
                break

    return names


def get_id_for_name(name):
    url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={API_KEY}"
    request = requests.get(url=url)
    summoner = request.json()
    return summoner['accountId']


def get_matches(account_id, count):
    begin_index = 0
    end_index = 80
    m_ids = []

    for i in range(count):
        print(f"Run #{i} from {begin_index} to {end_index}.")
        m_url = f"https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?beginIndex={begin_index}&endIndex={end_index}&api_key={API_KEY}"
        m_request = requests.get(url=m_url)
        while m_request.status_code != 200:
            if m_request.status_code == 429:
                retry = int(m_request.headers['Retry-After']) + 1
                print(f"Response code {m_request.status_code}. Retrying in {retry}s..")
                time.sleep(retry)
                m_request = requests.get(url=m_url)
            else:
                print(f"Response code {m_request.status_code}. Ending query chain.")
                return None

        matches = m_request.json()
        matches = matches['matches']
        for j in range(len(matches)):
            m_ids.append(matches[j]['gameId'])

        begin_index = end_index + 1
        end_index += 80
        # time.sleep(120)

    return m_ids


def write_matches(match_ids, filename):
    with open(filename, mode='w', newline='') as output:
        csv_writer = csv.writer(output, delimiter=',')
        csv_writer.writerow(match_ids)


maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

csv.field_size_limit(maxInt)

unique_matches = set()
ids_for_writing = list()
name_list = read_players('player_games.csv', 100)
print(f"Read {len(name_list)} names from file.")
for n in name_list:
    p_id = get_id_for_name(n)
    p_matches = get_matches(p_id, 10)
    for x in p_matches:
        if x not in unique_matches:
            unique_matches.add(x)
            ids_for_writing.append(x)

print(f"Fetched {len(ids_for_writing)} unique match ids.")
write_matches(ids_for_writing, 'more_match_ids.csv')