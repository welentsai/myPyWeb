# -*- coding: utf-8 -*-
import pandas as pd
import datetime
import time

from webCrawlers import tw0050Spider
from mDbLib import mLab_Conn
from mDbLib import tw0050Db

def findLast():
	return tw0050Db.Tw0050.objects.order_by('-Date').first() # 取得最後一筆交易資料

def updateLastTradings():
	today = datetime.datetime.today()
	df = tw0050Spider.getData(today.year, today.month, '0050')
	df = df.set_index(['Date'])
	lastDt = tw0050Db.Tw0050.objects.order_by('-Date').first().Date # 取得最後一筆交易資料
	# lastDt = '2017-11-01'
	print('last record date in db => ' + str(lastDt))
	# print(df)
	df = df.loc[lastDt:] # get the rest data from last date
	df =  df.drop(df.index[0]) # drop first row (already in db)
	df = df.reset_index() # reset to auto index
	# print(df)
	if(len(df)):
			# print('new tradings')
			tradings = []
			for idx, row in df.iterrows():
				# create new Tw0050 document
				trading = tw0050Db.Tw0050(Date=row.Date, Open=row.Open, High=row.High, Low=row.Low,
																	Close=row.Close, Volume=row.Volume, Turnover=row.Turnover)
				# print(trading)
				tradings.append(trading)
			print("New tradings count : " + str(len(tradings)))
			print(tradings)
			# tw0050Db.Tw0050.objects.insert(tradings)
	else:
		print('No New Data !!')

def updateTradings(year):
	print('updateTradings() => ' + str(year))
	df = tw0050Spider.getDataByYear(year)
	# print(df)

	if(len(df)):
		# print('new tradings')
		tradings = []
		for idx, row in df.iterrows():
			# create new Tw0050 document
			trading = tw0050Db.Tw0050(Date=row.Date, Open=row.Open, High=row.High, Low=row.Low,
																Close=row.Close, Volume=row.Volume, Turnover=row.Turnover)
			# print(trading)
			tradings.append(trading)
		print("New tradings count : " + str(len(tradings)))
		# print(tradings)
		tw0050Db.Tw0050.objects.insert(tradings)
	else:
		print('No New Data !!')

# main program entry
if __name__ == "__main__":
	myConn = mLab_Conn.MyConn() # connect to mLab DB

	updateLastTradings()

	# updateTradings(2009)

	# for year in range(2003, 2018):
	# 	updateTradings(year)
	# 	time.sleep(30)   # delays for 1 minute
	# last = findLast()
	# print(last)
