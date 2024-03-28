import ImageUtilities
import Initializer
import cProfile
import pickle
import random
import time
import xml.etree.ElementTree as ET
import seaborn as sns
from Constants import *
import numpy
from PIL import Image
from deap import base, creator, algorithms, tools
from matplotlib import pyplot as plt

import Utilities
import elitism
from Tritanopia import Tritanopia
import Constants
import Modifier


random.seed(80)
toolbox = base.Toolbox()
bocpPath, boccPath = PATHTOBOCPBOCC + ACTUALBOCP, PATHTOBOCPBOCC + ACTUALBOCC
bocp, bocc = Utilities.openBocc(bocpPath, boccPath)
img_path = PATHTOIMGSNAPSHOT + ACTUALIMG
img = Image.open(img_path)
snap_path = PATHTOIMGSNAPSHOT + ACTUALSNAPSHOT
root = ET.parse(snap_path).getroot()
nodesMap = Initializer.extractNodes(root)
problem = Tritanopia(bocc, bocp, img, root)
#creator.create("FitnessMulti", base.Fitness, weights=(1.0,))
#creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -0.8))
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -0.5, -0.8))
creator.create("Individual", list, fitness=creator.FitnessMulti)
toolbox.register("similarColors", Initializer.generateIndividual, list(bocc.keys()))
toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.similarColors, len(bocc.keys()))
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)


def getCost(individual):
    return problem.evaluate(individual)


toolbox.register("evaluate", getCost)
toolbox.register("select", tools.selTournament, tournsize=10)
toolbox.register("mate", Initializer.onePointCrossover)
toolbox.register("mutate", Initializer.mutate, indpb=1 / len(bocc.keys()))


def start():
    population = toolbox.populationCreator(n=Constants.POPULATION_SIZE)
    contrast_stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    similarity_stats = tools.Statistics(lambda ind: ind.fitness.values[1])
    # CAMBIARE values[0] in values[2]
    colors_stats = tools.Statistics(lambda ind: ind.fitness.values[2])
    stats = tools.MultiStatistics(contrast=contrast_stats, similarity=similarity_stats, colors=colors_stats)
    #stats = tools.MultiStatistics(similarity=similarity_stats, colors=colors_stats)
    # stats = tools.MultiStatistics(colors=colors_stats)
    #stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", numpy.max, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("avg", numpy.mean, axis=0)
    hof = tools.HallOfFame(Constants.HALL_OF_FAME_SIZE)
    start_time = time.perf_counter()
    population, logbook = elitism.eaSimpleWithElitism(population=population, toolbox=toolbox,
                                                      cxpb=Constants.P_CROSSOVER,
                                                      mutpb=Constants.P_MUTATION, ngen=Constants.MAX_GENERATIONS,
                                                      stats=stats,
                                                      verbose=True, halloffame=hof)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    image = ImageUtilities.buildImage(img_path, snap_path, list(bocp.keys()), hof.items[0], 0)
    return population, logbook, elapsed_time, hof, image
