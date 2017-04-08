from __future__ import division

import pandas as pd
import numpy as np
# import time
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
# from helperFunctions import clearTerminal
# from helperFunctions import printElapsedTime


ALL_FEATURES = ['weekday', 'hour', 'region', 'city', 'slotwidth', 'slotheight', 'slotprice']
CONTINOUS_FEATURES = ['slotwidth', 'slotheight', 'slotprice']
CATEGORICAL_FEATURES = ['weekday', 'hour', 'region', 'city']
LABEL = 'click'


def getX(data_set):
    x = []

    for feature in CATEGORICAL_FEATURES:
        values = map(lambda x: [x], data_set[feature].values.tolist())
        enc = OneHotEncoder()
        enc.fit(values)
        transformed = enc.transform(values).toarray()
        if len(x) > 0:
            x = np.concatenate((x, transformed), axis=1)
        else:
            x = transformed

    return x


def getPCTRS(training_set, validation_set):
    # Load datasets
    # training_set = pd.read_csv(train)
    # validation_set = pd.read_csv(valid)

    x_train = getX(training_set)
    x_valid = getX(validation_set)
    y_train = training_set[LABEL].values.tolist()
    # y_valid = validation_set[LABEL].values.tolist()

    logregressor = LogisticRegression()
    logregressor.fit(x_train, y_train)
    # y_pred = logregressor.predict(x_valid)

    probabilities = logregressor.predict_proba(x_valid)
    pctrs = map(lambda x: x[1], probabilities)
    return pctrs

# clearTerminal()

# start = time.time()
# print('Start')

# end = time.time()
# printElapsedTime(start, end)

# print('Finish')

# print(progba)
# print('hello')
# print(progba2)
# print(len(y_pred), len(y_valid))
# print(type(y_pred), type(y_valid))
# print(sum(y_pred), sum(y_valid))
# print(y_pred)
# print(logregressor.score(x_train, y_train))

# sum1 = 0
# sum0 = 0
# c1 = 0
# c0 = 0
# for i in range(0, len(y_pred)):
#     if y_valid[i] == 1.0:
#         # print(i, y_pred[i], y_valid[i], progba[i])
#         sum1 += progba2[i]
#         c1 += 1
#     else:
#         sum0 += progba2[i]
#         c0 += 1

# print(sum1, c1, sum1/c1)
# print(sum0, c0, sum0/c0)
