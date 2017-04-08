import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from helperFunctions import clearTerminal


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
training_set = pd.read_csv("train.csv")
validation_set = pd.read_csv("validation.csv")

x_train = getX(training_set)
x_valid = getX(validation_set)
y_train = training_set[LABEL].values.tolist()
y_valid = validation_set[LABEL].values.tolist()

logregressor = LogisticRegression()
logregressor.fit(x_train, y_train)
y_pred = logregressor.predict(x_valid)

print('xdim', x_train.ndim)
print(len(y_pred), len(y_valid))
print(type(y_pred), type(y_valid))
print(sum(y_pred), sum(y_valid))
print(y_pred)
