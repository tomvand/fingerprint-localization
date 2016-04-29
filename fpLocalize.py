"""
fpLocalize

Perform localization using RSSI fingerprints
"""
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier

def _make_unique(mylist):
    return list(set(mylist))


class FingerprintGenerator:
    """
    Class to convert RSSI observations into fingerprints

    The main functions of this class are to build a list of beacons that should be used for fingerprints,
    and to convert device-labeled observations into fingerprint vectors.

    Instantiate the class, fit a list of observations (or provide a custom list of beacons), then use transform
    to transform lists of observations [{'address 1': RSSI, ...}, ...].
    """


    def __init__(self, method='fixed', undetected_value=-100, beacons=None):
        """
        Instantiate fingerprint generator
        :param method: beacon selection method: 'fixed', 'always_visible', 'all'
            fixed: use the beacons given in 'beacons'
            always_visible: use beacons that appear in every observation passed to fit()
            all: use all beacons that have been observed at least once in the observations passed to fit()
        :param undetected_value: value to assign to unobserved beacons
        :param beacons: list of beacons to use with 'fixed'
        """
        if method == 'fixed' and not beacons:
            raise Exception('Beacons have to be provided when using a fixed set of beacons!')
        self._set_method(method)
        self._beacons = beacons
        self._undetected_value = undetected_value


    def fit(self, rssi, method=None):
        """
        Get beacons to form RSSI fingerprints
        :param method:
        :param rssi: list of rssi observations per device:
            rssi = [
                {
                    '01:23:45:67:89:01': RSSI,
                    ...
                },
                ...
            ]
        """
        if method:
            self._set_method(method)

        if self._method == 'fixed':
            # Do nothing
            return
        elif self._method == 'always_visible':
            self._fit_always_visible(rssi)
        elif self._method == 'all':
            self._fit_all(rssi)
        else:
            raise Exception('Invalid _method!')


    def transform(self, rssi):
        """
        Transform list of RSSI observations into fingerprints
        :param rssi: list of rssi observations per device:
            rssi = [
                {
                    '01:23:45:67:89:01': RSSI,
                    ...
                },
                ...
            ]
        :return: list of fingerprints
        """
        tf = []
        for observation in rssi:
            tf.append([])
            for beacon in self._beacons:
                if beacon in observation:
                    tf[-1].append(observation[beacon])
                else:
                    tf[-1].append(self._undetected_value)
        return tf


    def _set_method(self, method):
        if method not in ['fixed', 'always_visible', 'all']:
            raise Exception('Unknown fit method: {}!'.format(method))
        self._method = method

    def _fit_always_visible(self, rssi):
        beacons = rssi[0].keys()
        for observation in rssi:
            for beacon in beacons:
                if beacon not in observation.keys():
                    beacons.remove(beacon)
        self._beacons = _make_unique(beacons)

    def _fit_all(self, rssi):
        beacons = []
        for observation in rssi:
            for beacon in observation.keys():
                beacons.append(beacon)
        self._beacons = _make_unique(beacons)




class RoomClassifier:
    """
    Class to convert fingerprints into a room label

    Train the classifier using a set of labeled fingerprints by calling fit().
    New fingerprints can be labeled using predict(). To recognize fingerprints
    outside of the calibrated rooms, call predict_outlier() to check whether
    the fingerprints are outliers.

    This class is a simple wrapper around sklearn's PCA and KNeighborsClassifier.
    """
    def __init__(self, outlier_threshold=10.0):
        """
        Instantiate room classifier
        :param outlier_threshold: Threshold in dB for outlier detection
        """
        self.dimred = PCA(n_components=5)
        self.classifier = KNeighborsClassifier(n_neighbors=5)
        self.outlier_threshold = outlier_threshold

    def fit(self, fingerprints, label):
        """
        Train room classifier using labeled fingerprints
        :param fingerprints: list of fingerprints
        :param label: list of labels corresponding to fingerprints
        """
        fp = self.dimred.fit_transform(fingerprints)
        self.classifier.fit(fp, label)

    def predict(self, fingerprints):
        """
        Predict room label for all fingerprints
        :param fingerprints: list of fingerprints
        :return: list of room labels
        """
        fp = self.dimred.transform(fingerprints)
        return self.classifier.predict(fp)

    def predict_outlier(self, fingerprints):
        """
        Predict whether the fingerprints are taken in an unlabeled room
        :param fingerprints: list of fingerprints
        :return: list of booleans, True if the room is unlabeled, False otherwise
        """
        fp = self.dimred.transform(fingerprints)
        dist, ind = self.classifier.kneighbors(fp, n_neighbors=1, return_distance=True)
        return (dist > self.outlier_threshold).reshape(-1)




#-------------------------------------------------------------------
# Example code

def _fingerprint_example():
    # Example observations
    obs = [
        {
            'A': -10,
            'B': -20,
            'C': -30
        },
        {
            'B': -20,
            'C': -30,
            'D': -40
        }
    ]
    # Fixed beacons example
    fixed = ['A', 'B', 'C']
    unobserved = -99

    print 'FingerprintGenerator (fixed)'
    fp = FingerprintGenerator(method='fixed', undetected_value=unobserved, beacons=fixed)
    print fp.transform(obs) # [[-10, -20, -30], [-99, -20, -30]]

    print 'FingerprintGenerator (always_visible)'
    fp = FingerprintGenerator(method='always_visible')
    fp.fit(obs)
    print fp.transform(obs) # [[-30, -20], [-30, -20]]

    print 'FingerprintGenerator (all)'
    fp = FingerprintGenerator(method='all')
    fp.fit(obs)
    print fp.transform(obs) # [[-10, -30, -20, -100], [-100, -30, -20, -40]]


def _room_example():
    fingerprints = [
        [-10, -20, -30, -40, -50],
        [-50, -60, -70, -80, -90]
    ]
    label = [
        1,
        2
    ]

    print 'Instantiate room classifier'
    clf = RoomClassifier()
    clf.classifier.n_neighbors = 1 # Reduce neighbors for demonstration
    print 'Train...'
    clf.fit(fingerprints, label)
    print 'Predict rooms 1 and 2...'
    print clf.predict(fingerprints) # [1 2]
    print 'Predict inliers'
    print clf.predict_outlier(fingerprints) # [False False]
    print 'Predict outlier'
    print clf.predict_outlier([[0,0,0,0,0]]) # [True]


if __name__ == '__main__':
    _fingerprint_example()
    _room_example()