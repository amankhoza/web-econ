from __future__ import division  # for float division instead of int division
import pandas as pd
import numpy as np
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


def evaluateBiddingStrategy(bids, data_set, budget):
    '''
    bids = dictionary (key=bidid, value=bidprice)
    data_set = path to csv
    budget = spending is capped at this value
    '''
    print('Evaluating bidding strategy:')
    df = pd.read_csv(data_set)
    spent, impressions, clicks = 0, 0, 0

    n = len(df)

    payPriceErrors = 0

    for i in range(0, n):
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

    print(str(payPriceErrors)+' rows ignored because payprice > bidprice')

    if impressions > 0:
        ctr = clicks / impressions
    else:
        ctr = 0

    if clicks > 0:
        cpc = spent / clicks
    else:
        cpc = 0

    print('{:<12}\t{:<12}\t{:<12}\t{:<12}\t{:<12}'.format('spent', 'impressions', 'clicks', 'ctr', 'cpc'))
    print('{:<12}\t{:<12}\t{:<12}\t{:.10f}\t{:.10f}'.format(spent, impressions, clicks, ctr, cpc))
    return spent, impressions, clicks, ctr, cpc


def transformCategoricalFeatures(data_set):
    data_set['adexchange'] = data_set['adexchange'].map({'1': 1, '2': 2, '3': 3, '4': 4, 'null': 5})
    data_set['slotformat'] = data_set['slotformat'].map({'0': 0, '1': 1, '5': 2, 'Na': 3})
    data_set['slotvisibility'] = data_set['slotvisibility'].map({'0': 0, '1': 1, '2': 1, '255': 2, 'FifthView': 3, 'FirstView': 4, 'FourthView': 5, 'Na': 6, 'OtherView': 7, 'SecondView': 8, 'ThirdView': 9})
    data_set['useragent'] = data_set['useragent'].map({'android_chrome': 0, 'android_firefox': 0, 'android_ie': 0, 'android_maxthon': 0, 'android_opera': 0, 'android_other': 0, 'android_safari': 0, 'android_sogou': 0, 'ios_other': 1, 'ios_safari': 1, 'linux_chrome': 2, 'linux_firefox': 2, 'linux_ie': 2, 'linux_opera': 2, 'linux_other': 2, 'linux_safari': 2, 'mac_chrome': 3, 'mac_firefox': 3, 'mac_ie': 3, 'mac_maxthon': 3, 'mac_opera': 3, 'mac_other': 3, 'mac_safari': 3, 'mac_sogou': 3, 'other_chrome': 4, 'other_firefox': 4, 'other_ie': 4, 'other_opera': 4, 'other_other': 4, 'other_safari': 4, 'windows_chrome': 5, 'windows_firefox': 5, 'windows_ie': 5, 'windows_maxthon': 5, 'windows_opera': 5, 'windows_other': 5, 'windows_safari': 5, 'windows_sogou': 5, 'windows_theworld': 5})


def getX(data_set, features):
    x = []

    for feature in features:
        values = map(lambda x: [x], data_set[feature].values.tolist())
        if len(x) > 0:
            x = np.concatenate((x, values), axis=1)
        else:
            x = values

    return x


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
