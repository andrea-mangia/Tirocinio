import ColorFitness
import ContrastFitness5
import Initializer
import NewContrastFitness
import SimilarityFitness


class Tritanopia:
    def __init__(self, bocc, bocp, img, root):
        self.bocc = bocc
        self.bocp = bocp
        self.originalColors = list(bocp.keys())
        self.img = img
        self.root = root
        self.nodesMap = Initializer.extractNodes(self.root)
        self.parents_map = {c: p for p in self.root.iter() for c in p}
        self.colorsMap = self.extractColorsMap()

    def evaluate(self, individual):
        return NewContrastFitness.getNewContrast(individual, self.colorsMap,
                                                 self.bocc), SimilarityFitness.getSimilarity(
            self.originalColors, individual), ColorFitness.getColorFitness(individual, self.bocc)

    def second(self, individual):
        return ContrastFitness5.getTotalContrast(individual, self.bocc, self.nodesMap, self.parents_map),

    def fourth(self, individual):
        return ColorFitness.getColorFitness(individual, self.bocc),

    def sixth(self, individual):
        return ColorFitness.getColorFitness(individual, self.bocc), SimilarityFitness.getSimilarity(self.originalColors,
                                                                                                    individual)

    def seventh(self, individual):
        return NewContrastFitness.getNewContrast(individual, self.colorsMap, self.bocc),

    def extractColorsMap(self):
        colorsMap = {}
        colors = list(self.bocc.keys())
        for child, parent in self.parents_map.items():
            childColor = ContrastFitness5.getIndex(self.bocc, child, 0, self.nodesMap)
            parentColor = ContrastFitness5.getIndex(self.bocc, parent, 0, self.nodesMap)
            if childColor is not None and parentColor is not None:
                colorsMap[colors[childColor]] = colors[parentColor]
        return colorsMap
