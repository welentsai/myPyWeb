# -*- coding: utf-8 -*-
import pandas as pd


from webCrawlers import sp500
from mDbLib import mLab_Conn
from mDbLib import sp500db

'''
1. fetch SP500 historical data from google finance
2. insert data into mLab DB
'''
def getSP500():
	df = sp500.getData(str('2016'))
	tradings = []
	for idx, row in df.iterrows():
		# create new SP500 document
		trading = sp500db.SP500(Date=row.Date, Open=row.Open, High=row.High, Low=row.Low, Close=row.Close, Volume=row.Volume)
		# print(trading)
		tradings.append(trading)

	# insert data into db
	sp500db.SP500.objects.insert(tradings)


# main program entry
if __name__ == "__main__":
	myConn = mLab_Conn.MyConn() # connect to mLab DB

	getSP500()

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




