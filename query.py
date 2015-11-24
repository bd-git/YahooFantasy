def make_league_code(gameid, leagueid):
    return str(gameid) + '.l.' + str(leagueid)

def make_team_code(leaguecode, teamid):
    return  leaguecode + '.t.' + str(teamid)

def league_data(league_code):
    return "http://fantasysports.yahooapis.com/fantasy/v2/league/" + league_code

def team_data(team_code):
    return "http://fantasysports.yahooapis.com/fantasy/v2/team/" + team_code + ";out=metadata,stats"

def roster_data(team_code):
    return "http://fantasysports.yahooapis.com/fantasy/v2/team/" + team_code + "/roster"

def createteam(team):
   newtm = {
    'key':team['team_key'],
    'id':team['team_id'],
    'name':team['name'],
    'stats':False,
    'roster':False
   }
   return (newtm['id'],newtm)

def createplayer(player,isTaken=False):
   newpl = {
    'key':player['player_key'],
    'id':player['player_id'],
    'name':player['name']['full'],
    'edkeyPlayer':player['editorial_player_key'],
    'edkeyTeam':player['editorial_team_key'],
    'edkeyTeamDisp':player['editorial_team_abbr'],
    'postype':player['position_type'],
    'poseligible':player['eligible_positions']['position'],
    'statsLM':False,
    'statsSEA':False,
    'pctown':False,
    'pctdelta':False,
    'istaken':isTaken
   }
   return [newpl['id'],newpl]

def updateplayerstat(player, stats):
   try:
      if stats['player_stats']['coverage_type']=='season' and player['statsSEA']==False:
         player['statsSEA']=parseplayerstat(stats['player_stats']['stats']['stat'])
   except:
      True
   try:
       if stats['player_stats']['coverage_type']=='lastmonth' and player['statsLM']==False:
         player['statsLM']=parseplayerstat(stats['player_stats']['stats']['stat'])
   except:
      True
   try:
      if stats['percent_owned'] and player['pctown']==False:
        player['pctown']=stats['percent_owned']['value']
        player['pctdelta']=stats['percent_owned']['delta']
   except:
      True 
   return(player)

def parseplayerstat(player_stats_stats_stat):
   playerstats=player_stats_stats_stat
   statdict={}
   for x in playerstats:
       statdict[x['stat_id']]=x['value']
   return statdict

def parse_settings(sets):
   for x in sets:
        print(x['name']+','+x['stat_id'])
        print('')


   """
SORT
{stat_id} (statid integer)...NAME (last, first)...OR (overall rank)...AR (actual rank)...PTS (fantasy points)
SORT_TYPE
season...date...lastweek...lastmonth
SORT_DATE (if SORT_TYPE = date)
YYYY-MM-DD (/players;sort_type=date;sort_date=2010-02-01)
STATUS
A (all available players)...FA (free agents only)...W (waivers only)...T (all taken players)...K (keepers onl$
POSITION
G Goalie...P D/C/LW/RW
   """

def getdata(league_url,start,output,sortby="lastmonth",position="P",status="A"):
    """ 
Get data for multiple players

Args:
	leauge_url (string): generated league url
	start (int): index at which to start player list
	output (int): type of desired output:
		1 - season stats + percent_owned
		2 - last month stats
		3 - percent_owned
		4 - season stats
	sortby (Optional str): timeframe category for which to sort on
	position (Optional str): P or G typically
	status (Optional str): select player pool to search on (ie A = all available players, T = unavailable players, etc)

Returns:
	Ordered Dict if successful
   """
    options = {
    1:";out=percent_owned,stats",
    2:"/stats;type=lastmonth",
    3:"/percent_owned",
    4:"/stats"
    }
    return league_url+"/players;sort=AR;sort_type=" + sortby + ";start=" + str(start) + ";position=" + position + ";status=" + status + options[output]

