import genetic
import team

#non-goalie stat categories
ng=[ 1,2,4,5,6,7,9,10,12,14,16,31,32]

MYTEAMID=6

players = team.readPickle('players')
myteam = team.readPickle('teams')[MYTEAMID]

#get only first 24 players
mystarters = myteam['team_roster'][:24]

#interesting stats in order of descending importance
st = [1,2,4,14,5,31,32]

def test(stat,time):
    mystats = team.calcTeamStats(mystarters, stat, players, time)
    head = team.statidHeader(stat)
    t1,f1=genetic.run(mystarters,TeamsToInclude=[0,MYTEAMID],StatsToMaximize=stat,
                        TimeFrame=time, Population=1000, Generations=60)
    print('\n\n\n\n\n\n\n')

    [print(head[i],mystats[i]) for i in range(len(head))]
    print()

    gastats = team.calcTeamStats(t1, stat, players, time)
    [print(head[i],gastats[i]) for i in range(len(head))]

    m = set(mystarters)
    g = set(t1)

    k = m&g
    d = m-g
    u = g-m

    print('\nKeep:')
    for x in k:
      p = players[x]
      print(p['stats_percentown'],p['stats_percentowndelta'],p['player_name'],p['position_eligible'])
    print('\nDrop:')
    for x in d:
      p = players[x]
      print(p['stats_percentown'],p['stats_percentowndelta'],p['player_name'],p['position_eligible'])
    print('\nPickup:')
    for x in u:
      p = players[x]
      print(p['stats_percentown'],p['stats_percentowndelta'],p['player_name'],p['position_eligible'])

    mystats = team.calcTeamStats(mystarters, st, players, time)
    gastats = team.calcTeamStats(t1, st, players, time)
    print (gastats)
    print (mystats)
    print (len(mystats))
    print ( sum( [a/b for a,b in zip(gastats,mystats)] ) )

test(st, 'stats_lastmonth')
