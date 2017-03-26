from __future__ import division  # for float division instead of int division
import pandas as pd
import time
from helperFunctions import evaluateBiddingStrategy as evaluate
from helperFunctions import progress as progress
from helperFunctions import clearTerminal as clearTerminal
from helperFunctions import printElapsedTime as printElapsedTime


def train(training_set, lowerBidLimit=200, upperBidLimit=400, bidIncrement=1):
    print('Training constant bidding strategy model:')
    trainingDF = pd.read_csv(training_set)

    advertisers = list(set(trainingDF['advertiser']))

    n = len(advertisers) * len(range(lowerBidLimit, upperBidLimit, bidIncrement))
    i = 0
    j = 1

    optimalConstBidPrices = []
    optimalConstBids = {}

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
        optimalConstBidPrices.append(highest)
        optimalConstBids[advertiser] = highest[2]
        j += 1

    for optimalConstBidPrice in optimalConstBidPrices:
        print(optimalConstBidPrice)

    return optimalConstBids


def predict(constant_bidprices, validation_set):
    print('Predicting bid prices using constant bidding strategy model:')
    bids = {}
    validationDF = pd.read_csv(validation_set)

    n = len(validationDF)

    for i in range(0, n):
        progress(i+1, n)
        bidid = validationDF.bidid.values[i]
        advertiser = validationDF.advertiser.values[i]
        constBidPrice = constant_bidprices[advertiser]
        bids[bidid] = constBidPrice

    return bids


clearTerminal()

start = time.time()
print('Start')

const_bidprices = train('train.csv')
bids = predict(const_bidprices, 'validation.csv')
evaluate(bids, 'validation.csv', 25000)

end = time.time()
printElapsedTime(start, end)

print('Finish')
