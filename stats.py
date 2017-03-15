# -*- coding: utf-8 -*-

import pandas as pd
import os
import sys
import time


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


os.system('reset')

start = time.time()

print('Start')

df = pd.read_csv('train.csv')
# df = pd.read_csv('validation.csv')

advertisers = list(set(df['advertiser']))

n = len(df)

print('\nStats:')
print('Advertiser\tImps\t\tClicks\t\tCost\t\tCTR\t\tCPM\t\tCPC\t\teCPC')

for advertiser in advertisers:
    rows = df[df['advertiser']==advertiser]
    imps = len(rows)  # imps = number of impressions
    clicks = len(rows[rows['click']==1])
    totalCost = sum(rows['payprice'].values)
    clickedCost = sum(rows[rows['click']==1]['payprice'].values)
    ctr = 100 * float(clicks) / float(imps)  # ctr = click through rate
    cpm = float(totalCost) / float(imps) / float(1000)  # cpm = cost per mille = cost per 1000 impressions
    cpc = float(totalCost) / float(clicks)
    ecpc = float(clickedCost) / float(clicks)
    print('{} \t\t{} \t\t{} \t\t{}  \t{:.3f}% \t\t{:.3f} \t\t{:.2f} \t{:.2f}'.format(advertiser, imps, clicks, totalCost, ctr, cpm, cpc, ecpc))

print('\nAvg CTR by day:')
print('Advertiser\tMon\t\tTue\t\tWed\t\tThu\t\tFri\t\tSat\t\tSun')

for advertiser in advertisers:
    sys.stdout.write('{}\t\t'.format(advertiser))
    for day in range(0, 7):
        rows = df[(df['advertiser']==advertiser) & (df['weekday']==day)]
        imps = len(rows)  # imps = number of impressions
        clicks = len(rows[rows['click']==1])
        if imps>0:
            ctr = 100 * float(clicks) / float(imps)  # ctr = click through rate
            sys.stdout.write('{:.3f}%\t\t'.format(ctr))
        else:
            ctr = '-'
            sys.stdout.write('{}\t\t'.format(ctr))
    sys.stdout.write('\n')
    sys.stdout.flush()

# Morning is from sunrise to 11:59 AM. Sunrise typically occurs around 6 AM.
# Noon is at 12:00 PM.
# Afternoon is from 12:01 PM to around 5:00 PM.
# Evening is from 5:01 PM to 8 PM, or around sunset.
# Night is from sunset to sunrise, so from 8:01 PM until 5:59 AM.

print('\nAvg CTR by time:')
print('Advertiser\tMorning (6AM-11:59AM)\t\tAfternoon (12:01PM-5PM)\t\tEvening (5:01PM-8PM)\t\tNight (8:01PM-5:59AM)')

timeslots = []
timeslots.append(range(6, 12))
timeslots.append(range(12, 17))
timeslots.append(range(17, 20))
timeslots.append(range(20, 24) + range(0, 6))

for advertiser in advertisers:
    sys.stdout.write('{}\t\t'.format(advertiser))
    rows = df[(df['advertiser']==advertiser)]
    mRows = rows[(rows['hour']>=6) & (rows['hour']<12)]
    aRows = rows[(rows['hour']>=12) & (rows['hour']<17)]
    eRows = rows[(rows['hour']>=17) & (rows['hour']<20)]
    nRows = rows[((rows['hour']>=20) & (rows['hour']<24)) | ((rows['hour']>=0) & (rows['hour']<6))]
    allRows = [mRows, aRows, eRows, nRows]
    for i in range(0, 4):
        currRows = allRows[i]
        imps = len(currRows)  # imps = number of impressions
        clicks = len(currRows[currRows['click']==1])
        if imps>0:
            ctr = 100 * float(clicks) / float(imps)  # ctr = click through rate
            sys.stdout.write('{:.3f}%\t\t\t\t'.format(ctr))
        else:
            ctr = '-'
            sys.stdout.write('{}\t\t'.format(ctr))
    sys.stdout.write('\n')
    sys.stdout.flush()

print('\nAvg CTR by device:')
print('Advertiser\tWindows\t\tAndroid\t\tMac\t\tiOS\t\tOther')

devices = ['windows', 'android', 'mac', 'ios', 'other_']

for advertiser in advertisers:
    sys.stdout.write('{}\t\t'.format(advertiser))
    for i in range(0, len(devices)):
        rows = df[df['advertiser']==advertiser]
        currRows = rows[rows['useragent'].str.contains(devices[i])]
        imps = len(currRows)  # imps = number of impressions
        clicks = len(currRows[currRows['click']==1])
        if imps>0:
            ctr = 100 * float(clicks) / float(imps)  # ctr = click through rate
            sys.stdout.write('{:.3f}%\t\t'.format(ctr))
        else:
            ctr = '-'
            sys.stdout.write('{}\t\t'.format(ctr))
    sys.stdout.write('\n')
    sys.stdout.flush()

end = time.time()
print('\nTime elapsed: {} minutes {} seconds'.format(int((end-start)/60), int((end-start) % 60)))

print('Finish')
