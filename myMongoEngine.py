# -*- coding: utf-8 -*-

import json

from mongoengine import connect
from mongoengine import Document
from mongoengine import DateTimeField
from mongoengine import StringField
from mongoengine import IntField

import datetime

def js_r(filename):
	''' Deserialize JSON from file to dict object '''
	with open(filename) as f_in:
		return(json.load(f_in)) # deserialize JSON to dict object

def get_Conn():
	''' connects to mLab '''
	conf = js_r('config.json')
	connStr = 'mongodb://' + conf['mgUser'] + ':' + conf['mgPwd'] + '@' + conf['mgUri']
	client = connect('welendb', host=connStr)
	print(client)

# The way to link a class to an existing collection => using meta:
class TwCap(Document):
	# Meta variables.
	meta = {
		'collection': 'twCaps' # 對應到 twCaps Document in existing MongoDB
	}
	v = IntField(db_field='__v') # 對應到 __v field 的 MongoEngine 寫法
	date = DateTimeField(default=datetime.datetime.utcnow)
	price = StringField(required=True)

get_Conn() # 連線初始化

# find all
# for cap in TwCap.objects:
# 	print(cap)

# main program entry
if __name__ == "__main__":
	# find with condition
	for cap in TwCap.objects(price='30951400'):
		print(cap.date, end=' , price: ')
		print(cap.price)
