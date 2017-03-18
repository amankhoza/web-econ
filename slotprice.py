import pandas as pd
import time
import os
import sys

start = time.clock()

os.system('reset')

def progress(count, total, status='Complete'):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def training(csv):
	advertisers = list(set(csv['advertiser']))

	data = {}

	for advertiser in advertisers:
		data[advertiser] = {}
		advertiserRows = csv[(csv['advertiser'] == advertiser)]

		for slotprice in range(0, 400):

			rows = advertiserRows[(advertiserRows['slotprice'] == slotprice)]
			if len(rows) > 0:
				data[advertiser][slotprice] = round(float(sum(rows['bidprice'].values)) / float(len(rows)))
			else:
				data[advertiser][slotprice] = float(0)

	print 'Done Training'

	return data

def validate(trainResults, csv):
	advertisers = list(set(csv['advertiser']))

	data = {}

	for advertiser in advertisers:
		data[advertiser] = {}

		advertiserRows = csv[(csv['advertiser'] == advertiser)]

		bought = int(0)

		for slotprice in range(0, 400):
			rows = advertiserRows[(advertiserRows['slotprice'] == slotprice)]

			# exact = rows[(rows['bidprice'] <= trainResults[advertiser][slotprice] + 1) & (rows['bidprice'] >= trainResults[advertiser][slotprice] - 1)]
			exact = rows[(rows['bidprice'] == trainResults[advertiser][slotprice] )]

			bought += len(exact)

		data[advertiser] = 100 * float(bought) / float(len(advertiserRows))
		print repr(advertiser) + ': ' + '%.2f' % data[advertiser] + '%'

	return data

def testFunc(trainResults, csv):
	advertisers = list(set(csv['advertiser']))
	sums = {}

	for advertiser in advertisers:
		sums[advertiser] = float(0)

	data = {}
	data['bidid'] = []
	data['bidprice'] = []

	n = len(csv)

	for i in range(0, n):
		progress(i, n)
		slotprice = csv.loc[i]['slotprice']
		advertiser = csv.loc[i]['advertiser']
		bidid = csv.loc[i]['bidid']

		bidprice = trainResults[advertiser][slotprice]

		sums[advertiser] += bidprice

		data['bidid'].append(bidid)
		data['bidprice'].append(trainResults[advertiser][slotprice])

	print 'Done Testing'
	print sums

	return data

def saveToFile(data):

	# Convert Dictionary to DataFrame then save as CSV

	output = pd.DataFrame.from_dict(data)
	output.to_csv("data/result.csv")

	return

train = pd.read_csv('data/train.csv')
validation = pd.read_csv('data/validation.csv')
#test = pd.read_csv('data/test.csv')

print 'Done Loading Files'

validate(training(train), validation)
#saveToFile(testFunc(training(train), test))

print 'Time Taken: ' + ("%.2f" % (time.clock() - start)) + 's'