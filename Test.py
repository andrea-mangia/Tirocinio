import colorsys
import pickle
import random
import time
import xml.etree.ElementTree as ET

import PIL.Image
from PIL import Image

import Algorithm
import ColorFitness
import ContrastFitness5
import ImageUtilities
import Initializer
import SimilarityFitness
import Tritanopia
import Utilities


def start():
    Utilities.saveBocc("Shots/campus.png", "Shots/campus.uix", "BOCPCAMPUS", "BOCCCAMPUS")


def test():
    counter = 0
    path = "Results/resultCounter"
    with open(path, 'wb') as file:
        pickle.dump(counter, file)
