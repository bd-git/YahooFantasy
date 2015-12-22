import pickle
from auth import data_pickle

def rpick(filename):
        filename=filename+'.pickle'
        with open(filename,'rb') as f:
                data = pickle.load(f)
        return data

teams = rpick('teams')
players = rpick('players')

for team in teams:
    count = 0
    for player in teams[team]['team_roster']:
       try:
          players[player]['league_teamid']=team
       except:
          count+=1

print(str(count)+" players on team rosters not in player dictionary")

data_pickle(players, 'players.pickle')
