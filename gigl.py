#!/usr/bin/env python

#-----------------------------------------------------------------------
# gigl.py
# Authors: TA, AB, IA, YD
#-----------------------------------------------------------------------

import flask
from flask_mail import Mail
from flask import Flask
import auth
import os
import dotenv
import database
from datetime import datetime
from cas_details import cas_details
from forms import ApplyForm, DeleteGigForm, PostGigForm
from flask_mail import Message
from flask import current_app
import sys



#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates/')
dotenv.load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'developmenttemp123')

#-----------------------------------------------------------------------

# Configure Flask-Mail with environment variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'giglprinc3ton@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PW']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Initialize Flask-Mail
mail = Mail(app)

def send_email(to_email, subject, body):
    msg = Message(subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to_email],
                  body=body)
    try:
        with current_app.app_context():
            mail.send(msg)
    except Exception as e:
        print(str(e))
        sys.exit(1)
    return True

def send_application(to_email, subject, userName, candidateName, gigTitle, applicationMessage):
    msg = Message(subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to_email])
    msg.html = flask.render_template('applicationEmail.html', userName=userName, candidateName=candidateName, gigTitle=gigTitle, applicationMessage=applicationMessage)

    try:
        with current_app.app_context():
            mail.send(msg)
    except Exception as e:
        print(str(e))
        sys.exit(1)
    return True


def send_email_welcome(to_email, subject, userName):
    msg = Message(subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to_email])
    msg.html = flask.render_template('welcomeEmail.html', userName=userName)

    try:
        with current_app.app_context():
            mail.send(msg)
    except Exception as e:
        print(str(e))
        sys.exit(1)
    return True
#-----------------------------------------------------------------------

 
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    netid = auth.authenticate()
    status = database.check_and_add_user(netid)
    if status == "user_created":
        username = cas_details(netid)[0]
        email = netid + "@princeton.edu"
        send_email_welcome(email, "Welcome to Gigl!", username)
        
    username = database.get_user(netid).get_name()
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
    netid = auth.authenticate()
    database.check_and_add_user(netid)

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
@app.route('/details/<int:id>', methods=['GET','POST'])
def details(id):
    netid = auth.authenticate()
    database.check_and_add_user(netid)
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

    apply_form = ApplyForm()
    
    if apply_form.validate_on_submit():
        _ = flask.get_flashed_messages() # clears flashed messages
        application_message = apply_form.message.data

        if database.owns_gig(netid, id):
            flask.flash("You can't apply to your own gig...", 'error')
            print("You can't apply to your own gig...")
        elif database.get_application(netid, id):
            flask.flash("You have already applied...", 'error')
            print("You have already applied...")
        elif database.send_application(netid, id, application_message):
            flask.flash("You have successfully applied!", 'success')
            print("You have successfully applied!")
            send_application(gigNetID + "@princeton.edu", "You have a new application!", gigAuthor, database.get_user(netid).get_name(), gigTitle, application_message)
        else:
            flask.flash("Application couldn't be sent due to a database error.", 'error')

        return flask.redirect(flask.url_for('apply_result', gigID=id))
    
    delete_form = DeleteGigForm()
    show_confirm = False
    if delete_form.validate_on_submit():
        url = flask.url_for('details', id=id)
        _ = flask.get_flashed_messages() # clears flashed messages
        if delete_form.delete.data:
            show_confirm = True
        elif delete_form.confirm.data:
            flask.flash("Your Gig has been successfully deleted!", "success")
            return flask.redirect(flask.url_for('gigdeleted', gig_id=id))
        elif delete_form.cancel.data:
            return flask.redirect(url)

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
                                        gigID=id,
                                        apply_form=apply_form,
                                        delete_form=delete_form,
                                        show_confirm=show_confirm)
    response = flask.make_response(html_code)
    return response
#-----------------------------------------------------------------------
@app.route('/apply_result', methods=['GET'])
def apply_result():
    netid = auth.authenticate()
    database.check_and_add_user(netid)
    gigID = flask.request.args.get('gigID')
    html_code = flask.render_template('apply_err.html', gigID=gigID)
    response = flask.make_response(html_code)
    return response
#-----------------------------------------------------------------------
@app.route('/postgig', methods=['GET', 'POST'])
def postgig():
    netid = auth.authenticate()
    database.check_and_add_user(netid)
    user = database.get_user(netid)
    gig_form = PostGigForm()
    if gig_form.validate_on_submit():
        gig_id = database.create_gig(netid, gig_form.title.data, gig_form.categories.data,
                                gig_form.description.data, gig_form.qualifications.data,
                                gig_form.start_date.data, gig_form.end_date.data,
                                datetime.now().date())
        return flask.redirect(flask.url_for('gigposted_success', gigID=gig_id))
    else:
            #TODO: Error handling
            pass
    
    username = user.get_name()
    user_email = f"{netid}@princeton.edu"
    html_code = flask.render_template('postgig.html', username=username,
                                      user_email=user_email,
                                      gig_form=gig_form) 
    response = flask.make_response(html_code)
    return response
#-----------------------------------------------------------------------
@app.route('/profile', methods=['GET'])
def profile():
    netid = auth.authenticate()
    database.check_and_add_user(netid)
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
    database.check_and_add_user(netid)
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
    return flask.redirect(flask.url_for('gigposted_success', gigID=gigID))

@app.route('/gigdeleted/<int:gig_id>', methods=['GET'])
def gigdeleted(gig_id):
    netid = auth.authenticate()
    database.delete_gig_from_db(gig_id)
    html_code = flask.render_template('gigdeleted.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
@app.route('/gigposted_success/<int:gigID>', methods=['GET'])
def gigposted_success(gigID):
    netid = auth.authenticate()
    database.check_and_add_user(netid)
    return flask.render_template('gigposted.html', gigID=gigID)

#-----------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host = 'localhost', debug=True, port=8888)
