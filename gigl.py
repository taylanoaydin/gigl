#!/usr/bin/env python

#-----------------------------------------------------------------------
# gigl.py
# Authors: TA, AB, IA, YD
#-----------------------------------------------------------------------

import flask
import auth
import os
import sys
import database
from datetime import datetime
from cas_details import cas_details
#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='templates/')
app.secret_key = os.urandom(12).hex()

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    netid = auth.authenticate()
    username = database.get_user(netid).get_name()

    if not database.check_and_add_user(netid):
        return "Error handling omitted"
    
    html_code = flask.render_template('index.html', usrname=username)
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
    auth.authenticate()

    keyword = flask.request.args.get('keyword')
    category = flask.request.args.getlist('category')  # Use getlist since we will later use a multi-select dropdown
    cat = category[0]
    if category == ['']:
        category = []

    # Fetch list of gigs based on the keyword / category
    gigs = database.get_gigs(keyword=keyword, categories=category)

    # Check if gigs is a list (successful fetch) or an integer (error code = zero)
    #if isinstance(gigs, int):
        # Handle the error, e.g., return an error page or message
        # return "Error fetching gigs from the database."
    html_code = flask.render_template('searchresults.html',
                                        mygigs=gigs,
                                        cat=cat,
                                        kw=keyword)
    response = flask.make_response(html_code)

    return response

#-----------------------------------------------------------------------
@app.route('/details/<int:id>', methods=['GET'])
def details(id):
    netid = auth.authenticate()
    gig = database.get_gig_details(id)
    gigTitle = gig.get_title()
    gigNetID = gig.get_netid()
    gigAuthor = database.get_user(gigNetID).get_name()
    gigCategory = gig.get_category()
    gigDescription = gig.get_description()
    gigQualifications = gig.get_qualifications()
    gigStartDate = gig.get_fromdate()
    gigEndDate = gig.get_til_date()
    gigPostedDate = gig.get_post_date()

    owns = database.owns_gig(netid, id) # boolean
    if owns:
        all_apps = database.get_apps_for(id)
        application = None
    else:
        all_apps = None
        application = database.get_application(netid, id)

    html_code = flask.render_template('details.html', 
                                        gigTitle=gigTitle,
                                        gigPoster=gigAuthor,
                                        gigCategory=gigCategory,
                                        gigDescription=gigDescription,
                                        gigQualifications=gigQualifications,
                                        gigStartDate=gigStartDate,
                                        gigEndDate=gigEndDate,
                                        gigPostedDate=gigPostedDate,
                                        is_owner=owns,
                                        application=application,
                                        all_apps=all_apps,
                                        gigID=id)
    response = flask.make_response(html_code)
    return response
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
    netid = auth.authenticate()
    user = database.get_user(netid)
    username = user.get_name()
    user_email = f"{netid}@princeton.edu"

    mygigs = database.get_gigs_posted_by(netid)
    myapps = database.get_apps_by(netid)

    html_code = flask.render_template('profile.html', username=username,
                                      user_email=user_email,
                                      mygigs=mygigs,
                                      myapps=myapps)
    response = flask.make_response(html_code)     
    return response
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
    gigID = database.create_gig(netid, title, category, description,
                        qualif, start_date, end_date, posted)
    html_code = flask.render_template('gigposted.html',
                                        gigID = int(gigID))
    response = flask.make_response(html_code)
    return response
#-----------------------------------------------------------------------
@app.route('/deletegig', methods=['POST'])
def deletegig():
    
    return
#-----------------------------------------------------------------------
@app.route('/apply', methods=['POST'])
def apply():
    netid = auth.authenticate()
    gigID = flask.request.form.get("apply")
    message = flask.request.form.get("msg")

    if database.owns_gig(netid, gigID):
        html_code = flask.render_template('apply_error.html',
                                            gigID = int(gigID),
                                            err="You can't apply to your own gig...")
        response = flask.make_response(html_code)
        return response
    
    application = database.get_application(netid, gigID)
    if application is not None:
        html_code = flask.render_template('apply_error.html',
                                            gigID = int(gigID),
                                            err="You have already applied...")
        response = flask.make_response(html_code)
        return response

    if database.send_application(netid, gigID, message):
        html_code = flask.render_template('apply_error.html',
                                            gigID = int(gigID),
                                            err="You have successfully applied!")
        response = flask.make_response(html_code)
        return response
    else:
        html_code = flask.render_template('apply_error.html',
                                            gigID = int(gigID),
                                            err="Application couldn't be sent due to a database error.")
        response = flask.make_response(html_code)
        return response
#-----------------------------------------------------------------------
if __name__ == '__main__':
	app.run(host = 'localhost', debug=True, port=8888)
