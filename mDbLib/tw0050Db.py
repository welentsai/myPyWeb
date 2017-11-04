# -*- coding: utf-8 -*-

from . import mLab_Conn # 自定義class - 建立連線

import datetime
from mongoengine import connect
from mongoengine import Document
from mongoengine import DateTimeField
from mongoengine import StringField
from mongoengine import IntField
from mongoengine import FloatField

# The way to link a class to an existing collection => using meta:
class Tw0050(Document):
	# Meta variables.
	meta = {
		'collection': 'tw0050' # 對應到 tw0050 in existing MongoDB
	}

	Date = DateTimeField(required=True)
	Open = FloatField() # 開盤價
	High = FloatField() # 最高價
	Low = FloatField() # 最低價
	Close = FloatField() # 收盤價
	Volume = IntField() # 成交量
	Turnover = IntField() # 成交金額

	def __str__(self):
		return str([self.Date, self.Open, self.High, self.Low, self.Close, self.Volume, self.Volume])

# main program entry
if __name__ == "__main__":
	myConn = mLab_Conn.MyConn()

	# for trading in Tw0050.objects(cp='47.30'): # 收盤價 = '47.30'
	# 	print(trading.date, end=' , close price: ')
	# 	print(trading.cp)
