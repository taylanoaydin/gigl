#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import os
import time
import flask
import database
import auth

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

app.secret_key = os.urandom(12).hex()

#-----------------------------------------------------------------------

def get_ampm():
    if time.strftime('%p') == "AM":
        return 'morning'
    return 'afternoon'

def get_current_time():
    return time.asctime(time.localtime())

#-----------------------------------------------------------------------

# Routes for authentication.

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return auth.logoutcas()

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    username = auth.authenticate()

    html_code = flask.render_template('index.html',
        username=username,
        ampm=get_ampm(),
        current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/searchform', methods=['GET'])
def search_form():

    username = auth.authenticate()

    prev_author = flask.request.cookies.get('prev_author')
    if prev_author is None:
        prev_author = '(None)'

    html_code = flask.render_template('searchform.html',
        username=username,
        ampm=get_ampm(),
        current_time=get_current_time(),
        prev_author=prev_author)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/searchresults', methods=['GET'])
def search_results():

    username = auth.authenticate()

    author = flask.request.args.get('author')
    if author is None:
        author = ''
    author = author.strip()

    if author == '':
        prev_author = '(None)'
        books = []
    else:
        prev_author = author
        books = database.get_books(author) # Exception handling omitted

    html_code = flask.render_template('searchresults.html',
        username=username,
        ampm=get_ampm(),
        current_time=get_current_time(),
        author=prev_author,
        books=books)
    response = flask.make_response(html_code)
    response.set_cookie('prev_author', prev_author)
    return response
