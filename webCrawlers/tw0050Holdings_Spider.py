# -*- coding: utf-8 -*-

# 從公開資訊觀測站抓 0050 每季持股明細表
import requests 
import json
import datetime
import time
import pandas as pd
import numpy as np
from bs4 import Tag
from bs4 import BeautifulSoup

# Global Variable
StockDict = None

def ADtoROC(year):
	return str(year - 1911)

# 回傳 dict(股票名稱:股票代號)
def getStockNoDict():
	# 臺灣證券交易所發行量加權股價指數成分股暨市值比重
	url = 'http://www.taifex.com.tw/chinese/9/9_7_1.asp' 
	result = requests.get(url)
	html_doc = result.content
	soup = BeautifulSoup(html_doc, 'lxml')
	table = soup.find('table')
	stockInfoL = [td.text.strip() for td in table.find_all('td')]
	stockTupleL = list(zip(stockInfoL[1::4], stockInfoL[2::4]))

	stockDict = dict((y,x) for x, y in stockTupleL)
	# 因為網頁上抓不到 => hard-code 加入
	stockDict['華映'] = '2475' # 中華映管
	stockDict['奇美電子'] = '3009' # 2010/3/18 併入群創光電
	stockDict['F-晨星'] = '3697' # 2014/2/1 併入聯發科
	stockDict['華亞科'] = '3474' # 2016/12/6 併入美光
	# 奇美電子 併入 群創光電
	# print(stockDict)
	return stockDict

# 回傳=>股票代號
def getStockNum(stockName):
	# 公司名簡稱不一致, 所以hard-code一份對照表
	HardCodeTupleL = [
										('南亞塑膠', '南亞'),
										('和泰汽車', '和泰車'),
										('彰化銀行', '彰銀'),
										('玉山金控', '玉山金'),
										('台新金控', '台新金'),
										('永豐金控','永豐金'),
										('第一金控', '第一金'),
										('寶成工業','寶成'),
										('台塑石化', '台塑化'),
										('光寶科技', '光寶科'),
										('仁寶電腦', '仁寶'),
										('群創光電', '群創'),
										('可成科技', '可成'),
										('裕隆汽車', '裕隆'),
										('中華汽車', '中華'),
										('長榮海運', '長榮'),
										('凌陽科技', '凌陽'),
										('微星科技', '微星'),
										('錸德科技', '錸德'),
										('陽明海運', '陽明'),
										('威盛電子', '威盛'),
										('合庫', '合庫金'),
										('聯強國際', '聯強'),
										('長榮航空', '長榮航'),
										('裕隆日產', '裕日車')
										]

	hardCodeDict = dict((x,y) for x, y in HardCodeTupleL)

	try:
		value = StockDict[stockName]
	except KeyError:
		try:
			newKey = hardCodeDict[stockName]
			value = StockDict[newKey]
			# print('' + stockName + ' => ' +  newKey + ' => ' + value)
		except KeyError:
			print('' + stockName + ' => NaN')
			value = np.nan
	return value

# 把ratio string 轉成 float
def getRatio(ratioStr):
	ratioStr = ratioStr.replace('%', '') #清掉%
	return float(ratioStr)

# year from 2003
# quarter = [1, 2, 3, 4] , 4個會計計度
def getData(year, quarter):
	if quarter > 4 or quarter < 1: return None  # wrong quarter, early return 
	global StockDict # explict refer to global variable 
	if StockDict is None: 
		StockDict = getStockNoDict() # initialize global variable
	print("year : " + str(year) + " quarter : " + str(quarter))
	url = 'http://mops.twse.com.tw/mops/web/ajax_t78sb04'
	payload = { # python dict data-type
		'encodeURIComponent':'1',
		'TYPEK':'all',
		'step':'1',
		'run':'Y',
		'firstin':'true',
		'FUNTYPE': '02',
		'year': ADtoROC(year),
		'season': str(quarter).zfill(2) ,
		'fund_no':'0'
	}
	# print(payload)
	result = requests.post(url, data=payload)
	html_doc = result.content
	soup = BeautifulSoup(html_doc, 'lxml')

	table = soup.find("table", "noBorder")
	if table == None : return None # early return 
	column = [tag.text.strip() for tag in table.find_all('td')]

	table = soup.find("table", "hasBorder")
	if table == None : return None # early return
	title = [tag.text.strip() for tag in table.find_all('th')]
	stockHodingList = [tag.text.strip() for tag in table.find_all('td')]
	stockTupleL = list(zip(stockHodingList[0::4], stockHodingList[1::4]))
	stockTupleL = stockTupleL[:-2] # remove last 2 elements from list, 移除垃圾資料

	df = pd.DataFrame(stockTupleL)
	df.columns = ['Name', 'Ratio'] # 設定Column名稱
	df['Ratio'] = df['Ratio'].map(getRatio) # 整理資料格式
	df['Code'] = df['Name'].map(getStockNum) # 新增 Column, 股票代號
	df['Year'] = str(year) # 新增 Column, 年度
	df['Quarter'] = str(quarter).zfill(2) # 新增 Column, 季度
	return df

def getDataByYear(year):
	df = pd.DataFrame() # create a empty dataframe
	for quarter in range(1,5):
		df2 = getData(year, quarter)
		if not (df2 is None): # 使用 is keyword 來檢查 None
			print(df2)
			df = df.append(df2, ignore_index=True) # 重設 index
		time.sleep(5)
	return df

# main program entry
if __name__ == "__main__":
	# StockDict = getStockNoDict()
	df = getDataByYear(2017)
	print(df)