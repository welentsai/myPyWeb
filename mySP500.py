# -*- coding: utf-8 -*-
import pandas as pd
import time


from webCrawlers import sp500Spider
from mDbLib import mLab_Conn
from mDbLib import sp500Db

'''
1. fetch SP500 historical data from google finance
2. insert data into mLab DB
'''
def getSP500(year):
	df = sp500Spider.getData(str(year))
	tradings = []
	for idx, row in df.iterrows():
		# create new SP500 document
		trading = sp500Db.SP500(Date=row.Date, Open=row.Open, High=row.High, Low=row.Low, Close=row.Close, Volume=row.Volume)
		# print(trading)
		tradings.append(trading)

	print("tradings count : " + str(len(tradings)))
	# insert data into db
	sp500Db.SP500.objects.insert(tradings)

def getSP500DataFrame(year, number):
	return sp500Spider.getData(str(year), str(number))

def getLastDate():
	tradingRec = sp500Db.SP500.objects.order_by('-Date').first() # 取得最後一筆交易資料
	return tradingRec.Date

def updateNewTradings():
	lastDt = getLastDate() # get last date of trading in db
	# lastDt = '2017-10-25'
	df = getSP500DataFrame(2017, 30) # get last 30 days' trading of 2017
	df = df.set_index(['Date']) 
	# df.loc[:end_idx] => get data from first to end_idx
	df = df.loc[:lastDt] # get data from first to last date
	df =  df.drop(df.index[len(df)-1]) # drop last row (already in db)
	df = df.reset_index() # reset to auto index
	# print(df)
	if(len(df)):
		print('new tradings')
		tradings = []
		for idx, row in df.iterrows():
			# create new SP500 document
			trading = sp500Db.SP500(Date=row.Date, Open=row.Open, High=row.High, Low=row.Low, Close=row.Close, Volume=row.Volume)
			# print(trading)
			tradings.append(trading)
		print("tradings count : " + str(len(tradings)))
		print(tradings)
		# sp500Db.SP500.objects.insert(tradings)
	else:
		print('No New Data !!')


# main program entry
if __name__ == "__main__":
	myConn = mLab_Conn.MyConn() # connect to mLab DB

	updateNewTradings()


	# year 1970 ~ 
	# for year in range(1970, 2018):
	# 	print(year)
	# 	getSP500(year)
	# 	time.sleep(10)   # delays for 1 seconds

	# df = sp500.getData(str('2016'))
	# # df = df.sort_values(by=['Date'])
	# # print(df.sort_values(by=['Date']))

	# tradings = []
	# for idx, row in df.iterrows():
	# 	# create new SP500 document
	# 	trading = sp500db.SP500(Date=row.Date, Open=row.Open, High=row.High, Low=row.Low, Close=row.Close, Volume=row.Volume)
	# 	# print(new_entry)
	# 	tradings.append(trading)

	# # insert data into db
	# sp500db.SP500.objects.insert(tradings)




