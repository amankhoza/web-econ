from __future__ import division

import pandas as pd
import numpy as np
import time
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from helperFunctions import clearTerminal
from helperFunctions import printElapsedTime
from helperFunctions import evaluateBiddingStrategy as evaluate
from helperFunctions import transformCategoricalFeatures


'''
Features chosen via LinearSVC see featureSelection.py
'''
CLICK_CONTINOUS_FEATURES = ['slotheight', 'slotprice']
CLICK_CATEGORICAL_FEATURES = ['weekday', 'hour', 'region', 'city', 'adexchange', 'slotvisibility', 'useragent']
BIDPRICE_CONTINOUS_FEATURES = ['slotwidth', 'slotheight', 'slotprice', 'bidprice', 'payprice']
BIDPRICE_CATEGORICAL_FEATURES = ['weekday', 'hour', 'region', 'city', 'advertiser', 'adexchange', 'slotformat', 'slotvisibility', 'useragent']


def getHotEncodedX(data_set, categorical_features, continuous_features):
    x = []

    for feature in categorical_features:
        values = map(lambda x: [x], data_set[feature].values.tolist())
        enc = OneHotEncoder()
        enc.fit(values)
        transformed = enc.transform(values).toarray()
        if len(x) > 0:
            x = np.concatenate((x, transformed), axis=1)
        else:
            x = transformed

    for feature in continuous_features:
        values = map(lambda x: [x], data_set[feature].values.tolist())
        if len(x) > 0:
            x = np.concatenate((x, values), axis=1)
        else:
            x = values

    return x


def linearRegressionPrediction(x_train, y_train, x_pred):
    linreg = LinearRegression()
    linreg.fit(x_train, y_train)
    y_pred = linreg.predict(x_pred)
    return y_pred


def logisticRegressionPctrs(x_train, y_train, x_pred):
    logregressor = LogisticRegression()
    logregressor.fit(x_train, y_train)
    probabilities = logregressor.predict_proba(x_pred)
    logistic_pctrs = map(lambda x: x[1], probabilities)
    return logistic_pctrs


def avgCtr(data_set):
    clicks = len(data_set[data_set['click']==1])
    imps = len(data_set)
    avgctr = clicks/imps
    return avgctr


def scalePctrs(pctrs, avgctr):
    return map(lambda x: x/avgctr, pctrs)


def scaleBids(bids, scale_factors):
    return [bid*scale_factor for bid, scale_factor in zip(bids, scale_factors)]


def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)


def clampScaleFactors(scale_factors):
    return map(lambda x: clamp(x, 0, 1.05), scale_factors)


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

click_x_train = getHotEncodedX(training_set, CLICK_CONTINOUS_FEATURES, CLICK_CATEGORICAL_FEATURES)
click_x_valid = getHotEncodedX(validation_set, CLICK_CONTINOUS_FEATURES, CLICK_CATEGORICAL_FEATURES)
bidprice_x_train = getHotEncodedX(training_set, BIDPRICE_CONTINOUS_FEATURES, BIDPRICE_CATEGORICAL_FEATURES)
bidprice_x_valid = getHotEncodedX(validation_set, BIDPRICE_CONTINOUS_FEATURES, BIDPRICE_CATEGORICAL_FEATURES)
bidprice_train = training_set['bidprice'].values.tolist()
bidprice_valid = validation_set['bidprice'].values.tolist()
click_valid = validation_set['click'].values.tolist()
click_train = training_set['click'].values.tolist()

print('Split into train,valid sets (one hot encoding complete)')

bidprice_pred = linearRegressionPrediction(bidprice_x_train, bidprice_train, bidprice_x_valid)

linear_pctrs = linearRegressionPrediction(click_x_train, click_train, click_x_valid)

print('Made linear predictions')

logistic_pctrs = logisticRegressionPctrs(click_x_train, click_train, click_x_valid)

print('Made logistic predictions')

avgctr = avgCtr(validation_set)

linear_scale_factors = scalePctrs(linear_pctrs, avgctr)
logistic_scale_factors = scalePctrs(logistic_pctrs, avgctr)

linear_scale_factors = clampScaleFactors(linear_scale_factors)
logistic_scale_factors = clampScaleFactors(logistic_scale_factors)

# clicked_linear_scale_factors = []
# clicked_logistic_scale_factors = []

# print('comparison of linear/logistic scale factors')
# for i in range(0, len(click_valid)):
#     if click_valid[i] == 1:
#         print(i, linear_scale_factors[i], logistic_scale_factors[i])
#         clicked_linear_scale_factors.append(linear_scale_factors[i])
#         clicked_logistic_scale_factors.append(logistic_scale_factors[i])

linear_scaled_bidprices = scaleBids(bidprice_pred, linear_scale_factors)
logistic_scaled_bidprices = scaleBids(bidprice_pred, logistic_scale_factors)

unscaled_bids = dict(zip(bidid_valid, bidprice_pred))
linear_scaled_bids = dict(zip(bidid_valid, linear_scaled_bidprices))
logistic_scaled_bids = dict(zip(bidid_valid, logistic_scaled_bidprices))

print('Evaluating: ')

evaluate(unscaled_bids, 'validation.csv', 6250)
evaluate(logistic_scaled_bids, 'validation.csv', 6250)
evaluate(linear_scaled_bids, 'validation.csv', 6250)

end = time.time()
printElapsedTime(start, end)

print('Finish')
