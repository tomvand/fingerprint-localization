import matplotlib.pyplot as plt

from fpParse import loadPickledFingerprints
from fpFloorplan import FloorplanEstimator

if __name__ == '__main__':
    print 'Load dataset...'
    data, label = loadPickledFingerprints('./data/data_gf_7x20.p')
    print 'Estimate floorplan'
    fl = FloorplanEstimator()
    fl.fit(data, label)
    fl.draw()
    plt.axis('equal')
    plt.show()