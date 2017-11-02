# -*- coding: utf-8 -*-
from . import mLab_Conn # 自定義class - 建立連線

import datetime
from mongoengine import connect
from mongoengine import Document
from mongoengine import DateTimeField
from mongoengine import StringField
from mongoengine import IntField
from mongoengine import FloatField

class SP500(Document):
	meta = {
		'collection': 'sp500' # 對應到 sp500 collection in DB
	}
	Date = DateTimeField(required=True)
	Open = FloatField()
	High = FloatField()
	Low = FloatField()
	Close = FloatField()
	Volume = IntField()

	def __str__(self):
		return str([self.Date, self.Open, self.High, self.Low, self.Close, self.Volume])

# main program entry
if __name__ == "__main__":
	myConn = mLab_Conn.MyConn()
