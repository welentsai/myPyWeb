# -*- coding: utf-8 -*-

from pprint import pprint

import mLab_Conn # 自定義class - 建立連線

from mongoengine import connect
from mongoengine import Document
from mongoengine import DateTimeField
from mongoengine import StringField
from mongoengine import IntField

import datetime

# The way to link a class to an existing collection => using meta:
class TwCap(Document):
	# Meta variables.
	meta = {
		'collection': 'twCaps' # 對應到 twCaps Document in existing MongoDB
	}

	v = IntField(db_field='__v') # 對應到 __v field 的 MongoEngine 寫法
	date = DateTimeField(default=datetime.datetime.utcnow)
	price = StringField(required=True)


# main program entry
if __name__ == "__main__":
	myConn = mLab_Conn.MyConn()

	# find with condition
	for cap in TwCap.objects(price='30951400'):
		print(cap.date, end=' , price: ')
		print(cap.price)

	# find all
	# for cap in TwCap.objects:
	# 	print(cap)