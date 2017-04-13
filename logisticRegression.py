from __future__ import division

from sklearn.linear_model import LogisticRegression
from helperFunctions import getX
from helperFunctions import avgCtr
from helperFunctions import scalePctrs
from helperFunctions import scaleBids
from helperFunctions import clampScaleFactors

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


def boostBidprices(training_set, validation_set, bidprices):
    pctrs = getPCTRS(training_set, validation_set)
    avgctr = avgCtr(validation_set)
    scale_factors = scalePctrs(pctrs, avgctr)
    scale_factors = clampScaleFactors(scale_factors)
    scaled_bids = scaleBids(bidprices, scale_factors)
    return scaled_bids
