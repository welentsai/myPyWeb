# -*- coding: utf-8 -*-

# 從公開資訊觀測站抓 0050 交易資料
import requests 
import json
import datetime
import time
import pandas as pd
from bs4 import Tag
from bs4 import BeautifulSoup

def cleanNum(num):
	return num.replace(',', '').replace('-', '-1')

def urlComposer(year, month, stockNo):
	# uri = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20030601&stockNo=0050'
	base = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='
	return base + str(year) + str(month).zfill(2) + '01' + '&stockNo=' + stockNo

def ROCtoAD(rocYr):
	return str(rocYr + 1911)

# 民國記年轉西元
def getAD(rocDate):
	words = rocDate.strip().split('/')
	year = ROCtoAD(int(words[0]))
	return year + '-' + words[1] + '-' + words[2]

# 某一年某月的交易資料, 回傳 => Pandas DataFrame
def getData(year, month, stockNo):
	url = urlComposer(year, month, stockNo)
	print(url)
	result = requests.get(url)
	jsonObj = json.loads(result.content)
	# print(jsonObj['fields'])
	df = pd.DataFrame.from_records(jsonObj['data'])
	df = df.drop([7,8], axis=1) # drop 7th, 8th column, axis = 1 for column, 0 for row
	df.columns = ['Date', 'Volume', 'Turnover', 'Open', 'High', 'Low', 'Close'] # 設定表頭
	# 整理資料
	df['Date'] = df['Date'].map(getAD) # # 民國轉成西元, apply a function to whole data of specific column
	df['Volume'] = df['Volume'].map(cleanNum) # 把數字裡的逗號清掉
	df['Turnover'] = df['Turnover'].map(cleanNum) # 把數字裡的逗號清掉
	#整理資料格式
	df['Date'] = pd.to_datetime(df.Date, format="%Y-%m-%d")
	df['Open'] = pd.to_numeric(df.Open, errors='coerce') # invalid parsing will be set as NaN
	df['High'] = pd.to_numeric(df.High, errors='coerce')
	df['Low'] = pd.to_numeric(df.Low, errors='coerce')
	df['Close'] = pd.to_numeric(df.Close, errors='coerce')
	df['Volume'] = pd.to_numeric(df.Volume, downcast='integer', errors='coerce')
	df['Turnover'] = pd.to_numeric(df.Turnover, downcast='integer', errors='coerce')
	return df

# 取得一整年份的交易資料, 回傳 => Pandas DataFrame
def getDataByYear(year):

	today = datetime.datetime.today()

	# from 2003-6 
	if year < 2003:
		return
	elif year == 2003:
		start = 6
	else:
		start = 1

	# 不超過今時今日
	if year == today.year:
		end = today.month + 1
	else:
		end = 13

	print("start : " + str(start) + " , end : " + str(end))

	# 建立一個空的 DataFrame
	df = getData(2003, 6, '0050')
	df = df.drop([0], axis=0) # drop [idx = 0] row, axis = 1 for column, 0 for row

	time.sleep(2)   # delays for 2 seconds
	for i in range(start, end):
		df2 = getData(year, i, '0050')
		df = df.append(df2, ignore_index=True) # 重設 index
		time.sleep(10)   # delays for 1 seconds
	return df

# main program entry
if __name__ == "__main__":
	for year in range(2003, 2018):
		df = getDataByYear(year)
		print(df)
		time.sleep(60)   # delays for 1 seconds

	# df = getDataByYear(2005)
	# print(df)
