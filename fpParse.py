"""
fpParse.py

Read previously recorded fingerprints.
"""

import pickle

def savePickledFingerprints(filename, fingerprints, label=None):
    """
    Save pickled fingerprints
    :param filename: filename (.p)
    :param fingerprints: list of fingerprints
    :param label: list of labels (optional)
    :return:
    """
    with open(filename, 'wb') as outfile:
        pickle.dump({
            'fingerprints': fingerprints,
            'label': label
        }, outfile)

def loadPickledFingerprints(filename):
    """
    Load pickled fingerprints
    :param filename: filename (.p)
    :return: fingerprints, label
    """
    with open(filename, 'rb') as infile:
        data = pickle.load(infile)
    return data['fingerprints'], data['label']



def parseOldFingerprints(filename):
    """
    Parse old fingerprint files.
    :param filename: Filename (.p)
    :return: data, label. Data is a list of fingerprints, label is a list of room labels.
    """
    aggregator = pickle.load(open(filename,"rb"))
    return aggregator.get_som_data()