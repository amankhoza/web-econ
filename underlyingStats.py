from __future__ import division  # for float division instead of int division
import pandas as pd
import time
from helperFunctions import evaluateBiddingStrategy as evaluate
from helperFunctions import transformCategoricalFeatures
from helperFunctions import clearTerminal
from helperFunctions import printElapsedTime
from logisticRegression import boostBidprices

'''
Evaluate the validation set as is, so take the current bid prices in the CSV and see the stats
'''

clearTerminal()

start = time.time()
print('Start')

training_set = pd.read_csv('train.csv')
validation_set = pd.read_csv('validation.csv')

transformCategoricalFeatures(training_set)
transformCategoricalFeatures(validation_set)

bidids = validation_set['bidid'].values.tolist()
bidprices = validation_set['bidprice'].values.tolist()

print('Evaluating data set as is: ')
bids = dict(zip(bidids, bidprices))
evaluate(bids, 'validation.csv', 25000)
evaluate(bids, 'validation.csv', 6250)

print('Evaluating data set with logistic regression boosted bids: ')
boostedbidprices = boostBidprices(training_set, validation_set, bidprices)
boosted_bids = dict(zip(bidids, boostedbidprices))
evaluate(boosted_bids, 'validation.csv', 25000)
evaluate(boosted_bids, 'validation.csv', 6250)

end = time.time()
printElapsedTime(start, end)

print('Finish')
