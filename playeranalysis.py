from collections import OrderedDict
from matplotlib import pyplot


def average_cs(summoner_name, s_data):
    s_data = s_data[summoner_name]
    total_cs = 0
    game_count = len(s_data)
    wins = 0
    defeats = 0
    for game in s_data:
        if game['stats']['win']:
            wins += 1
        else:
            defeats += 1

        total_cs += game['stats']['totalMinionsKilled']

    return total_cs / game_count


def winrate(summoner_name, s_data):
    s_data = s_data[summoner_name]
    wins = 0
    defeats = 0
    for game in s_data:
        if game['stats']['win']:
            wins += 1
        else:
            defeats += 1

    return wins / (wins + defeats)


def stats(summoner_name, s_data):
    s_data = s_data[summoner_name]

    print("Average cs for won games:")
    total_cs = 0
    games_won = 0
    for d in s_data:
        if d['stats']['win']:
            total_cs += d['stats']['totalMinionsKilled']
            games_won += 1
    avg_cs = total_cs / games_won
    print(avg_cs)

    print("Average cs for lost games:")
    total_cs = 0
    games_lost = 0
    for d in s_data:
        if not d['stats']['win']:
            total_cs += d['stats']['totalMinionsKilled']
            games_lost += 1
    avg_cs = total_cs / games_lost
    print(avg_cs)

    print("CS versus winrate:")
    w = {}
    l = {}
    for d in s_data:
        result = d['stats']['win']
        if result:
            if d['stats']['totalMinionsKilled'] not in w:
                w[d['stats']['totalMinionsKilled']] = 1
            else:
                w[d['stats']['totalMinionsKilled']] += 1
        else:
            if d['stats']['totalMinionsKilled'] not in l:
                l[d['stats']['totalMinionsKilled']] = 1
            else:
                l[d['stats']['totalMinionsKilled']] += 1

    wrcs = {}
    for d in s_data:
        if d['stats']['totalMinionsKilled'] not in w:
            wrcs[d['stats']['totalMinionsKilled']] = 0
        elif d['stats']['totalMinionsKilled'] not in l:
            wrcs[d['stats']['totalMinionsKilled']] = 1
        else:
            wrcs[d['stats']['totalMinionsKilled']] = w[d['stats']['totalMinionsKilled']] / (
                        w[d['stats']['totalMinionsKilled']] + l[d['stats']['totalMinionsKilled']])

    ordered_wrcs = OrderedDict(sorted(wrcs.items()))

    x = list(ordered_wrcs.keys())
    y = list(ordered_wrcs.values())

    pyplot.plot(x, y)
    pyplot.show()
