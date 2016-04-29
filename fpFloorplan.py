from sklearn.manifold import Isomap
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
import matplotlib.pyplot as plt
import numpy as np

class FloorplanEstimator:
    """
    Simple estimator for rough floorplans
    """
    def __init__(self):
        """
        Instantiate floorplan estimator
        """
        self.dimred = Isomap(n_neighbors=25, n_components=2)
        self._fingerprints = None
        self._label = None

    def fit(self, fingerprints, label):
        """
        Estimate floorplan from labeled fingerprints
        :param fingerprints: list of fingerprints
        :param label: list of corresponding labels
        """
        self.dimred.fit(fingerprints)
        self._fingerprints = fingerprints
        self._label = label

    def transform(self, fingerprints):
        """
        Get x,y coordinates of fingerprints on floorplan
        :param fingerprints: list of fingerprints
        :return: list of [x,y] coordinates
        """
        return self.dimred.transform(fingerprints)

    def draw(self):
        """
        Draw the estimated floorplan in the current figure
        """
        xy = self.dimred.transform(self._fingerprints)

        x_min, x_max = xy[:,0].min(), xy[:,0].max()
        y_min, y_max = xy[:,1].min(), xy[:,1].max()
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 1.0),
                             np.arange(y_min, y_max, 1.0))
        clf = RadiusNeighborsClassifier(radius=3.0, outlier_label=0)
        clf.fit(xy, self._label)
        label = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

        plt.pcolormesh(xx, yy, label)
        plt.scatter(xy[:,0], xy[:,1], c=self._label, vmin=0)