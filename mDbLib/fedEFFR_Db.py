# -*- coding: utf-8 -*-
from . import mLab_Conn # 自定義class - 建立連線

import datetime
from mongoengine import connect
from mongoengine import Document
from mongoengine import DateTimeField
from mongoengine import StringField
from mongoengine import IntField
from mongoengine import FloatField

class FedRate(Document):
	meta = {
		'collection': 'fedrate' # 對應到 collection in DB
	}
	Date = DateTimeField(required=True)
	Rate = FloatField() # Effective Fed Fund Rate

	def __str__(self):
		return str([self.Date, self.Rate])

# main program entry
if __name__ == "__main__":
	myConn = mLab_Conn.MyConn()