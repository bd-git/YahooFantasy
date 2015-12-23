import random
import pickle
from copy import deepcopy

def readPickle(filename):
        filename=filename+'.pickle'
        with open(filename,'rb') as f:
                data = pickle.load(f)
        return data

def makePositionList(pos, playersdic, listofteamstoinclude=[i for i in range(0,13)]):
    #injured = ['NA','IR','IR+']
    injured = ['DUMMY']
    plist=[]
    for x in playersdic:
       eligible = playersdic[x]['position_eligible']
       leagueteam = playersdic[x]['league_teamid']
       if True in [ (position in injured) for position in eligible ]:
          'Skip Injured'
       elif True not in [ (teamid == leagueteam) for teamid in listofteamstoinclude ]:
          'Skip on on Team'
       elif pos in eligible:
          plist.append(x)
    return plist

def popFromOtherPositionLists(playerid, listOfPositionLists):
   positionLists = listOfPositionLists
   for poslist in positionLists:
      try:
        poslist.pop(poslist.index(playerid))
      except:
        True
   return tuple(positionLists)

def makeRandomTeam(clist, rwlist, lwlist, dlist, NumbersPerPositionAsList ):
   numC,numRW,numLW,numD,numU = NumbersPerPositionAsList
   team=[]
   c = deepcopy(clist)
   rw = deepcopy(rwlist)
   lw = deepcopy(lwlist)
   d = deepcopy(dlist)
   random.seed()

   for i in range(numC):
      newplayer = c.pop(random.randint(0,len(c)-1))
      rw,lw,d = popFromOtherPositionLists(newplayer,[rw,lw,d])
      team.append(newplayer)
   for i in range(numRW):
      newplayer = rw.pop(random.randint(0,len(rw)-1))
      c,lw,d = popFromOtherPositionLists(newplayer,[c,lw,d])
      team.append(newplayer)
   for i in range(numLW):
      newplayer = lw.pop(random.randint(0,len(lw)-1))
      c,rw,d = popFromOtherPositionLists(newplayer,[c,rw,d])
      team.append(newplayer)
   for i in range(numD):
      newplayer = d.pop(random.randint(0,len(d)-1))
      c,rw,lw = popFromOtherPositionLists(newplayer,[c,rw,lw])
      team.append(newplayer)
   u=list(set(c+lw+rw+d))
   for i in range(numU):
      newplayer = u.pop(random.randint(0,len(u)-1))
      team.append(newplayer)

   return team

def statidHeader(listofstatids):
   header=[]
   l = readPickle('leaguedata')
   for id in listofstatids:
     for name in l:
       if l[name]==id:
         header.append(name)
   #print(header)
   return header

def playerNames(listofplayerids,playerdic):
   players=[]
   for id in listofplayerids:
     players.append(playerdic[id]['player_name'])
     #print(playerdic[id]['player_name'],playerdic[id]['position_eligible'])
   return players

def calcTeamStats(TeamAsList, StatCatsAsList, PlayersAsDic, TimeFrame):
   individual = TeamAsList
   stats = StatCatsAsList
   p = PlayersAsDic
   listOfPlayerStatsForIndividual = [[p[player][TimeFrame][statid] for statid in stats]for player in individual]
   combinedStatsForIndividual = tuple([sum(totalstats) for totalstats in zip(*listOfPlayerStatsForIndividual)])
   return combinedStatsForIndividual
