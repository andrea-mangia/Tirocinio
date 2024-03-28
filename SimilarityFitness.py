import math


def euclideanDistance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    deltar = (r1 - r2) ** 2
    deltag = (g1 - g2) ** 2
    deltab = (b1 - b2) ** 2
    return math.sqrt(deltar + deltag + deltab)


def getOldSimilarity(oldColors, newColors):
    distances = []
    for i in range(0, len(oldColors)):
        distances.append(euclideanDistance(oldColors[i], newColors[i]))
    minVal = min(distances)
    maxVal = max(distances)
    normalizedDistances = [min_max_normalization(x, minVal, maxVal) for x in distances]
    return sum(normalizedDistances)


def min_max_normalization(x, min_val, max_val):
    return (x - min_val) / (max_val - min_val)


def getSimilarity(oldColors, newColors):
    distances = 0
    for i in range(0, len(oldColors)):
        distances += euclideanDistance(oldColors[i], newColors[i])
    return distances
