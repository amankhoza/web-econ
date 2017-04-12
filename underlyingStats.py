from __future__ import division  # for float division instead of int division
import pandas as pd
import time
from helperFunctions import evaluateBiddingStrategy as evaluate
from helperFunctions import clearTerminal as clearTerminal
from helperFunctions import printElapsedTime as printElapsedTime


'''
Evaluate the validation set as is, so take the current bid prices in the CSV and see the stats
'''

clearTerminal()

start = time.time()
print('Start')

validation_set = pd.read_csv('validation.csv')

bidids = validation_set['bidid'].values.tolist()
bidprices = validation_set['bidprice'].values.tolist()

bids = dict(zip(bidids, bidprices))

evaluate(bids, 'validation.csv', 6250)

end = time.time()
printElapsedTime(start, end)

print('Finish')
