#!/usr/bin/env python

#-----------------------------------------------------------------------
# gigl.py
# Authors: TA, AB, IA, YD
#-----------------------------------------------------------------------

import flask
from flask_mail import Mail, Message
from flask import Flask
import auth
import os
import dotenv
import database
from datetime import datetime
from cas_details import cas_details
from forms import ApplyForm, DeleteGigForm, PostGigForm, SearchForm, ProfileSearchForm, BioEditForm, LinkEditForm
from flask import current_app
import sys
from flask import render_template, request, make_response



#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates/')
dotenv.load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'developmenttemp123')
# csrf = CSRFProtect(app)

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

def send_application(to_email, subject, gigID, userName, candidateName, gigTitle, applicationMessage):
    msg = Message(subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to_email])
    msg.html = flask.render_template('applicationEmail.html', gigID=gigID, userName=userName, candidateName=candidateName, gigTitle=gigTitle, applicationMessage=applicationMessage)

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
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response
#-----------------------------------------------------------------------
@app.route('/home', methods=['GET', 'POST'])
def home():
    netid = auth.authenticate()
    status = database.check_and_add_user(netid)
    if status == "user_created":
        username = cas_details(netid)[0]
        email = netid + "@princeton.edu"
        send_email_welcome(email, "Welcome to Gigl!", username)
    else:
        database.update_activity(netid)
    # Initialize the form with the query parameters from the request
    search_form = SearchForm()
    if search_form.validate_on_submit():
        keyword = search_form.keyword.data
        category = search_form.category.data
        categories = [category] if category else [] 
        return flask.redirect(flask.url_for('search_results', kw=keyword, cat=category))
    else: # If form fails to validate (in case something goes wrong with the form submission)
        keyword = None
        category = None
        categories = []  # This will fetch gigs filtered by the selected category

    username = database.get_user(netid).get_name()
    html_code = flask.render_template('home.html', usrname=username,
                                      search_form=search_form)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
@app.route('/searchresults', methods=['GET', 'POST'])
def search_results():
    netid = auth.authenticate()
    database.check_and_add_user(netid)
    database.update_activity(netid)

    # Initialize the form with the query parameters from the request
    search_form = SearchForm()

    if search_form.validate_on_submit():
        keyword = search_form.keyword.data
        category = search_form.category.data
        categories = [category] if category else [] 
        return flask.redirect(flask.url_for('search_results',cat=category, kw=keyword ))
    else: # If form fails to validate (in case something goes wrong with the form submission)
        category = flask.request.args.get('cat')
        keyword = flask.request.args.get('kw')
        search_form.category.data = category

    # Fetch list of gigs based on the keyword / category
    categories = category
    if not categories:
        categories = []
    else:
        categories = [categories]
    
    gigs = database.get_gigs(keyword=keyword, categories=categories)    

    # Check if gigs is not an empty list
    if gigs == 0:
        gigs = []  # Ensure gigs is always a list
        print("No gigs found, setting gigs to an empty list.")

    # Render the template with the search results and the form
    html_code = render_template('searchresults.html', search_form=search_form, mygigs=gigs, cat=category, kw=keyword)

    response = make_response(html_code)

    return response

#-----------------------------------------------------------------------
@app.route('/details/<int:id>', methods=['GET','POST'])
def details(id):
    netid = auth.authenticate()
    database.check_and_add_user(netid)
    database.update_activity(netid)

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
        elif database.get_application(netid, id):
            flask.flash("You have already applied...", 'error')
        elif database.send_application(netid, id, application_message):
            flask.flash("You have successfully applied!", 'success')
            send_application(gigNetID + "@princeton.edu", "You have a new application!", id, gigAuthor, database.get_user(netid).get_name(), gigTitle, application_message)
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
    database.update_activity(netid)

    gigID = flask.request.args.get('gigID')
    html_code = flask.render_template('apply_err.html', gigID=gigID)
    response = flask.make_response(html_code)
    return response
#-----------------------------------------------------------------------
@app.route('/postgig', methods=['GET', 'POST'])
def postgig():
    netid = auth.authenticate()
    database.check_and_add_user(netid)
    database.update_activity(netid)

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
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    netid = auth.authenticate()
    database.check_and_add_user(netid)
    database.update_activity(netid)

    user = database.get_user(netid)
    username = user.get_name()
    user_email = f"{netid}@princeton.edu"
    links = user.get_links()
    bio = user.get_bio()

    bioeditform = BioEditForm()
    linkeditform = LinkEditForm()

    if request.method == 'POST':
        if 'toggle_visibility' in request.form:
            # Call the function to toggle visibility
            database.set_visibility(netid, not user.is_visible())
            # Redirect to the profile page with a GET request to prevent double-submit
            return flask.redirect(flask.url_for('profile'))

    mygigs = database.get_gigs_posted_by(netid)
    myapps = database.get_apps_by(netid)

    html_code = flask.render_template('profile.html', username=username,
                                      user_email=user_email,
                                      mygigs=mygigs,
                                      myapps=myapps,
                                      is_visible=user.is_visible(),
                                      links=links,
                                      bio=bio,
                                      bioeditform=bioeditform,
                                      linkeditform = linkeditform)  # Pass the visibility status to the template
    response = flask.make_response(html_code)     
    return response
