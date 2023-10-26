#!/usr/bin/env python

#-----------------------------------------------------------------------
# gigl.py
# Authors: TA, AB, IA, YD
#-----------------------------------------------------------------------

import flask
import auth
import os
#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='templates/')
app.secret_key = os.urandom(12).hex()

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
@app.route('/home', methods=['GET'])
def home():
    username = auth.authenticate()
    html_code = flask.render_template('home.html',
                                      username=username)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
@app.route('/searchresults', methods=['GET'])
def search_results():
    return
#-----------------------------------------------------------------------
@app.route('/details', methods=['GET'])
def details():
    return
#-----------------------------------------------------------------------
@app.route('/postgig', methods=['GET'])
def postgig():
    return
#-----------------------------------------------------------------------
@app.route('/profile', methods=['GET'])
def profile():
    return
#-----------------------------------------------------------------------
@app.route('/gigposted', methods=['POST'])
def gigposted():
    return
#-----------------------------------------------------------------------
@app.route('/deletegig', methods=['POST'])
def deletegig():
    return
#-----------------------------------------------------------------------
if __name__ == '__main__':
	app.run(debug=True, port=8888)