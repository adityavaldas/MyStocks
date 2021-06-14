import csv, re, time, sys, logging, os, datetime
from Show import Show

log = logging.getLogger(__name__)

class Calc():
	def __init__(self):
		self.show = Show()

	def summarizeESPP(self, stockData, nowDate, nowPrice):
		self.stockData = stockData
		self.currentDate = nowDate
		self.currentStockPrice = nowPrice

		print('ESPP Summary')
		table = self.populateTable('ESPP')
		self.displayResults(table)

	def summarizeRSU(self, stockData, nowDate, nowPrice):
		self.stockData = stockData
		self.currentDate = nowDate
		self.currentStockPrice = nowPrice
		print('RSU Summary')
		table = self.populateTable('RSU')
		self.displayResults(table)

	def todaySummary(self, stockData, nowDate, nowPrice):
		self.stockData = stockData
		self.currentDate = nowDate
		self.currentStockPrice = nowPrice
		print('If sale today')
		table = self.populateTable('ESPP')
		rsuTable = self.populateTable('RSU')
		table.extend(rsuTable)
		self.displayResults(table)

	def dateSummary(self, stockData, nowDate, nowPrice):
		self.stockData = stockData
		self.currentDate = nowDate
		self.currentStockPrice = nowPrice
		print('If sale on date: {}'.format(nowDate.strftime('%m/%d/%Y')))
		table = self.populateTable('ESPP')
		rsuTable = self.populateTable('RSU')
		table.extend(rsuTable)
		self.displayResults(table)

	def oneStock(self, stockData, nowDate, nowPrice, no):
		self.stockData = stockData
		self.currentDate = nowDate
		self.currentStockPrice = nowPrice
		print('Stock {}'.format(no))
		table = []
		table.append(self.stockData[no])
		table = self.fillTable(table, table[0][0])
		self.displayResults(table)

	def populateTable(self, stockType):
		table = [x for x in self.stockData if x[0].lower() == stockType.lower()]
		return self.fillTable(table, stockType)

	def fillTable(self, table, stockType):
		for i in range(len(table)):
			sellableStocks = self.getSellableStocks(table[i], stockType)
			table[i].append(sellableStocks)
			diff = self.currentStockPrice - table[i][3]
			table[i].append(diff)
			totalCost = table[i][3]*table[i][4]
			table[i].append(totalCost)
			currentSaleRevenue = round(sellableStocks*self.currentStockPrice, 2)
			table[i].append(currentSaleRevenue)
			table[i].append(round(diff*table[i][4], 2))
		return table

	def getSellableStocks(self, row, stockType):
		if(stockType.lower() == 'espp'):
			return row[2]
		if(stockType.lower() == 'rsu'):
			boughtStocks = row[2]
			boughtDate = row[1]

			noOfDays = self.daysFromBought(boughtDate)
			if(noOfDays < 365):
				multiplier = 0
			elif(noOfDays >= 365 and noOfDays < 548):
				multiplier = 0.33
			elif(noOfDays >= 548 and noOfDays < 730):
				multiplier = 0.5
			elif(noOfDays >= 548 and noOfDays < 730):
				multiplier = 0.66
			elif(noOfDays >= 730 and noOfDays < 913):
				multiplier = 0.83
			elif(noOfDays >= 913):
				multiplier = 1

			sellableStocks = int(multiplier*row[2])
			return sellableStocks

	def daysFromBought(self, boughtDate):
		d2 = self.currentDate
		d1 = boughtDate
		# d1 = datetime.datetime.strptime(d1, '%m/%d/%Y')
		delta = d2 - d1
		return delta.days

	def displayResults(self, table):
		self.show.displayResults(table)
		cost = 0.0
		rev = 0.0
		profit = 0.0
		for line in table:
			cost += line[-3]
			profit += line[-1]
			rev += line[-2]
		cost = round(cost, 2)
		profit = round(profit, 2)
		inLoss = False
		if(profit < 0):
			inLoss = True
			profit = abs(profit)
		rev = round(rev, 2)
		print('Total Expense: ${}'.format(cost))
		print('Total Revenue: ${}'.format(rev))
		if inLoss:
			print('Total Loss   : ${}'.format(profit))
		else:
			print('Total Profit : ${}'.format(profit))
