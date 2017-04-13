from __future__ import division

import pandas as pd
import time
from helperFunctions import clearTerminal
from helperFunctions import printElapsedTime
from helperFunctions import transformCategoricalFeatures
from helperFunctions import getX
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel

FEATURES = ['slotwidth', 'slotheight', 'slotprice', 'weekday', 'hour', 'region', 'city', 'advertiser', 'adexchange', 'slotformat', 'slotvisibility', 'useragent']
LABELS = ['click', 'bidprice']


clearTerminal()

start = time.time()
print('Start')

validation_set = pd.read_csv('validation.csv')

transformCategoricalFeatures(validation_set)

X = getX(validation_set, FEATURES)

for label in LABELS:
    print(label)

    y = validation_set[label].values.tolist()

    print('original x shape: ', X.shape)
    print(FEATURES)
    print(X[0:3])

    lsvc = LinearSVC(C=0.01, penalty="l1", dual=False).fit(X, y)
    model = SelectFromModel(lsvc, prefit=True)
    X_new = model.transform(X)

    print('new x shape: ', X_new.shape)
    print(X_new[0:3])

end = time.time()
printElapsedTime(start, end)

print('Finish')
