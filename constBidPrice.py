import pandas as pd
import os
import time

os.system('reset')

start = time.time()

print('Start')

df = pd.read_csv('train.csv')

advertisers = list(set(df['advertiser']))

n = len(df)

for advertiser in advertisers:
    highest = (advertiser, 0, 0)
    for bid in range(200, 400):
        rows = df[(df['advertiser']==advertiser) & (df['bidprice']<=bid)]
        imps = len(rows)  # imps = number of impressions
        clicks = len(rows[rows['click']==1])
        if imps > 0:
            ctr = float(clicks) / float(imps)  # ctr = click through rate
        else:
            ctr = 0
        if ctr > highest[2]:
            highest = (advertiser, bid, ctr)
    print(highest)

end = time.time()
print('\nTime elapsed: {} minutes {} seconds'.format(int((end-start)/60), int((end-start) % 60)))

print('Finish')
