# -*- coding: utf-8 -*-

from pprint import pprint

import json
import os
from mongoengine import connect

'''
mLab Connection Class
1. read data from config.json 
2. build connection at init()
3. only keep/share single connection client
'''
class MyConn:

	''' static variable, client connection only build once '''
	__client__ = None

	''' Constructor '''
	def __init__(self):
		if MyConn.__client__ is None:
			mydir = os.path.dirname(os.path.abspath(__file__)) # get the path to current file
			self.conf = self.js_r(os.path.join(mydir, 'config.json')) # fetch config file in module
			self.connStr = 'mongodb://' + self.conf['mgUser'] + ':' + self.conf['mgPwd'] + '@' + self.conf['mgUri']
			MyConn.__client__ = connect('welendb', host=self.connStr)
			print(MyConn.__client__)
			print('*** Successfully connected to mLab !! ***')
		else:
			print('Connection has been builded already !!')

	''' Destructor '''
	def __del__(self):
		print('*** The connection instance is about to be destroyed !! ***')
		MyConn.__client__.close()  # close the connection
		# print(MyConn.__client__)

	''' Deserialize JSON from file to dict object '''
	def js_r(self, filename):
		with open(filename) as f_in:
			return(json.load(f_in)) # deserialize JSON to dict object

	''' Serialize dict to JSON file '''
	def js_w(filename):
		with open(filename, 'w') as f_out:
			json.dump(my_data, f_out, ensure_ascii=False)
			return 'write file successed !!'


''' main program entry ''' 
if __name__ == "__main__":
	myConn = MyConn()
	myConn2 = MyConn()
	pprint(dir(MyConn.__client__)) # list all attributes and methods of an object