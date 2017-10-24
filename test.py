# -*- coding: utf-8 -*-

# from flask import g # flask.g => flask application object for store information

import json

print(__name__)

mydict = dict(
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
)

def connect_db():
  """Connects to the specific database."""
  # rv = sqlite3.connect(current_app.config['DATABASE'])
  # rv.row_factory = sqlite3.Row
  # return rv
  return "OK"

def get_db():
	"""Opens a new database connection if there is none yet for the
	current application context.
	"""
	if not 'sqlite_db' in mydict:
		mydict['sqlite_db'] = connect_db()
	return mydict['sqlite_db']

def js_r(filename):
	with open(filename) as f_in:
		return(json.load(f_in)) # deserialize JSON to dict object

print(mydict)

print(mydict['USERNAME'])

print(get_db())

print(mydict)

my_data = js_r('config.json')
print(my_data)

print(my_data['username'])