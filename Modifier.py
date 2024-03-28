from PIL import Image, ImageDraw
import Constants
import colorsys


def getIndex(oldColors, color):
    for i in range(0, len(oldColors)):
        if oldColors[i] == color:
            return i
    return 0

def changeColors(bocp, oldColors, newColors, img):
    draw = ImageDraw.Draw(img)
    x, y = img.size
    for color, pixelList in bocp.items():
        index = getIndex(oldColors, color)
        for p in pixelList:
            n, xp, yp = p
            draw.point((xp, yp), fill=newColors[index])
    return img
