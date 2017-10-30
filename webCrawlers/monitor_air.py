# -*- coding: utf-8 -*-

# 讀取空氣品質監測JSON
# Output : 所有監測地區 AQI數值

import json
import re # regular expression 
import requests 
from bs4 import BeautifulSoup


def getPM25():
	# 空氣品質監測JSON
	result = requests.get("https://taqm.epa.gov.tw/taqm/aqs.ashx?lang=tw&act=aqi-epa")

	jsonObj = json.loads(result.content)

	pm25List = []

	# python中, json object = dict 
	for row in jsonObj['Data']:
		# print(row)
		pm25List.append((row['SiteName'], row['AQI']))
		# print(row['SiteName'], end=' ')
		# print(row['AQI'])

	return pm25List

def display(pm25List):
	print(pm25List)
	# for row in pm25List:
	# 	print(row)
