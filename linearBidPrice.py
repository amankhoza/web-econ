from __future__ import division  # for float division instead of int division
import pandas as pd
import time
from helperFunctions import evaluateBiddingStrategy as evaluate
from helperFunctions import progress as progress
from helperFunctions import clearTerminal as clearTerminal
from helperFunctions import printElapsedTime as printElapsedTime


def train(training_set, lowerBidLimit=200, upperBidLimit=400, bidIncrement=1):
    print('Training linear bidding strategy model:')
    trainingDF = pd.read_csv(training_set)

    advertisers = list(set(trainingDF['advertiser']))

    n = len(advertisers) * len(range(lowerBidLimit, upperBidLimit, bidIncrement))
    i = 0
    j = 1

    optimalBaseBidPrices = []
    optimalBaseBids = {}

    for advertiser in advertisers:
        highest = (advertiser, 0, 0)  # tuple containing highest ctr and corresponding bid prices
        for bid in range(lowerBidLimit, upperBidLimit, bidIncrement):
            i += 1
            progress(i, n, '('+str(j)+'/'+str(len(advertisers))+')')
            rows = trainingDF[(trainingDF['advertiser']==advertiser) & (trainingDF['bidprice']<=bid)]
            imps = len(rows)  # imps = number of impressions
            clicks = len(rows[rows['click']==1])
            if imps > 0:
                ctr = clicks / imps  # ctr = click through rate
            else:
                ctr = 0
            if ctr > highest[1]:
                highest = (advertiser, ctr, bid)
        optimalBaseBidPrices.append(highest)
        optimalBaseBids[advertiser] = highest[2]
        j += 1

    for optimalBaseBidPrice in optimalBaseBidPrices:
        print(optimalBaseBidPrice)

    return optimalBaseBids


def predict(base_bidprices, validation_set):
    print('Predicting bid prices using linear bidding strategy model:')
    bids = {}
    validationDF = pd.read_csv(validation_set)

    n = len(validationDF)

    pCTR = 1  # NEED TO CALCULATE THIS SOMEHOW
    avgCTR = 1  # NEED TO CALCULATE THIS SOMEHOW

    for i in range(0, n):
        progress(i+1, n)
        bidid = validationDF.bidid.values[i]
        advertiser = validationDF.advertiser.values[i]
        baseBidPrice = int(base_bidprices[advertiser] * pCTR / avgCTR)
        bids[bidid] = baseBidPrice

    return bids


clearTerminal()

start = time.time()
print('Start')

base_bidprices = train('train.csv')
bids = predict(base_bidprices, 'validation.csv')
evaluate(bids, 'validation.csv', 25000)

end = time.time()
printElapsedTime(start, end)

print('Finish')
