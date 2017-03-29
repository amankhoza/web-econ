import pandas as pd
import time
from helperFunctions import evaluateBiddingStrategy as evaluate
from helperFunctions import progress as progress
from helperFunctions import clearTerminal as clearTerminal

start = time.clock()

clearTerminal()

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

	predictedBidPrices = {}
	data = {}
	data['bidid'] = []
	data['bidprice'] = []

	n = len(csv)

	for i in range(0, n):
		progress(i+1, n)
		slotprice = csv.loc[i]['slotprice']
		advertiser = csv.loc[i]['advertiser']
		bidid = csv.loc[i]['bidid']

		bidprice = trainResults[advertiser][slotprice]

		sums[advertiser] += bidprice

		data['bidid'].append(bidid)
		data['bidprice'].append(trainResults[advertiser][slotprice])

		predictedBidPrices[bidid] = bidprice

	print 'Done Testing'
	print sums

	return data, predictedBidPrices

def saveToFile(data):

	# Convert Dictionary to DataFrame then save as CSV

	output = pd.DataFrame.from_dict(data)
	output.to_csv("data/result.csv")

	return

train = pd.read_csv('data/train.csv')
validation = pd.read_csv('data/validation.csv')
#test = pd.read_csv('data/test.csv')

print 'Done Loading Files'

#validate(training(train), validation)
#saveToFile(testFunc(training(train), test)[0])
predictedBidPrices = testFunc(training(train), validation)[1]
evaluate(predictedBidPrices, 'data/validation.csv', 25000)

print 'Time Taken: ' + ("%.2f" % (time.clock() - start)) + 's'