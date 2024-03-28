import pickle

import BOCP_BOCC_ALGORITHM


def saveBocc(screen, snap, nomeBocp, nomeBocc):
    bocp, bocc = BOCP_BOCC_ALGORITHM.bocp_bocc(screen, snap)
    with open(nomeBocc, 'wb') as file:
        pickle.dump(bocc, file)
    with open(nomeBocp, 'wb') as file:
        pickle.dump(bocp, file)


def openBocc(bocpPath, boccPath):
    with open(boccPath, 'rb') as file:
        bocc = pickle.load(file)
    with open(bocpPath, 'rb') as file:
        bocp = pickle.load(file)
    return bocp, bocc
