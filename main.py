import os
import pickle
import time

import Algorithm
import seaborn as sns
from matplotlib import pyplot as plt
import Constants
import Utilities
from Constants import *
import Test
from DistanceTest import testResults


def saveOriginalColors(colors, path):
    with open(path, "w") as f:
        for color in colors:
            f.write(str(color))
            f.write("\n")


def main():
    population, logbook, elapsed_time, hof, image = Algorithm.start()
    print("Elapsed time: ", elapsed_time)
    print("Hall of Fame Individuals = ", *hof.items, sep="\n")
    print("Best Ever Individual = ", hof.items[0])
    contrast, similarity, colors = Algorithm.getCost(hof[0])
    # similarity, colors = Algorithm.getCost(hof[0])
    # contrast = Algorithm.getCost(hof[0])
    # colors = Algorithm.getCost(hof[0])
    print("Contrast: ", contrast)
    print("Similarity:", similarity)
    print("Colors: ", colors)
    maxFitnessValues, minFitnessValues, meanFitnessValues = logbook.select("max", "min", "avg")
    # maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")
    sns.set_style("whitegrid")
    plt.plot(maxFitnessValues, color='red')
    plt.plot(minFitnessValues, color='yellow')
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Generation')
    plt.ylabel('Max / Min/ Average Fitness')
    plt.title('Max, Min and Average Fitness over Generations')
    plt.show()

    with open(RESULTCOUNTERPATH, 'rb') as file:
        counter = pickle.load(file)
    counter += 1
    with open(RESULTCOUNTERPATH, 'wb') as file:
        pickle.dump(counter, file)

    image.show()
    imageName = RESULTPATH + ACTUALIMG.split(".")[0] + "_" + str(counter) + ".png"
    image.save(imageName)
    bocpPath, boccPath = PATHTOBOCPBOCC + ACTUALBOCP, PATHTOBOCPBOCC + ACTUALBOCC
    bocp, bocc = Utilities.openBocc(bocpPath, boccPath)
    saveOriginalColors(list(bocp.keys()), Constants.ORIGINALCOLORSFILEPATH)
    os.system("node .\\Automated_tests\\main.js")
    time.sleep(5)
    jsOutputFile = open("js_output.txt", 'r')
    jsResults = []
    for line in jsOutputFile:
        jsResults.append((line[1: len(line) - 2].split(",")))


if __name__ == '__main__':
    # Test.test()
    # Test.start()
    main()
