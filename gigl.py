#!/usr/bin/env python

#-----------------------------------------------------------------------
# gigl.py
# Authors: TA, AB, IA, YD
#-----------------------------------------------------------------------

import flask
import auth
import os
import database
from datetime import datetime
#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='templates/')
app.secret_key = os.urandom(12).hex()

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    username = auth.authenticate()

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
    netid = auth.authenticate()
    user = database.get_user(netid) # This is returning none
    #TODO: Error Handling for DB failure
    username = user.get_name()
    user_email = f"{netid}@princeton.edu"
    html_code = flask.render_template('postgig.html', username=username,
                                      user_email=user_email) 
    response = flask.make_response(html_code)
    return response
#-----------------------------------------------------------------------
@app.route('/profile', methods=['GET'])
def profile():
    return
#-----------------------------------------------------------------------
@app.route('/gigposted', methods=['POST'])
def gigposted():
    netid = auth.authenticate()
    gig_form = flask.request.form
    start_date = gig_form.get('start_date')
    end_date = gig_form.get('end_date')
    qualif = gig_form.get('qualifications')
    title = gig_form.get('title')
    category = gig_form.get('category')
    description = gig_form.get('description')
    posted = datetime.now().date()
    database.create_gig(netid, title, category, description,
                        qualif, start_date, end_date, posted)
    html_code = flask.render_template('gigposted.html')
    response = flask.make_response(html_code)
    return response
#-----------------------------------------------------------------------
@app.route('/deletegig', methods=['POST'])
def deletegig():
    
    return
#-----------------------------------------------------------------------
if __name__ == '__main__':
	app.run(host = 'localhost', debug=True, port=8888)