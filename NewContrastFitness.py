import ContrastFitness5


def getOldNewContrast(colors):
    totContrast = 0
    for i in range(0, len(colors)):
        for j in range(i+1, len(colors)):
            totContrast += ContrastFitness5.getContrast(colors[i], colors[j])
    return totContrast


def checkParents(i, j, colorsMap, bocc):
    originalColors = list(bocc.keys())
    c1 = originalColors[i]
    c2 = originalColors[j]
    if colorsMap.get(c1) == c2:
        return True
    elif colorsMap.get(c2) == c1:
        return True
    return False


def getNewContrast(colors, colorsMap, bocc):
    totContrast = 0
    for i in range(0, len(colors)):
        for j in range(i+1, len(colors)):
            contrast = ContrastFitness5.getContrast(colors[i], colors[j])
            if ContrastFitness5.getContrast(colors[i], colors[j]) < 125:
                if checkParents(i, j, colorsMap, bocc):
                    contrast = contrast * -5
                else:
                    contrast *= -2
            totContrast += contrast
    return totContrast