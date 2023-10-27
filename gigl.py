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
    keyword = flask.request.args.get('keyword')
    category = flask.request.args.getlist('category')  # Use getlist since we will later use a multi-select dropdown

    # Fetch list of gigs based on the keyword / category
    gigs = get_gigs(keyword, category)

    # Check if gigs is a list (successful fetch) or an integer (error code = zero)
    if isinstance(gigs, int):
        # Handle the error, e.g., return an error page or message
        return "Error fetching gigs from the database."
	    
    html_code = flask.render_template('searchresults.html', gigs=gigs)
    response = flask.make_response(html_code)

    return response

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
	app.run(host = 'localhost', debug=True, port=8888)
