import random
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import team

def run(
             TeamsToInclude=[x for x in range(1,13)],
             Population=300,
             Generations=40,
             StatsToMaximize = [14,16,1,2,31,32],
             PlayersDictionary = team.readPickle('players')
            ):
   playersDic = PlayersDictionary
   rwList = team.makePositionList('RW',playersDic,TeamsToInclude)
   lwList = team.makePositionList('LW',playersDic,TeamsToInclude)
   cList = team.makePositionList('C',playersDic,TeamsToInclude)
   dList = team.makePositionList('D',playersDic,TeamsToInclude)

   creator.create("FitnessMax", base.Fitness, weights=tuple([1.0]*len(StatsToMaximize)) )
   creator.create("Team", list, fitness=creator.FitnessMax)

   toolbox = base.Toolbox()
   toolbox.register("genteam", generateTeam, c=cList, rw=rwList, lw=lwList, d=dList)
   toolbox.register("population", tools.initRepeat, list, toolbox.genteam)
   toolbox.register("evaluate", evalTeamFitness, stats=StatsToMaximize, p=playersDic)
   toolbox.register("mate", tools.cxTwoPoint)
   toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
   toolbox.register("select", tools.selBest)

   random.seed()
   pop = toolbox.population(n=Population)
   hof = tools.HallOfFame(1)
   algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=Generations,  halloffame=hof, verbose=True)

   return( hof[0] , hof[0].fitness.values , team.playerNames(hof[0],playersDic) , team.statidHeader(StatsToMaximize) )

def generateTeam(c,rw,lw,d):
   return creator.Team(team.makeRandomTeam(c,rw,lw,d))

def evalTeamFitness(individual, stats, p):
   listOfPlayerStatsForIndividual = [[p[player]['stats_lastmonth'][statid] for statid in stats]for player in individual]
   combinedStatsForIndividual = tuple([sum(totalstats) for totalstats in zip(*listOfPlayerStatsForIndividual)])
   return combinedStatsForIndividual

