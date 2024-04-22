import math

import Constants


def euclideanDistance(jsColor, gaColor):
    r1, g1, b1 = jsColor
    r2, g2, b2 = gaColor
    dx, dy, dz = r2 - r1, g2 - g1, b2 - b1
    sum_of_squares = dx ** 2 + dy ** 2 + dz ** 2
    return math.sqrt(sum_of_squares)


def calculateDistances(jsResult, gaResult):
    if len(jsResult) != len(gaResult):
        return -1
    distances = []
    for i in range(len(jsResult)):
        js = map(int, jsResult[i])
        ga = map(int, gaResult[i])
        distances.append(euclideanDistance(js, ga))
    return distances


def testResults(jsResult, gaResult):
    file = open(Constants.TESTRESULTSFILEPATH, "w")
    testResult = calculateDistances(jsResult, gaResult)
    if testResult == -1:
        msg = "Qualcosa è andato storto"
        file.write(msg)
    else:
        avg = sum(testResult) / len(testResult)
        msg = "DISTANCES: " + str(testResult) + " \n "
        msg += "AVG: " + str(avg)
        file.write(msg)
