import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

from fpParse import loadPickledFingerprints
from fpLocalize import RoomClassifier

if __name__ == '__main__':
    print 'Load dataset...'
    data, label = loadPickledFingerprints('./data/data_1st_2nd_3rd.p')
    print 'Split in train and test sets'
    X_train, X_test, y_train, y_test = train_test_split(data, label, train_size=0.90, stratify=label)
    print 'Train classifier'
    clf = RoomClassifier()
    clf.fit(X_train, y_train)
    print 'Predict rooms of test fingerprints'
    y_pred = clf.predict(X_test)
    print 'Accuracy: {}'.format(accuracy_score(y_test, y_pred))
    print 'Confusion matrix:\n{}'.format(confusion_matrix(y_test,y_pred))
