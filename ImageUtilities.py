import re

from PIL import Image, ImageDraw
import Constants
import colorsys
import xml.etree.ElementTree as ET


def getRGBValues(img):
    img.convert('RGB')
    width, height = img.size
    colorDict = dict()
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x, y))
            if (r, g, b) in colorDict:
                colorDict[(r, g, b)].append((x, y))
            else:
                colorDict[(r, g, b)] = [(x, y)]
    return colorDict


def changeColors(img, newColors):
    draw = ImageDraw.Draw(img)
    width, height = img.size
    oldColors = getRGBValues(img)
    i = 0
    for k in oldColors.keys():
        for value in oldColors[k]:
            x, y = value
            draw.point((x, y), fill=newColors[i])
        i += 1
    img.save(Constants.PATH + "immagine_modificata.jpg")
    return img


def quantizeImage(img):
    img = img.quantize(colors=20, kmeans=10, method=1, dither=Image.NONE)
    quantizedImageName = "Shots/matematica.png"
    img.convert('RGB').save(quantizedImageName)
    return img.convert('RGB')


def genera_tavolozza_equidistante(n):
    tavolozza = []
    angolo = 360 / n
    for i in range(n):
        tonalita = angolo * i
        saturazione = 100  # Puoi regolare la saturazione e la luminosità a tuo piacimento
        luminosita = 50
        colore_hsl = (tonalita, saturazione, luminosita)

        # Converte HSL in RGB
        colore_rgb = tuple(
            int(x * 255) for x in colorsys.hls_to_rgb(tonalita / 360, luminosita / 100, saturazione / 100))
        tavolozza.append(colore_rgb)

    return tavolozza


def genera_tavolozza_monocromatica(tonalita_base, n):
    # Crea una lista vuota per i colori
    tavolozza = []

    # Saturazione di base e luminosita
    saturazione_base = 50
    luminosita_base = 50

    # Calcola l'incremento per la saturazione e la luminosita
    delta_saturazione = 100 / (n - 1)
    delta_luminosita = 100 / (n - 1)

    # Genera i colori con diverse saturazioni e luminosita
    for i in range(n):
        saturazione = saturazione_base + i * delta_saturazione
        luminosita = luminosita_base + i * delta_luminosita

        # Converte HSL in RGB
        colore_rgb = tuple(int(x * 255) for x in colorsys.hls_to_rgb(tonalita_base / 360, luminosita / 100, saturazione / 100))
        tavolozza.append(colore_rgb)

    return tavolozza


def getComponentsFromSnapshot(root):
    lista = []
    for comp in root.iter():
        lista.append(comp)
    return lista


def getPixels(c, tipo):
    # takes ranges based on type and split it
    values = re.findall(r'\d+', c[16][1])
    component = c[3][1]
    if tipo == 1:
        values = re.findall(r'\d+', c[17][1])
        component = c[4][1]
    asse_x_inizio = int(values[0])
    asse_y_inizio = int(values[1])
    asse_x_fine = int(values[2])
    asse_y_fine = int(values[3])
    coordinate = (asse_x_inizio, asse_y_inizio, asse_x_fine, asse_y_fine)
    return coordinate


def getView(snapPath):
    root = ET.parse(snapPath).getroot()
    C = getComponentsFromSnapshot(root)
    list_view = []
    # iterate all component in bottom up
    for c in C:
        c_item = c.items()
        if len(c_item) == 17 and c_item[3][1].find("ImageView") != -1 and c_item[3][1].find("ImageButton") != -1:
            list_view.append(getPixels(c_item, 0))
        elif len(c_item) == 18 and c_item[4][1].find("ImageView") != -1 and c_item[4][1].find("ImageButton") != -1:
            list_view.append(getPixels(c_item, 1))
    return list_view


# check index color
def IndexColor(img, i, j, old_color):
    for k, color in enumerate(old_color):
        data = img.getpixel((i, j))
        if data[0] == color[0] and data[1] == color[1] and data[2] == color[2]:
            return k
    return None


# check imageview inside list
def checkImageView(view_list, i, j):
    for n, view in enumerate(view_list):
        if i >= view[0] and i <= view[2] and j >= view[1] and j <= view[3] == True:
            return True
    return False


def buildImage(img_path, snap_path, old_color, new_color, h):
    img = Image.open(img_path)
    # draw = ImageDraw.Draw(img)
    width = img.size[0]
    height = img.size[1]
    view_list = getView(snap_path)
    for i in range(0, width):  # process all pixels
        for j in range(0, height):
            if len(view_list) > 0:
                c_images = checkImageView(view_list, i, j)
                if not c_images:
                    k = IndexColor(img, i, j, old_color)
                    if k is not None:
                        img.putpixel((i, j), (new_color[k][0], new_color[k][1], new_color[k][2]))
                        # draw.point((i, j), fill=(new_color[k]))
            else:
                k = IndexColor(img, i, j, old_color)
                if k is not None:
                    img.putpixel((i, j), (new_color[k][0], new_color[k][1], new_color[k][2]))
                    # draw.point((i, j), fill=(new_color[k]))
    return img
