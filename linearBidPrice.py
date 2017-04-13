from __future__ import division  # for float division instead of int division
import pandas as pd
import time
from helperFunctions import evaluateBiddingStrategy as evaluate
from helperFunctions import progress as progress
from helperFunctions import clearTerminal as clearTerminal
from helperFunctions import printElapsedTime as printElapsedTime
from helperFunctions import transformCategoricalFeatures
from logisticRegression import getPCTRS


def train(lowerBidLimit=200, upperBidLimit=400, bidIncrement=1):
    print('Training linear bidding strategy model:')

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


def predict(base_bidprices):
    bids = {}

    n = len(validationDF)

    print('Calculating pCTRs using logistic regression:')
    pctrs = getPCTRS(trainingDF, validationDF)

    print('Calculating avgCTR:')
    imps = len(validationDF)  # imps = number of impressions
    clicks = len(validationDF[validationDF['click']==1])
    avgCTR = clicks / imps  # ctr = click through rate

    print('Predicting bid prices using linear bidding strategy model:')
    for i in range(0, n):
        progress(i+1, n)
        bidid = validationDF.bidid.values[i]
        advertiser = validationDF.advertiser.values[i]
        baseBidPrice = int(base_bidprices[advertiser] * pctrs[i] / avgCTR)
        bids[bidid] = baseBidPrice

    return bids


clearTerminal()

start = time.time()
print('Start')

trainingDF = pd.read_csv('train.csv')
validationDF = pd.read_csv('validation.csv')

transformCategoricalFeatures(trainingDF)
transformCategoricalFeatures(validationDF)

base_bidprices = train()
bids = predict(base_bidprices)
evaluate(bids, 'validation.csv', 6250)

end = time.time()
printElapsedTime(start, end)

print('Finish')
