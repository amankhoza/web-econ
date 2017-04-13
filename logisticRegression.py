from __future__ import division

from sklearn.linear_model import LogisticRegression
from helperFunctions import getX

FEATURES = ['advertiser', 'weekday', 'hour', 'region', 'city', 'slotwidth', 'slotheight', 'slotvisibility', 'slotformat', 'slotprice', 'adexchange', 'useragent']
LABEL = 'click'


def getPCTRS(training_set, validation_set):
    x_train = getX(training_set, FEATURES)
    x_valid = getX(validation_set, FEATURES)
    y_train = training_set[LABEL].values.tolist()

    logregressor = LogisticRegression()
    logregressor.fit(x_train, y_train)

    probabilities = logregressor.predict_proba(x_valid)
    pctrs = map(lambda x: x[1], probabilities)
    return pctrs
