from __future__ import division

import pandas as pd
import numpy as np
import time
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from helperFunctions import clearTerminal
from helperFunctions import printElapsedTime
from helperFunctions import evaluateBiddingStrategy as evaluate
from helperFunctions import transformCategoricalFeatures
from helperFunctions import avgCtr
from helperFunctions import scalePctrs
from helperFunctions import scaleBids
from helperFunctions import clampScaleFactors

'''
Features chosen via LinearSVC see featureSelection.py
'''
CONTINOUS_FEATURES = ['slotprice', 'slotheight', 'slotwidth']
CATEGORICAL_FEATURES = ['advertiser', 'weekday', 'region', 'useragent', 'adexchange', 'slotvisibility']


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

    for feature in CONTINOUS_FEATURES:
        values = map(lambda x: [x], data_set[feature].values.tolist())
        if len(x) > 0:
            x = np.concatenate((x, values), axis=1)
        else:
            x = values

    return x

def bayesianPrediction(x_train, y_train, x_pred):
    nb = GaussianNB()
    nb.fit(x_train, y_train)
    y_pred = nb.predict(x_pred)
    return y_pred

def linearRegressionPrediction(x_train, y_train, x_pred):
    linreg = LinearRegression()
    linreg.fit(x_train, y_train)
    y_pred = linreg.predict(x_pred)
    return y_pred


def logisticRegressionPctrs(x_train, y_train, x_pred):
    logregressor = LogisticRegression()
    logregressor.fit(x_train, y_train)
    probabilities = logregressor.predict_proba(x_valid)
    logistic_pctrs = map(lambda x: x[1], probabilities)
    return logistic_pctrs


clearTerminal()

start = time.time()
print('Start')

training_set = pd.read_csv('train.csv')
validation_set = pd.read_csv('validation.csv')

print('Loaded data')

transformCategoricalFeatures(training_set)
transformCategoricalFeatures(validation_set)

print('Transformed categorical features')

bidid_valid = validation_set['bidid'].values.tolist()

x_train = getX(training_set)
x_valid = getX(validation_set)
bidprice_train = training_set['bidprice'].values.tolist()
bidprice_valid = validation_set['bidprice'].values.tolist()
click_valid = validation_set['click'].values.tolist()
click_train = training_set['click'].values.tolist()

print('Split into train,valid sets (one hot encoding complete)')

nb_pred = bayesianPrediction(x_train, bidprice_train, x_valid)
nb_pctrs = bayesianPrediction(x_train, click_train, x_valid)

print('Made bayesian prediction')

bidprice_pred = linearRegressionPrediction(x_train, bidprice_train, x_valid)

linear_pctrs = linearRegressionPrediction(x_train, click_train, x_valid)

print('Made linear predictions')

logistic_pctrs = logisticRegressionPctrs(x_train, click_train, x_valid)

print('Made logistic predictions')

avgctr = avgCtr(validation_set)

nb_scale_factors = scalePctrs(nb_pctrs, avgctr)

linear_scale_factors = scalePctrs(linear_pctrs, avgctr)
logistic_scale_factors = scalePctrs(logistic_pctrs, avgctr)

linear_scale_factors = clampScaleFactors(linear_scale_factors)
logistic_scale_factors = clampScaleFactors(logistic_scale_factors)

clicked_linear_scale_factors = []
clicked_logistic_scale_factors = []

print('comparison of linear/logistic scale factors')
for i in range(0, len(click_valid)):
    if click_valid[i] == 1:
        print(i, linear_scale_factors[i], logistic_scale_factors[i])
        clicked_linear_scale_factors.append(linear_scale_factors[i])
        clicked_logistic_scale_factors.append(logistic_scale_factors[i])

linear_scaled_bidprices = scaleBids(bidprice_pred, linear_scale_factors)
logistic_scaled_bidprices = scaleBids(bidprice_pred, logistic_scale_factors)

nb_scaled_bidprices = scaleBids(nb_pred, logistic_scale_factors)
nb_unscaled_bids = dict(zip(bidid_valid, nb_pred))
nb_scaled_bids = dict(zip(bidid_valid, nb_scaled_bidprices))

unscaled_bids = dict(zip(bidid_valid, bidprice_pred))
linear_scaled_bids = dict(zip(bidid_valid, linear_scaled_bidprices))
logistic_scaled_bids = dict(zip(bidid_valid, logistic_scaled_bidprices))

evaluate(nb_unscaled_bids, 'validation.csv', 6250)
evaluate(nb_scaled_bids, 'validation.csv', 6250)

evaluate(unscaled_bids, 'validation.csv', 6250)
evaluate(logistic_scaled_bids, 'validation.csv', 6250)
evaluate(linear_scaled_bids, 'validation.csv', 6250)

end = time.time()
printElapsedTime(start, end)

print('Finish')
