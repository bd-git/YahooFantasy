## = changes added by brian
import auth
import datetime

y = auth.yahoo_session()

def make_league_code(gameid, leagueid):
    return str(gameid) + '.l.' + str(leagueid)

def make_team_code(gameid, leagueid, teamid):
    return str(gameid) + '.l.' + str(leagueid) + '.t.' + str(teamid)

def league_data(league_code):
    return "http://fantasysports.yahooapis.com/fantasy/v2/league/" + league_code

def team_data(team_code):
    return "http://fantasysports.yahooapis.com/fantasy/v2/team/" + team_code + ";out=metadata,stats"

def roster_data(team_code):
    return "http://fantasysports.yahooapis.com/fantasy/v2/team/" + team_code + "/roster"

def player_stats_data(player_key):
    return "http://fantasysports.yahooapis.com/fantasy/v2/player/" + player_key + ";out=stats,percent_owned"

def player_search(league_url,start,position="P",status="A"):
    return league_url+"/players;sort=OR;sort_type=season;start=" + str(start) + ";position=" + position + ";status=" + status

def update_player_data(AUTH, player, team_code):
    player_stat_url = player_stats_data(player['player_key'])
    player_data = auth.api_query(AUTH, player_stat_url)
    player['queried_stats'] = player_data['fantasy_content']['player']['player_stats']
    player['percent_owned'] = player_data['fantasy_content']['player']['percent_owned']
    player['team_code'] = team_code
    return player

    

hpk = [
    #NHL2014;109glen
    #{'gameid': 341, 'leagueid': 62035},
    #NHL2015;109glen
    {'gameid': 352, 'leagueid': 59140},
]

leagues = []
teams = []
rosters = []

for i in hpk:
    #get league data
    league_code = make_league_code(i['gameid'], i['leagueid'])
    league_url = league_data(league_code)
    l = auth.api_query(y, league_url)
    #grab relevant part of dict
    this_league = l['fantasy_content']['league']
    leagues.append(this_league)

    print("Getting Top 50 Rated Free Agent Goalies")
    for count in range(0,50,25):
        print("...."+str(count))
        query = player_search(league_url,count,position="G")
        query = auth.api_query(y, query)
        for k in query['fantasy_content']['league']['players']['player']:
            rosters.append(update_player_data(y,k,'FA'))

    auth.data_pickle(filename="goalies.pickle",data=rosters)
    rosters=[]

    print("Getting Top 350 Rated Free Agent Forwards/Defenders")
    for count in range(0,350,25):
        print("...."+str(count))
        query = player_search(league_url,count)
        query = auth.api_query(y, query)
        for k in query['fantasy_content']['league']['players']['player']:
            rosters.append(update_player_data(y,k,'FA'))

    auth.data_pickle(filename="forwards.pickle",data=rosters)
    rosters=[]

    #iterate over teams
    num_teams = int(this_league['num_teams'])
    for j in range(1, num_teams + 1):
        #get basic team data
        team_code = make_team_code(i['gameid'], i['leagueid'], j)
        t = auth.api_query(y, team_data(team_code))
        #just relevant response
        this_team = t['fantasy_content']['team']
        #include season in dict
        this_team['season'] = this_league['season']
        this_team['logo'] = this_team['team_logos']['team_logo']['url']

        #handle co-managers
        this_manager = this_team['managers']['manager']
        if type(this_manager) == list:
            this_manager = this_manager[0]

        this_team['manager_id'] = this_manager['manager_id']

        this_team['manager_nickname'] = this_manager['nickname']
        if 'guid' in this_manager: manager_guid = this_manager['guid']
        if 'guid' not in this_manager: manager_guid = None
        this_team['manager_guid'] = manager_guid
        if 'email' in this_manager: manager_email = this_manager['email']
        if 'email' not in this_manager: manager_email = None
        this_team['manager_email'] = manager_email
        if "is_owned_by_current_login" not in this_team: this_team["is_owned_by_current_login"] = None
        #drop some keys
        this_team.pop("managers", None)
        this_team.pop("team_logos", None)
        this_team.pop("roster_adds", None)

        print ("Getting Player Stats for " + str(this_manager['nickname']) + "'s Roster")
        teams.append(this_team)

        #get team roster
        r = auth.api_query(y, roster_data(team_code))##, last_day))
        this_roster = r['fantasy_content']['team']['roster']['players']['player']
        pcnt = 0
        print(len(this_roster))
        for k in this_roster:
            pcnt +=1
            print(pcnt)
            rosters.append(update_player_data(y,k,team_code))


#write data
auth.data_pickle(
    filename="leagues.pickle",
    data=leagues
)
auth.data_pickle(
    filename="teams.pickle",
    data=teams
)
auth.data_pickle(
    filename="rosters.pickle",
    data=rosters
)

