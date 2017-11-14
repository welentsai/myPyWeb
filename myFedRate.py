# -*- coding: utf-8 -*-
import os
import pandas as pd
import datetime
import time

from webCrawlers import fedRateSpider
from mDbLib import mLab_Conn
from mDbLib import fedEFFR_Db

def findLast():
	return fedEFFR_Db.FedRate.objects.order_by('-Date').first() # 取得最後一筆交易資料

def updateDataFromCSV(file):
	df = fedRateSpider.getDataFromCSV(file)
	# print(df)
	if(len(df)):
		rates = []
		for idx, row in df.iterrows():
			rate = fedEFFR_Db.FedRate(Date=row.Date, Rate=row.Rate)
			rates.append(rate)
		print("New rates count : " + str(len(rates)))
		# print(rates)
		fedEFFR_Db.FedRate.objects.insert(rates)
	else:
		print('No New Data !!')

def updateFedRates():
	startDate = fedEFFR_Db.FedRate.objects.order_by('-Date').first().Date # 取得最後一筆資料的日期
	endDate = datetime.date.today()
	# print(startDate.strftime("%Y-%m-%d"))
	# print(endDate)
	df = fedRateSpider.getData(startDate, endDate)
	df =  df.drop(df.index[len(df)-1]) # drop last row, startDate, (already in db)
	if(len(df)):
		rates = []
		for idx, row in df.iterrows():
			rate = fedEFFR_Db.FedRate(Date=row.Date, Rate=row.Rate)
			rates.append(rate)
		print("New rates count : " + str(len(rates)))
		# print(rates)
		fedEFFR_Db.FedRate.objects.insert(rates)
	else:
		print('No New Data !!')
	# return df

# main program entry
if __name__ == "__main__":
	myConn = mLab_Conn.MyConn() # connect to mLab DB
	# mydir = os.path.dirname(os.path.abspath(__file__)) # get the path to current file
	# subdir = 'webCrawlers\dataSrc'
	# file = 'fed-funds-rate-historical.csv'
	# abs_file_path = os.path.join(mydir, subdir, file)
	# updateDataFromCSV(abs_file_path)

	# updateFedRates('01/01/2017', '12/31/2017')
	updateFedRates()
	# print(df)
