import csv, re, time, sys, logging, os, datetime
from yahoo_fin import stock_info
from CSVReader import CSVReader

log = logging.getLogger()
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)-5s: %(message)s','%d-%b-%y %H:%M:%S')
ch.setFormatter(formatter)
log.addHandler(ch)
os.system('cls')

class MyStocks():
	def __init__(self):
		self.csv_reader = CSVReader()
		self.stockData = []
		self.currentStockPrice = 0.0
		self.currentDate = None
		self.ticker = 'QCOM'

	def Run(self, inFile):
		self.getCurrentDate()
		self.getCurrentStockprice(self.ticker)
		self.getStockData(inFile)

	def getCurrentStockprice(self, ticker):
		self.currentStockPrice = stock_info.get_live_price(ticker)
		self.currentStockPrice = round(self.currentStockPrice, 2)
		if(self.currentStockPrice == 0.0):
			log.error('Failed to get current stock price')
			exit()
		log.info('QCOM current stock price: {}'.format(self.currentStockPrice))

	def getCurrentDate(self):
		self.currentDate = datetime.datetime.today()
		log.info('Today: {}'.format(self.currentDate))

	def getStockData(self, inFile):
		if not self.csv_reader.isCSVOkay(inFile):
			exit()
		self.stockData = self.csv_reader.importDataFromCSV()
		log.info('self.stockData: ')
		for line in self.stockData:
			log.info('{}'.format(line))


if(__name__ == "__main__"):
	tv = MyStocks()
	tv.Run(sys.argv[-1])
