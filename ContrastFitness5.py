def getIndex(BOCC, elem, h, nodesMap):
    list_keys = list(BOCC.keys())
    for index, key in enumerate(list_keys):
        for comp in BOCC.get(key):
            if comp[0] == h and comp[1].items() == nodesMap.get(elem):
                return index
    return None


def getContrast(color_a, color_b):
    return abs(((299 * color_a[0] + 587 * color_a[1] + 114 * color_a[2]) / 1000) - (
            (299 * color_b[0] + 587 * color_b[1] + 114 * color_b[2]) / 1000))


def is_valid_element(elem):
    return (
            (len(elem.items()) == 17 and "ImageView" not in elem.items()[3][1] and "ImageButton" not in elem.items()[3][
                1])
            or (len(elem.items()) == 18 and "ImageView" not in elem.items()[4][1] and "ImageButton" not in
                elem.items()[4][1])
    )


def getTotalContrast(individual, bocc, nodesMap, parent_map):
    totalContrast = 0
    for child in parent_map.keys():
        if is_valid_element(child):
            childIndex = getIndex(bocc, child, 0, nodesMap)
            if childIndex is not None:
                firstColor = individual[childIndex]
                parent = parent_map.get(child)
                parentIndex = getIndex(bocc, parent, 0, nodesMap)
                if parentIndex is not None:
                    secondColor = individual[parentIndex]
                    contrast = getContrast(firstColor, secondColor)
                    totalContrast += contrast
    return totalContrast * 2
