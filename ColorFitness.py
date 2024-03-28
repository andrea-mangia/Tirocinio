import colorsys


"""def getOldColorFitness(individual, bocc):
    blueCounter = 0
    originalColors = list(bocc.keys())
    for i, gene in enumerate(individual):
        r, g, b = gene
        # if b > r and b > g and b > 180:
        if b > 180 and b > r and b > g:
            blueCounter += len(bocc.get(originalColors[i]))
        if r + g > 350 and abs(r - g) < 50:
            yellowCounter += len(bocc.get(originalColors[i]))
    return blueCounter"""


def rgbToHsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    hsv = colorsys.rgb_to_hsv(r, g, b)
    h, s, v = (hsv[0] * 360, hsv[1] * 100, hsv[2] * 100)
    return h, s, v


def getColorFitness(individual, bocc):
    blueCounter = 0
    originalColors = list(bocc.keys())
    for i, gene in enumerate(individual):
        r, g, b = gene
        h, s, v = rgbToHsv(r, g, b)
        if h >= 200 and s >= 40 and v >= 40:
            if h >= 240 and s >= 50 and v >= 50:
                penalty = 10
            else:
                penalty = 1
            blueCounter += len(bocc.get(originalColors[i])) * penalty
    return blueCounter
