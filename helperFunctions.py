from __future__ import division  # for float division instead of int division
import pandas as pd
import sys
import os


def clearTerminal():
    os.system('reset')


def printElapsedTime(start, end):
    print('\nTime elapsed: {} minutes {} seconds'.format(int((end-start)/60), int((end-start) % 60)))


def progress(count, total, status='Complete'):
    bar_len = 60
    filled_len = int(round(bar_len * count / total))
    percents = round(100.0 * count / total, 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    if count==total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def evaluateBiddingStrategy(bids, df, budget, silent):
    '''
    bids = dictionary (key=bidid, value=bidprice)
    data_set = path to csv
    budget = spending is capped at this value
    '''
    if silent == 1:
        print('Evaluating bidding strategy:')
    spent, impressions, clicks = 0, 0, 0

    n = len(df)

    payPriceErrors = 0

    for i in range(0, n):
        if silent == 1:
            progress(i+1, n)
        bidid = df.bidid.values[i]
        actualBidPrice = df.bidprice.values[i] / 1000
        payPrice = df.payprice.values[i] / 1000
        clicked = df.click.values[i]
        biddedPrice = bids[bidid] / 1000
        if payPrice > actualBidPrice:
            payPriceErrors += 1
        if spent+biddedPrice <= budget and payPrice < actualBidPrice:  # ensure pay price is less than bid price to remove garbage results
            if biddedPrice >= actualBidPrice:
                spent += payPrice
                impressions += 1
                if clicked == 1:
                    clicks += 1

    if silent == 1:
        print(str(payPriceErrors)+' rows ignored because payprice > bidprice')

    if impressions > 0:
        ctr = clicks / impressions
    else:
        ctr = 0

    if clicks > 0:
        cpc = spent / clicks
    else:
        cpc = 0

    if silent == 1:
        print('{:<12}\t{:<12}\t{:<12}\t{:<12}\t{:<12}'.format('spent', 'impressions', 'clicks', 'ctr', 'cpc'))
        print('{:<12}\t{:<12}\t{:<12}\t{:.10f}\t{:.10f}'.format(spent, impressions, clicks, ctr, cpc))
    return spent, impressions, clicks, ctr, cpc
