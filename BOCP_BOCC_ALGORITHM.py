import itertools
import xml.etree.ElementTree as ET
from PIL import Image
import pandas as pd
import re

import ImageUtilities


def getComponents(root):
    data = []
    for elem in root.iter():
        data.append(elem)
    return data


def checkPixel(pixel_x, pixel_y, pixel_int):
    pixel = (pixel_x, pixel_y)
    if pixel_int.get(pixel) is None:
        pixel_int.setdefault(pixel, [])
        return True
    return False


def getColor(S, x, y):
    return S.getpixel((x, y))


def getPixels(screenshot, c_item, pixel_interface, type):
    # takes ranges based on type and split it
    values = re.findall(r'\d+', c_item[16][1])
    component = c_item[3][1]
    if type == 1:
        values = re.findall(r'\d+', c_item[17][1])
        component = c_item[4][1]
    asse_x_inizio = int(values[0])
    asse_y_inizio = int(values[1])
    asse_x_fine = int(values[2])
    asse_y_fine = int(values[3])
    result = []
    list_color = []
    list_x = []
    list_y = []
    list_component = []
    # iterate x axis
    for x in range(asse_x_inizio, asse_x_fine):
        list_x.append(x)
    # iterate y axis
    for y in range(asse_y_inizio, asse_y_fine):
        list_y.append(y)
        # makes the Cartesian product, takes all the colors according to the axes and assigns the component to the pixels
    for element in itertools.product(list_x, list_y):
        if checkPixel(element[0], element[1], pixel_interface):
            result.append(element)
            list_color.append(getColor(screenshot, element[0], element[1]))
            list_component.append(component)
        # dataframe creation
    pixel_c = pd.DataFrame(data=result)
    if list_color:
        pixel_c.columns = ['Axis-X', 'Axis-Y']
        pixel_c["R-G-B"] = list_color
        pixel_c["Components"] = component
    return pixel_c


def bocp_bocc(screenshotPath, snapshotPath):
    bocp = {}
    bocc = {}
    pixel_interface = {}
    screenshot = Image.open(screenshotPath)
    screenshot = ImageUtilities.quantizeImage(screenshot)
    tree = ET.parse(snapshotPath)
    root = tree.getroot()
    components = getComponents(root)
    for c in reversed(components):
        c_item = c.items()
        pixel_c = pd.DataFrame()
        if len(c_item) == 17 and c_item[3][1].find("ImageView") == -1 and c_item[3][1].find("ImageButton") == -1:
            pixel_c = getPixels(screenshot, c_item, pixel_interface, 0)
        if len(c_item) == 18 and c_item[4][1].find("ImageView") == -1 and c_item[4][1].find("ImageButton") == -1:
            pixel_c = getPixels(screenshot, c_item, pixel_interface, 1)
        if not pixel_c.empty:
            list_color = list(pixel_c["R-G-B"])
            list_x = list(pixel_c["Axis-X"])
            list_y = list(pixel_c["Axis-Y"])
            i = 0
            for pixel_color in list_color:
                pixel_x_y = (0, list_x[i], list_y[i])
                c_n = (0, c)
                bocp.setdefault(pixel_color, []).append(pixel_x_y)
                bocc.setdefault(pixel_color, []).append(c_n)
                i += 1
    return bocp, bocc
