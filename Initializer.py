import random

from deap import creator

import Constants


def generateIndividual(colors):
    index = counter(colors)
    r, g, b = colors[index.counter]
    index.increment()
    tmp = [r, g, b]
    for i in range(0, 3):
        low = 0 if tmp[i] - Constants.THRESHOLD < 0 else tmp[i] - Constants.THRESHOLD
        up = 255 if tmp[i] + Constants.THRESHOLD > 255 else tmp[i] + Constants.THRESHOLD
        tmp[i] = random.randrange(low, up)
    color = (tmp[0], tmp[1], tmp[2])
    return color


class counter:
    def __init__(self, colori):
        self.colori = colori
        self.counter = 0

    def increment(self):
        self.counter = (self.counter + 1) % len(self.colori)


def mutate(individuo, indpb):
    delta = Constants.DELTA
    n_mutations = random.randint(1, int(len(individuo) / 10))
    perturbazione = random.randint(-delta, delta)
    for i in range(0, n_mutations):
        gene_index = random.randint(0, len(individuo) - 1)
        tmp = [0, 0, 0]
        if random.random() < indpb:
            r, g, b = individuo[gene_index]
            # print("Gene vecchio: ", r, g, b)
            tmp[0] = r + perturbazione if 0 <= r + perturbazione <= 255 else random.randrange(0, 255)
            tmp[1] = g + perturbazione if 0 <= g + perturbazione <= 255 else random.randrange(0, 255)
            tmp[2] = b + perturbazione if 0 <= b + perturbazione <= 255 else random.randrange(0, 255)
            # print("Gene nuovo: ", tmp[0], tmp[1], tmp[2])
            individuo[gene_index] = tuple(tmp)

    return individuo,


def onePointCrossover(ind1, ind2):
    off1 = ind1
    off2 = ind2
    if random.random() < Constants.P_CROSSOVER:
        indLen = len(ind1)
        crossoverPoint = random.randint(0, indLen - 1)
        for i in range(crossoverPoint, indLen):
            off1[i], off2[i] = ind2[i], ind1[i]
    return off1, off2


def extractNodes(root):
    nodesMap = {}
    for elem in root.iter():
        if elem not in nodesMap:
            nodesMap[elem] = elem.items()
    return nodesMap
