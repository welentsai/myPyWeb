# -*- coding: utf-8 -*-

# from flask import g # flask.g => flask application object for store information

import json
from pymongo import MongoClient

# mydict = dict(
# 	SECRET_KEY='development key',
# 	USERNAME='admin',
# 	PASSWORD='default'
# )

def js_r(filename):
	''' Deserialize JSON from file to dict object '''
	with open(filename) as f_in:
		return(json.load(f_in)) # deserialize JSON to dict object

def js_w(filename):
	''' Serialize dict to JSON file '''
	with open(filename, 'w') as f_out:
		json.dump(my_data, f_out, ensure_ascii=False)
		return 'write file successed !!'

def get_Conn():
	''' connects to mLab '''
	conf = js_r('config.json')
	connStr = 'mongodb://' + conf['mgUser'] + ':' + conf['mgPwd'] + '@' + conf['mgUri']
	client = MongoClient(connStr)
	if hasattr(client, 'welendb'):
		return client.welendb

# main program entry
if __name__ == "__main__":
	db = get_Conn()
	tradings = db.tradings # same =>  db['tradings']
	print('total data count is ' + str(tradings.count()))

