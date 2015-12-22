import random
import pickle
from copy import deepcopy

def readPickle(filename):
        filename=filename+'.pickle'
        with open(filename,'rb') as f:
                data = pickle.load(f)
        return data

def makePositionList(pos, playersdic, listofteamstoinclude=[i for i in range(0,13)]):
    injured = ['NA','IR','IR+']
    plist=[]
    for x in playersdic:
       eligible = playersdic[x]['position_eligible']
       leagueteam = playersdic[x]['league_teamid']
       if True in [ (position in injured) for position in eligible ]:
          continue
       elif True not in [ (teamid == leagueteam) for teamid in listofteamstoinclude ]:
          continue
       else:
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

def makeRandomTeam(clist, rwlist, lwlist, dlist, numC=5,numRW=5,numLW=5,numD=6,numU=3):
   team=[]
   c = deepcopy(clist)
   rw = deepcopy(rwlist)
   lw = deepcopy(lwlist)
   d = deepcopy(dlist)
   random.seed()

   for i in range(numC):
      newplayer = c.pop(random.randint(0,len(c)-1))
      rw,lw = popFromOtherPositionLists(newplayer,[rw,lw])
      team.append(newplayer)
   for i in range(numRW):
      newplayer = rw.pop(random.randint(0,len(rw)-1))
      c,lw = popFromOtherPositionLists(newplayer,[c,lw])
      team.append(newplayer)
   for i in range(numLW):
      newplayer = lw.pop(random.randint(0,len(lw)-1))
      c,rw = popFromOtherPositionLists(newplayer,[c,rw])
      team.append(newplayer)
   for i in range(numD):
      newplayer = d.pop(random.randint(0,len(d)-1))
      team.append(newplayer)
   u=list(set(c+lw+rw+d))
   for i in range(numU):
      newplayer = u.pop(random.randint(0,len(u)-1))
      team.append(newplayer)

   return team

#team = makeRandomTeam(c,rw,lw,d)

#for x in team:
#  print(p[x]['player_name'],p[x]['position_eligible'])

