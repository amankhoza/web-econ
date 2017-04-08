from __future__ import division

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from helperFunctions import clearTerminal
from sklearn import svm


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


clearTerminal()

# Load datasets
training_set = pd.read_csv("validation.csv")
validation_set = pd.read_csv("validation.csv")

x_train = getX(training_set)
x_valid = getX(validation_set)
y_train = training_set[LABEL].values.tolist()
y_valid = validation_set[LABEL].values.tolist()
# y_train = [1] * len(training_set)
# y_train[0] = 0
# y_valid = [1] * len(validation_set)
# y_valid[0] = 0

logregressor = LogisticRegression()
logregressor.fit(x_train, y_train)
y_pred = logregressor.predict(x_valid)

print('xdim', x_train.ndim)
progba = logregressor.predict_proba(x_train)
progba2 = map(lambda x: x[1], progba)
print('sams sum', sum(progba2))
print(x_train)
print(x_train.shape)
# print(progba)
# print('hello')
# print(progba2)
# print(len(y_pred), len(y_valid))
# print(type(y_pred), type(y_valid))
# print(sum(y_pred), sum(y_valid))
# print(y_pred)
# print(logregressor.score(x_train, y_train))
sum1 = 0
sum0 = 0
c1 = 0
c0 = 0
for i in range(0, len(y_pred)):
    if y_valid[i] == 1.0:
        # print(i, y_pred[i], y_valid[i], progba[i])
        sum1 += progba2[i]
        c1 += 1
    else:
        sum0 += progba2[i]
        c0 += 1

print(sum1, c1, sum1/c1)
print(sum0, c0, sum0/c0)
