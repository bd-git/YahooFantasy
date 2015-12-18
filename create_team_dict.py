## = changes added by brian
import auth
import datetime
import query

y = auth.yahoo_session()

yahoo_game = [
    {'gameid': 352, 'leagueid': 59140},
]

teams = {}

for i in yahoo_game:
    #get league data
    league_code = query.make_league_code(i['gameid'], i['leagueid'])
    league_url = query.league_data(league_code)
    l = auth.api_query(y, league_url)

    #grab relevant part of dict
    this_league = l['fantasy_content']['league']

    #iterate over teams
    num_teams = int(this_league['num_teams'])
    for j in range(1, num_teams + 1):
        #get basic team data
        team_code = query.make_team_code(league_code, j)
        t = auth.api_query(y, query.team_data(team_code))
        #just relevant response
        this_team = t['fantasy_content']['team']

        r = auth.api_query(y, query.roster_data(team_code))
        this_roster = r['fantasy_content']['team']['roster']['players']['player']
        length = len(this_roster)
        players = []
        for i in range(0,length):
           players.append(int(this_roster[i]['player_id']))
        dic = query.createteam(this_team)
        dic['team_roster']=players
        dic['team_stats']=query.parseplayerstat(this_team['team_stats']['stats']['stat'])
        teams[int(dic['team_id'])]=dic


auth.data_pickle(
    filename="teams.pickle",
    data=teams
)
