import csv, re, time, sys, logging, os, datetime

log = logging.getLogger(__name__)

class CSVReader():
	def __init__(self):
		self.stock_data = []

	def isCSVOkay(self, inFile):
		if not os.path.exists(inFile):
			print('Stock data file not found')
			print('Need an input text file containing CSV data of stocks')
			return False
		if not self.parseCSV(inFile):
			return False
		return True

	def parseCSV(self, inFile):
		error = False
		with open(inFile) as f:
			self.stock_data = f.readlines()
			for i in range(len(self.stock_data)):
				self.stock_data[i] = self.stock_data[i].split(',')
				self.stock_data[i] = [x.strip() for x in self.stock_data[i]]
			for i in range(len(self.stock_data)):
				reqEntries = {'rsu':3, 'espp':4}
				for stockOption in reqEntries:
					if(self.stock_data[i][0].lower() == stockOption):
						if(len(self.stock_data[i]) != reqEntries[stockOption]):
							print('{}'.format(', '.join(self.stock_data[i])[:-2]))
							print('Expecting {} entries for {}'.format(reqEntries[stockOption], stockOption.upper()))
							error = True
				self.stock_data[i][2] = int(self.stock_data[i][2])
				if(len(self.stock_data[i]) == 4):
					self.stock_data[i][3] = float(self.stock_data[i][3])
				if(len(self.stock_data[i]) == 3):
					self.stock_data[i].append(0.0)
				dateComps = self.stock_data[i][1].split('/')
				dateComps = [int(x) for x in dateComps]
				[m,d,y] = dateComps
				self.stock_data[i][1] = datetime.datetime(y,m,d)
			if error:
				return False
			return True

	def importDataFromCSV(self):
		return self.stock_data
