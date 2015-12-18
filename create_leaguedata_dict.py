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
league_data=''

for i in yahoo_game:
    #get league data
    league_code = query.make_league_code(i['gameid'], i['leagueid'])
    league_url = query.league_data(league_code)
    settings = league_url+"/settings"
    settings = auth.api_query(y, settings)
    league_data = query.parse_settings(settings['fantasy_content']['league']['settings']['stat_categories']['stats']['stat'])

auth.data_pickle(
    filename="leaguedata.pickle",
    data=league_data
)
