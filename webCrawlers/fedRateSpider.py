# -*- coding: utf-8 -*-

# New York Fed 的網頁抓取 FED Fund Rate 
# Note : EFFR for "effective federal funds rate"

import os
import re
import requests 
import datetime
import time
import pandas as pd
import numpy as np
from bs4 import Tag
from bs4 import BeautifulSoup

# 清除日期字串中的其他字元
def cleanDate(dateStr):
	regex = re.compile('[a-zA-Z]')
	#First parameter is the replacement, second parameter is your input string
	return regex.sub('', dateStr) # remove alphabet from date string

def getData(startDate, endDate):
	url = 'https://apps.newyorkfed.org/markets/autorates/fed-funds-search-result-page'
	# start = '1/01/2017'
	# end = '11/09/2017'
	payload = {
		'txtDate1':startDate,
		'txtDate2':endDate,
		'submit.x':'94',
		'submit.y':'11'
	}

	result = requests.post(url, data=payload)
	html_doc = result.content
	soup = BeautifulSoup(html_doc, 'lxml')
	table = soup.find("table", "greyborder")

	df = pd.read_html(str(table))[0] # 1. convert BeautifulSoup object into a String , 2. get first table
	df = df.drop([0,2,4,5,6,7,8,9,10,11], axis=1) # drop 7th, 8th column, axis = 1 for column, 0 for row
	df.columns = list(df.iloc[0]) # rename column from row[0]
	df = df.drop([0,1]) # drop row[0] and row[1]
	df = df.reset_index(drop=True) # drop = true => not insert index column, using default auto-index
	df.columns = ['Date', 'Rate'] # 設定Column名稱
	df['Date'] = df['Date'].map(cleanDate) # 整理資料格式
	df['Date'] = pd.to_datetime(df.Date, format="%m/%d/%Y")
	df['Rate'] = pd.to_numeric(df.Rate, errors='coerce') # invalid parsing will be set as NaN
	return df

def getDataFromCSV(file):
	df = pd.read_csv(file)
	df.columns = ['Date', 'Rate'] # 設定Column名稱
	df['Date'] = pd.to_datetime(df.Date, format="%Y-%m-%d")
	df['Rate'] = pd.to_numeric(df.Rate, errors='coerce') # invalid parsing will be set as NaN
	return df


# main program entry
if __name__ == "__main__":
	# load historial data (from 1954)
	mydir = os.path.dirname(os.path.abspath(__file__)) # get the path to current file
	subdir = 'dataSrc'
	file = 'fed-funds-rate-historical.csv'
	abs_file_path = os.path.join(mydir, subdir, file)
	print(abs_file_path)
	getDataFromCSV(abs_file_path)

	# fetch fund rate from NYFed
	getData('01/01/2017', '01/31/2017')