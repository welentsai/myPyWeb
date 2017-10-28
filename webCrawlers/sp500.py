# -*- coding: utf-8 -*-

import requests 
from bs4 import Tag
from bs4 import BeautifulSoup

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

# 抓取 S&P500 某一年份 的交易資料
def getData(year):
	# 前200筆資料
	uri = uriComposer(year, '0')
	result = requests.get(uri)
	html_doc = result.content
	soup = BeautifulSoup(html_doc, 'lxml')
	rowList = [getRow(tr) for tr in soup.find("table", "historical_price").find_all("tr")]
	# print(rowList)
	print(len(rowList))

	time.sleep(0.5)   # delays for 1 seconds

	# 剩下全部 (200筆之後)
	uri = uriComposer(year, '200')
	result = requests.get(uri)
	html_doc = result.content
	soup = BeautifulSoup(html_doc, 'lxml')
	rowList2 = [getRow(tr) for tr in soup.find("table", "historical_price").find_all("tr")]
	del(rowList2[0]) # rowList2[0] => 表頭, 已存在 rowList[0]
	# print(rowList2)
	print(len(rowList2))

	rowList.extend(rowList2) # 整合一整年
	return rowList

if __name__ == "__main__":
	# year 1970 ~ 
	for i in range(1970, 2018):
		rowList = getData(str(i))
		print("Year : " + str(i) + ", count: " + str(len(rowList)))
		time.sleep(1)   # delays for 1 seconds
		print('===================')
