import random
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from copy import deepcopy
import team

def run(
             BenchmarkTeam,
             StatsToMaximize,
             TeamsToInclude=[x for x in range(1,13)],
             Population=1000,
             Generations=60,
             PlayersDictionary = team.readPickle('players'),
             NumbersPerPositionAsList = [5,5,5,6,3],
             TimeFrame = 'stats_lastmonth'
            ):
   playersDic = PlayersDictionary
   rwList = team.makePositionList('RW',playersDic,TeamsToInclude)
   lwList = team.makePositionList('LW',playersDic,TeamsToInclude)
   cList = team.makePositionList('C',playersDic,TeamsToInclude)
   dList = team.makePositionList('D',playersDic,TeamsToInclude)

   creator.create("FitnessMax", base.Fitness, weights=(1.0,) )
   #creator.create("FitnessMax", base.Fitness, weights=tuple( [x/10 for x in range(10,(10-len(StatsToMaximize)),-1)] ) )
   creator.create("Team", list, fitness=creator.FitnessMax)

   toolbox = base.Toolbox()
   toolbox.register("genteam", generateTeam, c=cList, rw=rwList, lw=lwList, d=dList, npos=NumbersPerPositionAsList)
   toolbox.register("population", tools.initRepeat, list, toolbox.genteam)
   toolbox.register("evaluate", evalTeamFitness, BT=BenchmarkTeam, stats=StatsToMaximize, p=playersDic, time=TimeFrame)
   toolbox.register("mate", tools.cxTwoPoint)
   toolbox.register("mutate", mutateTeam, indpb=0.05, c=cList, rw=rwList, lw=lwList, d=dList, npos=NumbersPerPositionAsList)
   #toolbox.register("select", tools.selNSGA2)
   toolbox.register("select", tools.selTournament, tournsize=10)
   toolbox.decorate("mate", checkCrossover(c=cList, rw=rwList, lw=lwList, d=dList, npos=NumbersPerPositionAsList))

   random.seed()
   pop = toolbox.population(n=Population)
   hof = tools.HallOfFame(1)
   algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=Generations,  halloffame=hof, verbose=True)

   return( hof[0] , hof[0].fitness.values )

def generateTeam(c,rw,lw,d,npos):
   x=creator.Team(team.makeRandomTeam(c,rw,lw,d,npos))
   return x

def evalTeamFitness(individual, BT, stats, p, time):
   i = team.calcTeamStats(individual,stats,p,time)
   BT = team.calcTeamStats(BT,stats,p,time)
   i[stats.index(31)]=i[stats.index(31)]+800
   i[stats.index(32)]=i[stats.index(32)]+800
   i[stats.index(4)]=i[stats.index(4)]+100
   i[stats.index(1)]=i[stats.index(1)]+5
   BT[stats.index(31)]=BT[stats.index(31)]+800
   BT[stats.index(32)]=BT[stats.index(32)]+800
   BT[stats.index(4)]=BT[stats.index(4)]+100
   BT[stats.index(1)]=BT[stats.index(1)]+5
   x= tuple( [a/b for a,b in zip(i,BT)] )
   if 0.0 in x:
     print(x)
     input()
   #return tuple( [a/b for a,b in zip(i,BT)] )
   return sum([a/b for a,b in zip(i,BT)])-len(stats),

def mutateTeam(individual,indpb,c,rw,lw,d,npos):
    newteam = generateUniqueTeam([individual],c,rw,lw,d,npos)
    size = len(individual)

    for i in range(size):
        if random.random() < indpb:
          individual[i]=newteam[i]
    return individual,

def generateUniqueTeam(individuals,c,rw,lw,d,npos):
    cm=deepcopy(c)
    rm=deepcopy(rw)
    lm=deepcopy(lw)
    dm=deepcopy(d)
    for t in individuals:
       for player in t:
          cm,rm,lm,dm=team.popFromOtherPositionLists(player,[cm,rm,lm,dm])
    return generateTeam(cm,rm,lm,dm,npos)

def checkCrossover(c,rw,lw,d,npos):
    Expected = sum(npos)
    def decorator(func):
        def wrapper(*args, **kargs):
            off1,off2 = func(*args, **kargs)
            # if first crossover produced duplicates, perform until no duplicates
            while(not (len(set(off1))==Expected and len(set(off2))==Expected)):
               off1,off2 = func(*args, **kargs)
            return (off1,off2)
        return wrapper
    return decorator

