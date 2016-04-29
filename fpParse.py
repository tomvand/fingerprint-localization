"""
fpParse.py

Read previously recorded fingerprints.
"""

import pickle

def parsePickledFingerprints(filename):
    """
    parsePickledFingerprints
    :param filename: Filename (.p)
    :return: data, label. Data is a 2-dimensional array of fingerprints, label is a 1-dimensional array of room labels.
    """
    aggregator = pickle.load(open("data.p","rb"))
    return aggregator.get_som_data()