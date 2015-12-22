import random
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import team

playersDic = team.readPickle('players')
teamsToInclude=[0,6]
rwList = team.makePositionList('RW',playersDic,teamsToInclude)
lwList = team.makePositionList('LW',playersDic,teamsToInclude)
cList = team.makePositionList('C',playersDic,teamsToInclude)
dList = team.makePositionList('D',playersDic,teamsToInclude)
statsToMaximize = [14,16,1,2,31,32]

#Define Player and Player's Fitness
creator.create("FitnessMax", base.Fitness, weights=tuple([1.0]*len(statsToMaximize)) )
creator.create("Team", list, fitness=creator.FitnessMax)

#Register Player Operations
def generateTeam(c,rw,lw,d):
   return creator.Team(team.makeRandomTeam(c,rw,lw,d))

def evalTeamFitness(individual):
   listOfPlayerStatsForIndividual = [[playersDic[player]['stats_lastmonth'][statid] for statid in statsToMaximize]for player in individual]
   combinedStatsForIndividual = tuple([sum(totalstats) for totalstats in zip(*listOfPlayerStatsForIndividual)])
   return combinedStatsForIndividual

toolbox = base.Toolbox()
toolbox.register("genteam", generateTeam, c=cList, rw=rwList, lw=lwList, d=dList)
#toolbox.register("individual", tools.initRepeat, creator.Team, toolbox.genteam, n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.genteam)

toolbox.register("evaluate", evalTeamFitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selBest)

def main():
    random.seed()

    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40,  halloffame=hof, verbose=True)
    print(pop[0].fitness)
    print(pop[1].fitness)
    print(pop[2].fitness)

if __name__ == "__main__":
    main()
