# -*- coding: utf-8 -*-

import mLab_Conn # 自定義class - 建立連線

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
		'collection': 'tradings' # 對應到 tradings in existing MongoDB
	}

	v = IntField(db_field='__v') # 對應到 __v field 的 MongoEngine 寫法

	date = DateTimeField(default=datetime.datetime.utcnow)
	vol = StringField(required=True) # 成交量
	to = StringField(required=True) # 成交金額
	op = StringField(required=True) # 開盤價
	th = StringField(required=True) # 最高價
	tl = StringField(required=True) # 最低價
	cp = StringField(required=True) # 收盤價
	chg = StringField(required=True) # 漲跌價差
	txn = StringField(required=True) # 成交筆數

# main program entry
if __name__ == "__main__":
	myConn = mLab_Conn.MyConn()

	for trading in Tw0050.objects(cp='47.30'): # 收盤價 = '47.30'
		print(trading.date, end=' , close price: ')
		print(trading.cp)
