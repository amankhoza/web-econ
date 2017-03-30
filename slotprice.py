import pandas as pd
import time
from helperFunctions import evaluateBiddingStrategy as evaluate
from helperFunctions import progress as progress
from helperFunctions import clearTerminal as clear

start = time.clock()

clear()

print 'Slotprice Method'

def training(csv):
	print 'Training:'
	advertisers = list(set(csv['advertiser']))

	data = {}

	for advertiser in advertisers:
		print advertiser

		data[advertiser] = {}
		advertiserRows = csv[(csv['advertiser'] == advertiser)]

		for slotprice in range(0, 400):
			progress (slotprice + 1, 400)

			rows = advertiserRows[(advertiserRows['slotprice'] == slotprice)]
			if len(rows) > 0:
				data[advertiser][slotprice] = round(float(sum(rows['bidprice'].values)) / float(len(rows)))
			else:
				data[advertiser][slotprice] = float(0)

	return data

def testFunc(trainResults, csv):
	print 'Testing:'

	sums = {}

	bidprices = {}
	data = {}
	data['bidid'] = []
	data['bidprice'] = []

	n = len(csv)

	for i in range(0, n):
		progress(i + 1, n)

		slotprice = csv.slotprice.values[i]
		advertiser = csv.advertiser.values[i]
		bidid = csv.bidid.values[i]

		bidprice = trainResults[advertiser][slotprice]

		data['bidid'].append(bidid)
		data['bidprice'].append(bidprice)

		bidprices[bidid] = bidprice

	return data, bidprices

def saveToFile(data, file):

	output = pd.DataFrame.from_dict(data)
	output.to_csv(file)

	return

print 'Loading:'

test = pd.read_csv('data/datasets/test.csv')
train = pd.read_csv('data/datasets/train.csv')
validation = pd.read_csv('data/datasets/validation.csv')

trainResults = training(train)

#testResults = testFunc(trainResults, test)[0]
bidprices = testFunc(trainResults, validation)[1]

#saveToFile(testResults, 'data/submissions/test.csv')
evaluate(bidprices, 'data/datasets/validation.csv', 25000)

print 'Time Taken: ' + ("%.2f" % (time.clock() - start)) + 's'