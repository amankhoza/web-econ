import pandas as pd
import time
import random
from helperFunctions import evaluateBiddingStrategy as evaluate
from helperFunctions import progress as progress
from helperFunctions import clearTerminal as clearTerminal
from helperFunctions import printElapsedTime as printElapsedTime


def train(training_set):
    print('Training random bidding strategy model:')
    trainingDF = pd.read_csv(training_set)

    advertisers = list(set(trainingDF['advertiser']))

    n = len(advertisers)
    i = 0

    advertiserBidRange = {}

    for advertiser in advertisers:
        i += 1
        progress(i, n, '('+str(i)+'/'+str(len(advertisers))+')')
        rows = trainingDF[(trainingDF.advertiser==advertiser)]
        bids = rows.bidprice.values
        minBidPrice = min(bids)
        maxBidPrice = max(bids)
        advertiserBidRange[advertiser] = (minBidPrice, maxBidPrice)

    for advertiser in advertiserBidRange:
        print(advertiser, advertiserBidRange[advertiser])

    return advertiserBidRange


def predict(advertiser_bidrange, validation_set):
    print('Predicting bid prices using random bidding strategy model:')
    bids = {}
    validationDF = pd.read_csv(validation_set)

    n = len(validationDF)

    for i in range(0, n):
        progress(i+1, n)
        bidid = validationDF.bidid.values[i]
        advertiser = validationDF.advertiser.values[i]
        minBidPrice = advertiser_bidrange[advertiser][0]
        maxBidPrice = advertiser_bidrange[advertiser][1]
        diff = maxBidPrice - minBidPrice
        constBidPrice = random.randint(minBidPrice, maxBidPrice+diff)
        bids[bidid] = constBidPrice

    return bids


clearTerminal()

start = time.time()
print('Start')

advertiser_bidrange = train('train.csv')
bids = predict(advertiser_bidrange, 'validation.csv')
evaluate(bids, 'validation.csv', 25000)

end = time.time()
printElapsedTime(start, end)

print('Finish')
