import csv, re, time, sys, logging, os, datetime
from pandas import *
log = logging.getLogger(__name__)

class Show():
	def __init__(self):
		pass

	def showStockData(self, line):
		line[1] = line[1].strftime('%m/%d/%Y')
		return line

	def displayResults(self, table):
		# print('StockType, DateOfPurchase, StocksAllotted, PurchasePrice, SellableStocks, SalePrice, Revenue, Profit')
		#
		# for line in table:
		# 	print('{}'.format(line))
		colList = ['StockType', 'DateOfPurchase', 'StocksAllotted', 'PurchasePrice', 'SellableStocks', 'SalePrice', 'TotalCost', 'Revenue', 'Profit']
		df = DataFrame(table, columns = colList)
		print('{}'.format(df))

	def displayOrigTable(self, table):
		colList = ['StockType', 'DateOfPurchase', 'StocksAllotted', 'PurchasePrice']
		df = DataFrame(table, columns = colList)
		print('{}'.format(df))
