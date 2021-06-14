import csv, re, time, sys, logging, os, datetime
from yahoo_fin import stock_info
from CSVReader import CSVReader
from Calc import Calc
from Show import Show

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
		self.calc = Calc()
		self.show_data = Show()
		self.stockData = []
		self.currentStockPrice = 0.0
		self.currentDate = None
		self.ticker = 'QCOM'

	def Run(self, inFile):
		self.getCurrentDate()
		self.getCurrentStockprice(self.ticker)
		self.getStockData(inFile)
		self.getInput()

	def getCurrentStockprice(self, ticker):
		self.currentStockPrice = stock_info.get_live_price(ticker)
		self.currentStockPrice = round(self.currentStockPrice, 2)
		if(self.currentStockPrice == 0.0):
			log.error('Failed to get current stock price')
			exit()
		print('QCOM current stock price: {}'.format(self.currentStockPrice))

	def getCurrentDate(self):
		self.currentDate = datetime.datetime.today()
		print('Today: {}'.format(self.currentDate))

	def getStockData(self, inFile):
		if not self.csv_reader.isCSVOkay(inFile):
			exit()
		self.stockData = self.csv_reader.importDataFromCSV()
		self.show_data.displayOrigTable(self.stockData)

	def getInput(self):
		print()
		print('1. ESPP Summary')
		print('2. RSU Summary')
		print('3. Summary of sale for today')
		print('4. Summary of sale on certain date')
		print('5. Sell One Stock Group')
		print('q: Quit')
		print()
		a = input('Enter choice: ')
		if(a == 'q'): exit()
		if(a == '1'): self.calc.summarizeESPP(self.stockData, self.currentDate, self.currentStockPrice)
		if(a == '2'): self.calc.summarizeRSU(self.stockData, self.currentDate, self.currentStockPrice)
		if(a == '3'): self.calc.todaySummary(self.stockData, self.currentDate, self.currentStockPrice)
		if(a == '4'):
			date = input('Enter date in format MM/DD/YYYY: ')
			self.calc.dateSummary(self.stockData, datetime.datetime.strptime(date, '%m/%d/%Y'), self.currentStockPrice)
		if(a == '5'):
			date = input('Enter no: ')
			self.calc.oneStock(self.stockData, self.currentDate, self.currentStockPrice, int(date))

if(__name__ == "__main__"):
	tv = MyStocks()
	tv.Run(sys.argv[-1])
