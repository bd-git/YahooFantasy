###
'''

TODO? put this somewherein:
from time import localtime, strftime
strftime("%Y%m%d_%H%M%S", localtime())

'''
##


## = changes added by brian
import auth
import datetime
import query

y = auth.yahoo_session()

yahoo_game = [
    {'gameid': 352, 'leagueid': 59140},
]

leagues = []
teams = []
rosters = []

for i in yahoo_game:
    #get league data
    league_code = query.make_league_code(i['gameid'], i['leagueid'])
    league_url = query.league_data(league_code)
    l = auth.api_query(y, league_url)

    #grab relevant part of dict
    this_league = l['fantasy_content']['league']
    leagues.append(this_league)

    player_dict={}

    # Get All Taken Players
    loopcount=0
    while(True):
       # 2 Gets: first = 1 for seas+pct
       #         secnd = 2 for lastmonth 
       GET1 = auth.api_query(y, query.getdata(league_url,loopcount,1,status="T"))
       GET2 = auth.api_query(y, query.getdata(league_url,loopcount,2,status="T"))
       num_players_returned = int(GET1['fantasy_content']['league']['players']['@count'])

       # Relevent part of get
       GET_SEA = GET1['fantasy_content']['league']['players']['player']
       GET_LM  = GET2['fantasy_content']['league']['players']['player']

       for count in range(0,num_players_returned):
          # Create player 'object' using player information (name, etc) from one of the gets
          # createplayer( x, True) --- True = Taken/NonFreeAgent
          new_player = query.createplayer(GET_SEA[count], True)

          # Update new player with Season Stats from get
          # Update new player with LMonth Stats from get
          # Add new player to player dictionary
          new_player = query.updateplayerstat(new_player ,GET_SEA[count])
          new_player = query.updateplayerstat(new_player ,GET_LM[count])
          player_dict[int(new_player['player_id'])] = new_player

       loopcount+=25

       if (num_players_returned<25):
          break

    # Get Top 200 Free Agent Players
    loopcount=0
    while(True):
       GET1 = auth.api_query(y, query.getdata(league_url,loopcount,1,status="A"))
       GET2 = auth.api_query(y, query.getdata(league_url,loopcount,2,status="A"))
       GET_SEA = GET1['fantasy_content']['league']['players']['player']
       GET_LM  = GET2['fantasy_content']['league']['players']['player']

       for count in range(0,25):
          new_player = query.createplayer(GET_SEA[count])
          new_player = query.updateplayerstat(new_player, GET_SEA[count])
          new_player = query.updateplayerstat(new_player, GET_LM[count])
          player_dict[int(new_player['player_id'])] = new_player

       loopcount+=25
       if loopcount==200:
          break

auth.data_pickle(
    filename="players.pickle",
    data=player_dict
)
