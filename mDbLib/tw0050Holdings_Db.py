from . import mLab_Conn # 自定義class - 建立連線

import datetime
from mongoengine import connect
from mongoengine import Document
from mongoengine import DateTimeField
from mongoengine import StringField
from mongoengine import IntField
from mongoengine import FloatField

# The way to link a class to an existing collection => using meta:
class Tw0050Holding(Document):
	# Meta variables.
	meta = {
		'collection': 'tw0050_holdings' # 對應到 tw0050_holdings in existing MongoDB
	}

	Year = StringField(required=True) # 年度
	Quarter = StringField(required=True) # 季度
	Code = StringField() # 股票代號
	Name = StringField() # 股票名稱
	Ratio = FloatField() # 持股比例 (Shareholding ratio)

	def __str__(self):
		return str([self.Year, self.Quarter, self.Code, self.Name, self.Ratio])




# main program entry
if __name__ == "__main__":
	myConn = mLab_Conn.MyConn()