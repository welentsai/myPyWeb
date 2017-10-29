# -*- coding: utf-8 -*-

import requests 
from bs4 import Tag
from bs4 import BeautifulSoup

import pandas as pd

import datetime
import time

uri_1 = "https://finance.google.com/finance/historical?cid=626307&startdate=Jan+1%2C+1970&enddate=Dec+31%2C+1970&num=200";
uri_2 = "https://finance.google.com/finance/historical?cid=626307&startdate=Jan+1%2C+1970&enddate=Dec+31%2C+1970&num=200&start=200";

uri = "https://finance.google.com/finance/historical?cid=626307&startdate=Jan+1%2C+";

# 組成&回傳 URL
def uriComposer(year, startNo):
	uri = "https://finance.google.com/finance/historical?cid=626307&startdate=Jan+1%2C+";
	return uri + year + "&enddate=Dec+31%2C+" + year + "&num=200" + "&start=" + startNo;	

# 把數字裡的逗號清掉
# 把數字裡的'-'換成 '-1' => 沒有交易資料
def cleanNum(num):
	return num.replace(',', '').replace('-', '-1')

# 整理一行資料
# datetime.datetime.strptime() => convert a date_string to a datetime object
# strftime() => convert datetime to date string with specific format
def getRow(trTag):
	thRow = trTag.find_all("th")
	if thRow:
		return [th.get_text().strip() for th in thRow]
	else:
		tdRow = [td.get_text().strip() for td in trTag.find_all("td")]
		tdRow[0] = datetime.datetime.strptime(tdRow[0], "%b %d, %Y").strftime('%Y-%m-%d')
		tdRow[1] = float(cleanNum(tdRow[1]))  
		tdRow[2] = float(cleanNum(tdRow[2]))
		tdRow[3] = float(cleanNum(tdRow[3]))
		tdRow[4] = float(cleanNum(tdRow[4]))
		tdRow[5] = int(cleanNum(tdRow[5]))
		return tdRow

# 從網站上把 HTML Table 抓下來, 並轉成 pandas dataframe
def getDataFrame(url):
	result = requests.get(url)
	html_doc = result.content
	soup = BeautifulSoup(html_doc, 'lxml')
	table = soup.find("table", "historical_price")
	df = pd.read_html(str(table))[0] # 1. convert BeautifulSoup object into a String , 2. get first table
	df.columns = list(df.iloc[0]) # rename column from first row
	return df.drop([0]) # drop first row, it is ccolumn name

# 抓取 S&P500 某一年份 的交易資料
# 用 pandas 存放 table
def getData(year):
	# 讀取前200筆
	uri = uriComposer(year, '0')
	df1 = getDataFrame(uri)
	time.sleep(0.5)   # delays for 0.5 seconds
	# 剩下全部 (200筆之後)
	uri = uriComposer(year, '200')
	df2 = getDataFrame(uri)

	df = pd.concat([df1, df2], ignore_index=True)
	df['Date'] = pd.to_datetime(df.Date, format="%b %d, %Y")
	df['Open'] = pd.to_numeric(df.Open, errors='coerce') # invalid parsing will be set as NaN
	df['High'] = pd.to_numeric(df.High, errors='coerce')
	df['Low'] = pd.to_numeric(df.Low, errors='coerce')
	df['Close'] = pd.to_numeric(df.Close, errors='coerce')
	df['Volume'] = pd.to_numeric(df.Volume, downcast='unsigned', errors='coerce')

	return df # re-index

# main entry 
if __name__ == "__main__":
	# year 1970 ~ 
	for i in range(2015, 2018):
		df = getData(str(i))
		# print(df.sort_values(by=['Date']))
		print(df)
		print("Year : " + str(i) + ", count: " + str(len(df)))
		print('===================')
		time.sleep(1)   # delays for 1 seconds

