# -*- coding: utf-8 -*-

from flask import Flask, url_for, redirect
from flask import request

app = Flask(__name__)

# Static Rules
@app.route('/')
def index():
	# return 'Index Page'
	return redirect(url_for('hello'))

@app.route('/hello')
def hello():
	return 'Hello, World'

# Variable Rules
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'Hello %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/projects/')
def projects():
	return 'The project page'

with app.test_request_context('/test', method='GET'):
	# now you can do something with the request until the
	# end of the with block, such as basic assertions:
	assert request.path == '/test'
	assert request.method == 'GET'
