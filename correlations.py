import csv
import sys
import ast


def read_players(filename):
    names = list()
    with open(filename, mode='r', newline='') as input_file:
        csv_reader = csv.DictReader(input_file)
        for row in csv_reader:
            names.append(row['player'])

    return names


def read_player_games(filename):
    games_dict = {}
    with open(filename, mode='r', newline='') as input_file:
        csv_reader = csv.DictReader(input_file)
        for row in csv_reader:
            if row['player'] not in games_dict:
                games_dict[row['player']] = row['games']

    return games_dict


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

data = {'ich': [{'duration': 961,
         'team': {'teamId': 200, 'win': 'Fail', 'firstBlood': True, 'firstTower': False, 'firstInhibitor': False,
                  'firstBaron': False, 'firstDragon': False, 'firstRiftHerald': False, 'towerKills': 0,
                  'inhibitorKills': 0, 'baronKills': 0, 'dragonKills': 0, 'vilemawKills': 0, 'riftHeraldKills': 0,
                  'dominionVictoryScore': 0, 'bans': []}, 'champion': 22, 'spell1': 21, 'spell2': 4,
         'stats': {'participantId': 10, 'win': False, 'item0': 3085, 'item1': 3006, 'item2': 3031, 'item3': 1053,
                   'item4': 1038, 'item5': 0, 'item6': 2052, 'kills': 3, 'deaths': 12, 'assists': 16,
                   'largestKillingSpree': 2, 'largestMultiKill': 1, 'killingSprees': 1, 'longestTimeSpentLiving': 114,
                   'doubleKills': 0, 'tripleKills': 0, 'quadraKills': 0, 'pentaKills': 0, 'unrealKills': 0,
                   'totalDamageDealt': 34391, 'magicDamageDealt': 960, 'physicalDamageDealt': 33431,
                   'trueDamageDealt': 0, 'largestCriticalStrike': 328, 'totalDamageDealtToChampions': 10868,
                   'magicDamageDealtToChampions': 812, 'physicalDamageDealtToChampions': 10056,
                   'trueDamageDealtToChampions': 0, 'totalHeal': 1421, 'totalUnitsHealed': 1,
                   'damageSelfMitigated': 5296, 'damageDealtToObjectives': 288, 'damageDealtToTurrets': 288,
                   'visionScore': 0, 'timeCCingOthers': 40, 'totalDamageTaken': 16642, 'magicalDamageTaken': 6436,
                   'physicalDamageTaken': 9652, 'trueDamageTaken': 553, 'goldEarned': 9586, 'goldSpent': 9500,
                   'turretKills': 0, 'inhibitorKills': 0, 'totalMinionsKilled': 23, 'neutralMinionsKilled': 0,
                   'totalTimeCrowdControlDealt': 678, 'champLevel': 14, 'visionWardsBoughtInGame': 0,
                   'sightWardsBoughtInGame': 0, 'firstBloodKill': False, 'firstBloodAssist': False,
                   'firstTowerKill': False, 'firstTowerAssist': False, 'firstInhibitorKill': False,
                   'firstInhibitorAssist': False, 'combatPlayerScore': 0, 'objectivePlayerScore': 0,
                   'totalPlayerScore': 0, 'totalScoreRank': 0, 'playerScore0': 0, 'playerScore1': 0, 'playerScore2': 0,
                   'playerScore3': 0, 'playerScore4': 0, 'playerScore5': 0, 'playerScore6': 0, 'playerScore7': 0,
                   'playerScore8': 0, 'playerScore9': 0, 'perk0': 8005, 'perk0Var1': 879, 'perk0Var2': 522,
                   'perk0Var3': 356, 'perk1': 9111, 'perk1Var1': 677, 'perk1Var2': 0, 'perk1Var3': 0, 'perk2': 9104,
                   'perk2Var1': 6, 'perk2Var2': 5, 'perk2Var3': 0, 'perk3': 8017, 'perk3Var1': 220, 'perk3Var2': 0,
                   'perk3Var3': 0, 'perk4': 8139, 'perk4Var1': 627, 'perk4Var2': 0, 'perk4Var3': 0, 'perk5': 8135,
                   'perk5Var1': 4, 'perk5Var2': 0, 'perk5Var3': 0, 'perkPrimaryStyle': 8000, 'perkSubStyle': 8100}}]}

# write_games(game_collection=data, filename='test.csv')
games = read_player_games('player_games.csv')
for k, v in games.items():
    print(k, v)
    tmp = ast.literal_eval(v)
    print(len(tmp))
    for x in tmp:
        print(x)
        print(x['duration'])
