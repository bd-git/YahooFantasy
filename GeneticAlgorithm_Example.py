# Sample GA program to maximize stats
'''
Program Generates 100 'teams' of 25 'players' who have 3 'stats' each
ie [ [s01,s02,s03], [s11, s12, s13], ... , [s241,s242,s243]
'''

import random
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools


#Define Player and Player's Fitness
creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0, 1.0))
creator.create("Team", list, fitness=creator.FitnessMax)

#Register Player Operations
toolbox = base.Toolbox()

def generateTeam():
   return [random.uniform(0,20),random.uniform(0,700), random.uniform(0,100)]

toolbox.register("GenTeam", generateTeam)
toolbox.register("individual", tools.initRepeat,creator.Team, toolbox.GenTeam, 25 )
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evalTeamFitness(individual):
    return tuple(sum(sublist) for  sublist in zip(*individual))

toolbox.register("evaluate", evalTeamFitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selBest)

def main():
    random.seed()

    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=30,
                                    halloffame=hof, verbose=True)
    print(pop[0].fitness)

if __name__ == "__main__":
    main()
