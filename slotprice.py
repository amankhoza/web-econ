import pandas as pd
import time
from helperFunctions import evaluateBiddingStrategy as evaluate
from helperFunctions import clearTerminal as clear
from helperFunctions import progress

def training(csv, silent):
	if silent == 1:
		print 'Training:'
	advertisers = list(set(csv['advertiser']))

	data = {}

	for advertiser in advertisers:
		#if silent == 1:
		print advertiser

		data[advertiser] = {}
		advertiserRows = csv[(csv['advertiser'] == advertiser)]

		for slotprice in range(0, 400):
			if silent == 1:
				progress (slotprice + 1, 400)

			rows = advertiserRows[(advertiserRows['slotprice'] == slotprice)]
			clicks = rows[(rows['click'] == 1)]
			
			if len(rows) > 0:
				difference = float(len(rows)) - float(len(clicks))

				avgbid = float(sum(rows['bidprice'].values)) / float(len(rows))
				bidprice = avgbid - difference * float(0.01001)
				# bidprice = avgbid - difference * float(0.01001) + float(len(clicks))

				if bidprice <= float(0):
					# if difference < float(100000):
					# 	bidprice = avgbid - difference * float(0.0000425)
					# 	# bidprice = avgbid - difference * float(0.000043)
					# else:
					# 	bidprice = avgbid - difference * float(0.00000425)
					# 	# bidprice = avgbid - difference * float(0.0000043)

					# data[advertiser][slotprice] = round(bidprice)
					data[advertiser][slotprice] = 0
				else:
					won = rows[(rows['bidprice'] <= round(bidprice))]
					wonClicks = won[(won['click'] == 1)]
					if len(won) > 0:
						ctr = float(len(wonClicks)) / float(len(won))
					else:
						ctr = 0

					newbidprice = round(bidprice) + 1

					new = rows[(rows['bidprice'] <= newbidprice)]
					newClicks = new[(new['click'] == 1)]
					if len(new) > 0:
						ctrMore = float(len(newClicks)) / float(len(new))
					else:
						ctrMore = 0

					# if len(new) > len(won):
					# 	bidprice = bidprice + 1
					if ctr < ctrMore:
						bidprice = bidprice + 1

					data[advertiser][slotprice] = round(bidprice)
			else:
				data[advertiser][slotprice] = 0

	return data

def testFunc(trainResults, csv, silent):
	if silent == 1:
		print 'Testing:'

	sums = {}

	bidprices = {}
	data = {}
	data['bidid'] = []
	data['bidprice'] = []

	n = len(csv)

	for i in range(0, n):
		if silent == 1:
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

def method(train, validation, silent):

	trainResults = training(train, silent)

	#testResults = testFunc(trainResults, test)[0]
	bidprices = testFunc(trainResults, validation, silent)[1]

	#saveToFile(testResults, 'data/submissions/test.csv')
	return evaluate(bidprices, 'data/datasets/validation.csv', 6250)

def run():
	start = time.clock()

	clear()

	print 'Slotprice Method'
	print 'Loading Datasets...'

	# test = pd.read_csv('data/datasets/test.csv')
	train = pd.read_csv('data/datasets/train.csv')
	validation = pd.read_csv('data/datasets/validation.csv')

	method (train, validation, 	1)

	print 'Time Taken: ' + ("%.2f" % (time.clock() - start)) + 's'

run()