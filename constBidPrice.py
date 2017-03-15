import pandas as pd
import sys
import os
import time


def progress(count, total, status='Complete'):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    if count==total:
        sys.stdout.write('\n')
    sys.stdout.flush()


os.system('reset')

start = time.time()

print('Start')

df = pd.read_csv('train.csv')

advertisers = list(set(df['advertiser']))

lowerBidLimit = 200
upperBidLimit = 400
bidIncrement = 1

n = len(advertisers) * len(range(lowerBidLimit, upperBidLimit, bidIncrement))
i = 0
j = 1

optimalConstantBidPrices = []

for advertiser in advertisers:
    highest = (advertiser, 0, 0)
    for bid in range(lowerBidLimit, upperBidLimit, bidIncrement):
        i += 1
        progress(i, n, '('+str(j)+'/'+str(len(advertisers))+')')
        rows = df[(df['advertiser']==advertiser) & (df['bidprice']<=bid)]
        imps = len(rows)  # imps = number of impressions
        clicks = len(rows[rows['click']==1])
        if imps > 0:
            ctr = float(clicks) / float(imps)  # ctr = click through rate
        else:
            ctr = 0
        if ctr > highest[2]:
            highest = (advertiser, bid, ctr)
    optimalConstantBidPrices.append(highest)
    j += 1

for optimalConstantBid in optimalConstantBidPrices:
    print(optimalConstantBid)

end = time.time()
print('\nTime elapsed: {} minutes {} seconds'.format(int((end-start)/60), int((end-start) % 60)))

print('Finish')
