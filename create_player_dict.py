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
    #settings = league_url+"/settings"
    #settings = auth.api_query(y, settings)
    #parse_settings(settings['fantasy_content']['league']['settings']['stat_categories']['stats']['stat'])
    l = auth.api_query(y, league_url)

    #grab relevant part of dict
    this_league = l['fantasy_content']['league']
    leagues.append(this_league)

    player_dict={}

    # Get All Taken Players
    loopcount=0
    while(True):
       GET1 = auth.api_query(y, query.getdata(league_url,loopcount,1,status="T"))
       GET2 = auth.api_query(y, query.getdata(league_url,loopcount,2,status="T"))
       num_players_returned = int(GET1['fantasy_content']['league']['players']['@count'])
       for count in range(0,num_players_returned):
          player = query.createplayer(GET1['fantasy_content']['league']['players']['player'][count],True)
          player_dict[player[0]] = player[1]
          player_dict[player[0]] = query.updateplayerstat(player_dict[player[0]],GET1['fantasy_content']['league']['players']['player'][count])
          player_dict[player[0]] = query.updateplayerstat(player_dict[player[0]],GET2['fantasy_content']['league']['players']['player'][count])
       loopcount+=25

       if (num_players_returned<25):
          break

    # Get Top 200 Free Agent Players
    loopcount=0
    while(True):
       GET1 = auth.api_query(y, query.getdata(league_url,loopcount,1,status="A"))
       GET2 = auth.api_query(y, query.getdata(league_url,loopcount,2,status="A"))
       for count in range(0,25):
          player = query.createplayer(GET1['fantasy_content']['league']['players']['player'][count])
          player_dict[player[0]] = player[1]
          player_dict[player[0]] = query.updateplayerstat(player_dict[player[0]],GET1['fantasy_content']['league']['players']['player'][count])
          player_dict[player[0]] = query.updateplayerstat(player_dict[player[0]],GET2['fantasy_content']['league']['players']['player'][count])
       loopcount+=25
       if loopcount==200:
          break


auth.data_pickle(
    filename="players.pickle",
    data=player_dict
)
