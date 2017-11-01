# -*- coding: utf-8 -*-
from . import mLab_Conn # 自定義class - 建立連線

import datetime

from mongoengine import connect
from mongoengine import Document
from mongoengine import DateTimeField
from mongoengine import StringField
from mongoengine import IntField
from mongoengine import FloatField
from mongoengine import ListField

class TaskRec(Document):
	meta = {
		'collection': 'taskRecs' # 對應到 task records collection in DB
	}
	Date = DateTimeField(default=datetime.datetime.utcnow)
	Op = StringField(required=True) # task operation 
	Dur = StringField(required=True) # task duration [daily, monthly]
	Raw = ListField(StringField(max_length=500)) # Raw Data List

	# print object instance
	def __str__(self):
		return str([self.Date, self.Op, self.Dur, self.Raw]) + ' Raw Data Length : ' +str(len(self.Raw))