#-----------------------------------------------------------------------
@app.route('/profilesearch', methods=['GET', 'POST'])
def profilesearch():
    netid = auth.authenticate()
    database.check_and_add_user(netid)
    database.update_activity(netid)

    # Initialize the form with the query parameters from the request
    psearch_form = ProfileSearchForm()

    if psearch_form.validate_on_submit():
        keyword = psearch_form.keyword.data
        specialty = psearch_form.specialty.data
        return flask.redirect(flask.url_for('profilesearch',spec=specialty, kw=keyword ))
    else: # If form fails to validate (in case something goes wrong with the form submission)
        specialty = flask.request.args.get('spec')
        keyword = flask.request.args.get('kw')
        psearch_form.specialty.data = specialty
    
    freelancers = database.get_freelancers(keyword=keyword, specialty=specialty)

    # Render the template with the search results and the form
    html_code = render_template('profilesearch.html', psearch_form=psearch_form, freelancers=freelancers, spec=specialty, kw=keyword)

    response = make_response(html_code)

    return response

#-----------------------------------------------------------------------
@app.route('/gigdeleted/<int:gig_id>', methods=['GET'])
def gigdeleted(gig_id):
    netid = auth.authenticate()
    database.check_and_add_user(netid)
    database.update_activity(netid)

    database.delete_gig_from_db(gig_id)
    html_code = flask.render_template('gigdeleted.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
@app.route('/gigposted_success/<int:gigID>', methods=['GET'])
def gigposted_success(gigID):
    netid = auth.authenticate()
    database.check_and_add_user(netid)
    database.update_activity(netid)

    return flask.render_template('gigposted.html', gigID=gigID)

#-----------------------------------------------------------------------
@app.route('/logout', methods=['GET'])
def logout():
    flask.session.clear()
    html_code = flask.render_template('index.html')
    response = flask.redirect(flask.url_for('index'))
    return response
#-----------------------------------------------------------------------
@app.route('/freelancer/<netid>')
def freelancer_profile(netid):
    # Fetch freelancer details from the database using netid
    id = auth.authenticate()
    database.update_activity(id)

    freelancer = database.get_user(netid)
    if freelancer and freelancer.is_visible():
        return render_template('freelancer.html', freelancer=freelancer)
    else:
        # Handle the case where the freelancer does not exist or is not visible
        return "You cannot access this page", 404

#-----------------------------------------------------------------------
@app.route('/editbio', methods=['POST'])
def editbio():
    netid = auth.authenticate()
    bioeditform = BioEditForm(flask.request.form)
    if bioeditform.validate_on_submit():
        newbio = bioeditform.bio.data
        database.update_bio(netid, newbio) 
        html_code = flask.render_template('bio_in_profile.html', bio=newbio, bioeditform=bioeditform)
        response = flask.make_response(html_code)
        return response
    else:
        bioeditform = BioEditForm()
        bio = database.get_user(netid).get_bio()
        html_code = flask.render_template('bio_in_profile_error.html', bio=bio, bioeditform=bioeditform)
        response = flask.make_response(html_code)
        return response
#----------------------------------------------------------------------
@app.route('/editlinks', methods=['POST'])
def editlinks():
    netid = auth.authenticate()
    linkeditform = LinkEditForm(flask.request.form)
    if linkeditform.validate_on_submit():
        link1 = linkeditform.link1.data
        link2 = linkeditform.link2.data
        link3 = linkeditform.link3.data
        link4 = linkeditform.link4.data
        links = [link1, link2, link3, link4]
        links = filter(lambda x : x != '', links)
        database.update_links(netid, links)
        links = database.get_user(netid).get_links()
        html_code = flask.render_template('links_in_profile.html', links=links, linkeditform=linkeditform)
        response = flask.make_response(html_code)
        return response
    else:
        linkeditform = LinkEditForm()
        links = database.get_user(netid).get_links()
        html_code = flask.render_template('links_in_profile_error.html', links=links, linkeditform=linkeditform)
        response = flask.make_response(html_code)
        return response

    
#-----------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host = 'localhost', debug=True, port=8888)
