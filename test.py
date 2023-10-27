#!usr/bin/env python

import flask

app = flask.Flask(__name__, template_folder='templates/')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response