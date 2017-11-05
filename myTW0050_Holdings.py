# -*- coding: utf-8 -*-
import pandas as pd
import datetime
import time

from webCrawlers import tw0050Holdings_Spider
from mDbLib import mLab_Conn
from mDbLib import tw0050Holdings_Db

# 回傳 => 最後一筆交易 (年份, 季度) tuple
def findLast():
	lastYr = tw0050Holdings_Db.Tw0050Holding.objects.order_by('-Year').first().Year # 取得最後一筆交易年份
	lastQtr = tw0050Holdings_Db.Tw0050Holding.objects(Year=lastYr).order_by('-Quarter').first().Quarter # 取得最後一筆交易季度
	return (int(lastYr), int(lastQtr))

# input => datetime.date
# 回傳 => 日期所在的(年份, 季度) tuple
def completed_quarter(dt):
	prev_quarter_map = ((1, 0), (2, 0), (3, 0), (4, 0))
	quarter, yd = prev_quarter_map[(dt.month - 1) // 3] # 整數除法, 以[0~11] map to [0~3]的結果
	return (dt.year + yd, quarter)

# update 一個季度的資料
def updateHoldingsByQuarter(year, quarter):
	# print('updateHoldingsByQuarter() => ' + str(year) + ", " + str(quarter))
	df = tw0050Holdings_Spider.getData(year, quarter)
	if df == None:
		print('None Data !!')
		return None # early Return

	if(len(df)):
		# print('new tradings')
		holdings = []
		for idx, row in df.iterrows():
			# create new Tw0050 holding document
			holding = tw0050Holdings_Db.Tw0050Holding(Year=row.Year, Quarter=row.Quarter, Code=row.Code, Name=row.Name, Ratio=row.Ratio)
			# print(holding)
			holdings.append(holding)
		print("New Holdings count : " + str(len(holdings)))
		tw0050Holdings_Db.Tw0050Holding.objects.insert(holdings)
	else:
		print('No New Data !!')

def updateHoldings(year):
	print('updateHoldings() => ' + str(year))
	df = tw0050Holdings_Spider.getDataByYear(year)
	if df == None: return None # early return
	# print(df)	
	if(len(df)):
		# print('new tradings')
		holdings = []
		for idx, row in df.iterrows():
			# create new Tw0050 holding document
			holding = tw0050Holdings_Db.Tw0050Holding(Year=row.Year, Quarter=row.Quarter, Code=row.Code, Name=row.Name, Ratio=row.Ratio)
			# print(holding)
			holdings.append(holding)
		print("New Holdings count : " + str(len(holdings)))
		# tw0050Holdings_Db.Tw0050Holding.objects.insert(holdings)
	else:
		print('No New Data !!')

# main program entry
if __name__ == "__main__":
	myConn = mLab_Conn.MyConn() # connect to mLab DB

	
	todayTuple = completed_quarter(datetime.date.today()) 
	lastDTuple = findLast() # last record in db

	if todayTuple > lastDTuple: # 新季度
		print('Neq Quarter !!  Try to update if data is ready ...')
		updateHoldingsByQuarter(todayTuple[0], todayTuple[1])
		# updateHoldingsByQuarter(2017, 3)
	else:
		print("Not a New Quarter !!")


	# year start from 2003
	# for year in range(2003, 2018):
	# 	updateHoldings(year)
	# 	time.sleep(30)   # delays for 1 minute

	# last = findLast()
	# print(last)