#!/usr/bin/env python

# -----------------------------------------------------------------------
# gigl.py
# Authors: TA, AB, IA, YD
# -----------------------------------------------------------------------
import flask
from flask_mail import Mail, Message
from flask import Flask, jsonify, request
import auth
import os
import dotenv
import database
from datetime import datetime
from cas_details import cas_details
from forms import ApplyForm, DeleteGigForm, PostGigForm, SearchForm, ProfileSearchForm, BioEditForm, LinkEditForm, SpecialtySelectForm
from flask import current_app
from flask import render_template, request, make_response
from util import profileIDChecker
from urllib.parse import urlparse


# -----------------------------------------------------------------------
app = Flask(__name__, template_folder='templates/')
dotenv.load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'developmenttemp123')

# -----------------------------------------------------------------------

# Configure Flask-Mail with environment variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'giglprinc3ton@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PW']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Initialize Flask-Mail
mail = Mail(app)

# -----------------------------------------------------------------------


class DatabaseError(Exception):
    """Exception raised for errors related to the database operations."""
    pass


class AuthenticationError(Exception):
    """Exception raised for errors during authentication."""
    pass


class EmailSendingError(Exception):
    """Exception raised for errors during email sending."""
    pass

# Define error handlers


@app.errorhandler(DatabaseError)
def database_error_handler(error):
    app.logger.error(f"Database Error: {error}")
    return render_template('error_database.html'), 500


@app.errorhandler(AuthenticationError)
def authentication_error_handler(error):
    app.logger.error(f"Authentication Error: {error}")
    return render_template('error_auth.html'), 401


@app.errorhandler(404)
def not_found_error_handler(error):
    return render_template('error_404.html'), 404


@app.errorhandler(500)
def internal_error_handler(error):
    app.logger.error(f"Internal Server Error: {error}")
    return render_template('error_500.html'), 500
# -----------------------------------------------------------------------

# This makes 'app' importable from other modules
def get_app():
    return app

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def send_email(to_email, subject, body):
    msg = Message(subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to_email],
                  body=body)
    try:
        with current_app.app_context():
            mail.send(msg)
        return True
    except Exception as e:
        app.logger.error(f"Email Sending Error: {e}")
        raise EmailSendingError(f"Failed to send email to {to_email}")


def send_application(
        to_email,
        subject,
        gigID,
        userName,
        candidateName,
        gigTitle,
        applicationMessage):
    msg = Message(subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to_email])
    msg.html = flask.render_template(
        'applicationEmail.html',
        gigID=gigID,
        userName=userName,
        candidateName=candidateName,
        gigTitle=gigTitle,
        applicationMessage=applicationMessage)

    try:
        with current_app.app_context():
            mail.send(msg)
        return True
    except Exception as e:
        app.logger.error(f"Email Sending Error: {e}")
        flask.abort(500)  # This will trigger the internal_error_handler


def send_email_welcome(to_email, subject, userName):
    msg = Message(subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to_email])
    msg.html = flask.render_template('welcomeEmail.html', userName=userName)

    try:
        with current_app.app_context():
            mail.send(msg)
        return True
    except Exception as e:
        app.logger.error(f"Email Sending Error: {e}")
        flask.abort(500)  # This will trigger the internal_error_handler
# -----------------------------------------------------------------------


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    try:
        html_code = flask.render_template('index.html')
        response = flask.make_response(html_code)
        return response
    except AuthenticationError as e:
        app.logger.error(f"Authentication Error: {e}")
        flask.abort(401)  # This will trigger the authentication_error_handler
    except DatabaseError as e:
        app.logger.error(f"Database Error: {e}")
        flask.abort(500)  # This will trigger the database_error_handler
    except Exception as e:
        app.logger.error(f"Unexpected Error: {e}")
        flask.abort(500)  # This will trigger the internal_error_handler
# -----------------------------------------------------------------------


@app.route('/home', methods=['GET', 'POST'])
def home():
    netid = auth.authenticate()
    try:
        status = database.check_and_add_user(netid)
        if status == "user_created":
            username = cas_details(netid)[0]
            email = netid + "@princeton.edu"
            send_email_welcome(email, "Welcome to Gigl!", username)
        else:
            if database.is_banned(netid):
                html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
                response = flask.make_response(html_code)
                return response
            database.update_activity(netid)

        # Initialize the form with the query parameters from the request
        search_form = SearchForm()
        if search_form.validate_on_submit():
            keyword = search_form.keyword.data
            category = search_form.category.data
            categories = [category] if category else []
            return flask.redirect(
                flask.url_for(
                    'search_results',
                    kw=keyword,
                    cat=category))
        # If form fails to validate (in case something goes wrong with the form
        # submission)
        else:
            keyword = None
            category = None
            categories = []  # This will fetch gigs filtered by the selected category

        username = database.get_user(netid).get_name()
        print(username)
        popular_gigs = database.get_popular_gigs()  # Function to be implemented
        print(popular_gigs)
        featured_gigs = database.get_featured_gigs()  # Adjust to fetch based on user preferences
        new_gigs = database.get_new_gigs()  # Function to be implemented
        html_code = flask.render_template('home.html', usrname=username,
                                      search_form=search_form,
                                      popular_gigs=popular_gigs,
                                      featured_gigs=featured_gigs,
                                      new_gigs=new_gigs)
        response = flask.make_response(html_code)
        return response
    except AuthenticationError as e:
        app.logger.error(f"Authentication Error: {e}")
        flask.abort(401)  # This will trigger the authentication_error_handler
    except DatabaseError as e:
        app.logger.error(f"Database Error: {e}")
        flask.abort(500)  # This will trigger the database_error_handler
    except Exception as e:
        app.logger.error(f"Unexpected Error: {e}")
        flask.abort(500)  # This will trigger the internal_error_handler

# -----------------------------------------------------------------------
@app.route('/searchresults', methods=['GET', 'POST'])
def search_results():
    netid = auth.authenticate()
    try:
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
        database.update_activity(netid)

        # Initialize the form with the query parameters from the request
        search_form = SearchForm()

        if search_form.validate_on_submit():
            keyword = search_form.keyword.data
            category = search_form.category.data
            return flask.redirect(
                flask.url_for(
                    'search_results',
                    cat=category,
                    kw=keyword))
        
        # Retrieve the current page number and set items per page
        page = request.args.get('page', 1, type=int)
        per_page = 6

        category = flask.request.args.get('cat')
        keyword = flask.request.args.get('kw')
        search_form.category.data = category

        gigs = database.get_gigs(keyword=keyword, categories=[
                                 category] if category else [], page=page, per_page=per_page)
        
        # Calculate total pages for pagination
        total_gigs = len(database.get_gigs(keyword=keyword, categories=[category] if category else []))
        total_pages = (total_gigs + per_page - 1) // per_page
        
        for gig in gigs:
            gig.is_bookmarked = database.is_bookmarked(netid, gig.get_gigID())
        # Check if gigs is not an empty list
        if not gigs:
            gigs = []  # Ensure gigs is always a list

        # Render the template with the search results and the form
        html_code = render_template(
            'searchresults.html',
            search_form=search_form,
            mygigs=gigs,
            cat=category,
            kw=keyword,
            total_pages = total_pages,
            current_page = page,
            author = database.get_user,
            profileIDChecker = profileIDChecker,
            is_bookmarked = database.is_bookmarked,
            netid = netid,
            is_banned=database.is_banned)

        response = make_response(html_code)

        return response
    except AuthenticationError as e:
        app.logger.error(f"Authentication Error: {e}")
        flask.abort(401)  # This will trigger the authentication_error_handler
    except DatabaseError as e:
        app.logger.error(f"Database Error: {e}")
        flask.abort(500)  # This will trigger the database_error_handler
    except Exception as e:
        app.logger.error(f"Unexpected Error: {e}")
        flask.abort(500)  # This will trigger the internal_error_handler
# -----------------------------------------------------------------------


@app.route('/details/<int:id>', methods=['GET', 'POST'])
def details(id):
    netid = auth.authenticate()
    try:
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
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

        owns = database.owns_gig(netid, id)  # boolean
        isAdmin = (netid == 'cos-gigl')
        if owns:
            all_apps = database.get_apps_for(id)
            application = None
        else:
            all_apps = None
            application = database.get_application(netid, id)

        apply_form = ApplyForm()

        if apply_form.validate_on_submit():
            application_message = apply_form.message.data

            if database.owns_gig(netid, id):
                flask.flash("You can't apply to your own gig...", 'error')
            elif database.get_application(netid, id):
                flask.flash("You have already applied...", 'error')
            elif database.send_application(netid, id, application_message):
                flask.flash("You have successfully applied!", 'success')
                send_application(
                    gigNetID +
                    "@princeton.edu",
                    "You have a new application!",
                    id,
                    gigAuthor,
                    database.get_user(netid).get_name(),
                    gigTitle,
                    application_message)
            else:
                flask.flash(
                    "Application couldn't be sent due to a database error.",
                    'error')

            return flask.redirect(flask.url_for('apply_result', gigID=id))
    except AuthenticationError as e:
        app.logger.error(f"Authentication Error: {e}")
        flask.abort(401)  # This will trigger the authentication_error_handler
    except DatabaseError as e:
        app.logger.error(f"Database Error: {e}")
        flask.abort(500)  # This will trigger the database_error_handler
    except Exception as e:
        app.logger.error(f"Unexpected Error: {e}")
        flask.abort(500)  # This will trigger the internal_error_handler

    delete_form = DeleteGigForm()
    show_confirm = False
    if delete_form.validate_on_submit():
        _ = flask.get_flashed_messages()  # clears flashed messages
        # url = flask.url_for('details', id=id)
        if delete_form.delete.data:
            show_confirm = True
        elif delete_form.confirm.data:
            if owns or isAdmin:
                database.delete_gig_from_db(id)
                flask.flash("Your Gig has been successfully deleted!", "success")
                return flask.redirect(flask.url_for('gigdeleted'))
            else:
                flask.flash("You are not authorized to delete this gig.", "error")
                return flask.redirect(flask.url_for('gigdeleted'))
        # elif delete_form.cancel.data:
        #     return flask.redirect(url)

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
                                      show_confirm=show_confirm,
                                      isAdmin=isAdmin,
                                      get_usr = database.get_user)
    response = flask.make_response(html_code)
    return response
# -----------------------------------------------------------------------


@app.route('/apply_result', methods=['GET'])
def apply_result():
    netid = auth.authenticate()
    try:
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
        database.update_activity(netid)

        gigID = flask.request.args.get('gigID')
        html_code = flask.render_template('apply_err.html', gigID=gigID)
        response = flask.make_response(html_code)
        return response
    except AuthenticationError as e:
        app.logger.error(f"Authentication Error: {e}")
        flask.abort(401)  # This will trigger the authentication_error_handler
    except DatabaseError as e:
        app.logger.error(f"Database Error: {e}")
        flask.abort(500)  # This will trigger the database_error_handler
    except Exception as e:
        app.logger.error(f"Unexpected Error: {e}")
        flask.abort(500)  # This will trigger the internal_error_handler

# -----------------------------------------------------------------------
@app.route('/postgig', methods=['GET', 'POST'])
def postgig():
    netid = auth.authenticate()
    try:
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
        database.update_activity(netid)

        user = database.get_user(netid)
        gig_form = PostGigForm()
        if gig_form.validate_on_submit():
            gig_id = database.create_gig(
                netid,
                gig_form.title.data,
                gig_form.categories.data,
                gig_form.description.data,
                gig_form.qualifications.data,
                gig_form.start_date.data,
                gig_form.end_date.data,
                datetime.now().date())
            return flask.redirect(
                flask.url_for(
                    'gigposted_success',
                    gigID=gig_id))
        else:
            print(gig_form.start_date.errors)
            print(gig_form.end_date.errors)
            # TODO: Error handling
            pass

        username = user.get_name()
        user_email = f"{netid}@princeton.edu"
        html_code = flask.render_template('postgig.html', username=username,
                                          user_email=user_email,
                                          gig_form=gig_form)
        response = flask.make_response(html_code)
        return response
    except AuthenticationError as e:
        app.logger.error(f"Authentication Error: {e}")
        flask.abort(401)  # This will trigger the authentication_error_handler
    except DatabaseError as e:
        app.logger.error(f"Database Error: {e}")
        flask.abort(500)  # This will trigger the database_error_handler
    except Exception as e:
        app.logger.error(f"Unexpected Error: {e}")
        flask.abort(500)  # This will trigger the internal_error_handler
# -----------------------------------------------------------------------


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    netid = auth.authenticate()
    database.check_and_add_user(netid)
    if database.is_banned(netid):
        html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
        response = flask.make_response(html_code)
        return response
    database.update_activity(netid)

    user = database.get_user(netid)
    bio = user.get_bio()
    links = user.get_links()
    spec = user.get_specialty()
    username = user.get_name()
    user_email = f"{netid}@princeton.edu"

    bioeditform = BioEditForm()
    bioeditform.bio.data=bio
    linkeditform = LinkEditForm()
    specialtyform = SpecialtySelectForm()
    specialtyform.specialty.data = spec

    if request.method == 'POST':
        if 'toggle_visibility' in request.form:
            # Call the function to toggle visibility
            database.set_visibility(netid, not user.is_visible())

            return flask.redirect(flask.url_for('profile'))

    mygigs = database.get_gigs_posted_by(netid)
    myapps = database.get_apps_by(netid)

    html_code = flask.render_template(
        'profile.html',
        username=username,
        user_email=user_email,
        mygigs=mygigs,
        mybookmarks=database.get_bookmarks(netid),
        myapps=myapps,
        user=user,
        specialty=spec,
        is_visible=user.is_visible(),
        bio=bio,
        links=links,
        bioeditform=bioeditform,
        linkeditform=linkeditform,
        specialtyform=specialtyform)  # Pass the visibility status to the template
    response = flask.make_response(html_code)
    return response
# -----------------------------------------------------------------------


@app.route('/profilesearch', methods=['GET', 'POST'])
def profilesearch():
    netid = auth.authenticate()
    isAdmin = (netid == 'cos-gigl')
    try:
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
        database.update_activity(netid)

        # Initialize the form with the query parameters from the request
        psearch_form = ProfileSearchForm()

        if psearch_form.validate_on_submit():
            keyword = psearch_form.keyword.data
            specialty = psearch_form.specialty.data
            return flask.redirect(
                flask.url_for(
                    'profilesearch',
                    spec=specialty,
                    kw=keyword))
        # If form fails to validate (in case something goes wrong with the form
        # submission)
        else:
            specialty = flask.request.args.get('spec')
            keyword = flask.request.args.get('kw')
            psearch_form.specialty.data = specialty

        if isAdmin:
            freelancers = database.get_all_users(
                keyword=keyword, specialty=specialty)
        else:
            freelancers = database.get_freelancers(
                keyword=keyword, specialty=specialty)

        # Render the template with the search results and the form
        html_code = render_template(
            'profilesearch.html',
            psearch_form=psearch_form,
            freelancers=freelancers,
            spec=specialty,
            kw=keyword,
            isAdmin=isAdmin)

        response = make_response(html_code)

        return response
    except AuthenticationError as e:
        app.logger.error(f"Authentication Error: {e}")
        flask.abort(401)  # This will trigger the authentication_error_handler
    except DatabaseError as e:
        app.logger.error(f"Database Error: {e}")
        flask.abort(500)  # This will trigger the database_error_handler
    except Exception as e:
        app.logger.error(f"Unexpected Error: {e}")
        flask.abort(500)  # This will trigger the internal_error_handler

# -----------------------------------------------------------------------


@app.route('/gigdeleted', methods=['GET'])
def gigdeleted():
    netid = auth.authenticate()
    try:
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
        database.update_activity(netid)

        html_code = flask.render_template('gigdeleted.html')
        response = flask.make_response(html_code)
        return response
    except AuthenticationError as e:
        app.logger.error(f"Authentication Error: {e}")
        flask.abort(401)  # This will trigger the authentication_error_handler
    except DatabaseError as e:
        app.logger.error(f"Database Error: {e}")
        flask.abort(500)  # This will trigger the database_error_handler
    except Exception as e:
        app.logger.error(f"Unexpected Error: {e}")
        flask.abort(500)  # This will trigger the internal_error_handler

# -----------------------------------------------------------------------


@app.route('/gigposted_success/<int:gigID>', methods=['GET'])
def gigposted_success(gigID):
    netid = auth.authenticate()
    try:
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
        database.update_activity(netid)

        return flask.render_template('gigposted.html', gigID=gigID)
    except AuthenticationError as e:
        app.logger.error(f"Authentication Error: {e}")
        flask.abort(401)  # This will trigger the authentication_error_handler
    except DatabaseError as e:
        app.logger.error(f"Database Error: {e}")
        flask.abort(500)  # This will trigger the database_error_handler
    except Exception as e:
        app.logger.error(f"Unexpected Error: {e}")
        flask.abort(500)  # This will trigger the internal_error_handler

# -----------------------------------------------------------------------


@app.route('/logout', methods=['GET'])
def logout():
    # Log out of the CAS session, and then the application.
    return auth.logoutcas()
# -----------------------------------------------------------------------


@app.route('/freelancer/<netid>', methods=['GET', 'POST'])
def freelancer_profile(netid):
    id = auth.authenticate()
    isAdmin = (id == 'cos-gigl')
    try:
        # Fetch freelancer details from the database using netid
        database.check_and_add_user(id)
        if database.is_banned(id):
            html_code = flask.render_template('banneduser.html', name=database.get_user(id).get_name())
            response = flask.make_response(html_code)
            return response
        database.update_activity(id)

        if request.method == 'POST':
            if 'toggle_ban' in request.form:
                # Call the function to toggle visibility
                if database.is_banned(netid):
                    database.unban_user(netid)
                else:
                    database.ban_user(netid)

                return flask.redirect(flask.url_for('freelancer_profile', netid=netid))

        freelancer = database.get_user(netid)
        if freelancer and (freelancer.is_visible() or isAdmin):
            return render_template('freelancer.html', freelancer=freelancer, isAdmin = isAdmin)
        else:
            # Handle the case where the freelancer does not exist or is not
            # visible
            return render_template('error_404.html'), 404
    except AuthenticationError as e:
        app.logger.error(f"Authentication Error: {e}")
        flask.abort(401)  # This will trigger the authentication_error_handler
    except DatabaseError as e:
        app.logger.error(f"Database Error: {e}")
        flask.abort(500)  # This will trigger the database_error_handler
    except Exception as e:
        app.logger.error(f"Unexpected Error: {e}")
        flask.abort(500)  # This will trigger the internal_error_handler

# ----------------------------------------------------------------------
@app.route('/changespecialty', methods=['POST'])
def changespecialty():
    netid = auth.authenticate()
    if database.is_banned(netid):
        html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
        response = flask.make_response(html_code)
        return response
    specialtyform = SpecialtySelectForm(flask.request.form)
    if specialtyform.validate_on_submit():
        newspec = specialtyform.specialty.data
        database.update_specialty(netid, newspec)
        html_code = flask.render_template(
            'newspecialty.html', specialty=newspec)
        response = flask.make_response(html_code)
        return response
    else:
        spec = database.get_user(netid).get_specialty()
        html_code = flask.render_template(
            'newspecialty.html', specialty=spec)
        response = flask.make_response(html_code)
        return response
#-----------------------------------------------------------------------
@app.route('/editbio', methods=['POST'])
def editbio():
    netid = auth.authenticate()
    if database.is_banned(netid):
        html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
        response = flask.make_response(html_code)
        return response
    bioeditform = BioEditForm(flask.request.form)
    if bioeditform.validate_on_submit():
        newbio = bioeditform.bio.data
        database.update_bio(netid, newbio)
        html_code = flask.render_template(
            'bio_in_profile.html', bio=newbio, bioeditform=bioeditform)
        response = flask.make_response(html_code)
        return response
    else:
        bioeditform = BioEditForm()
        bio = database.get_user(netid).get_bio()
        bioeditform.bio.data=bio
        html_code = flask.render_template(
            'bio_in_profile_error.html',
            bio=bio,
            bioeditform=bioeditform)
        response = flask.make_response(html_code)
        return response
# ----------------------------------------------------------------------
@app.route('/editlinks', methods=['POST'])
def editlinks():
    netid = auth.authenticate()
    if database.is_banned(netid):
        html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
        response = flask.make_response(html_code)
        return response
    linkeditform = LinkEditForm(flask.request.form)
    if linkeditform.validate_on_submit():
        link1 = linkeditform.link1.data
        link2 = linkeditform.link2.data
        link3 = linkeditform.link3.data
        link4 = linkeditform.link4.data
        links = [link1, link2, link3, link4]
        links = list(filter(lambda x: x != '', links))
        
        database.update_links(netid, links)
        links = database.get_user(netid).get_links()
        linkeditform = LinkEditForm()
        html_code = flask.render_template(
            'links_in_profile.html',
            links=links,
            linkeditform=linkeditform)
        response = flask.make_response(html_code)
        return response
    else:
        linkeditform = LinkEditForm()
        links = database.get_user(netid).get_links()
        html_code = flask.render_template(
            'links_in_profile_error.html',
            links=links,
            linkeditform=linkeditform)
        response = flask.make_response(html_code)
        return response


@app.route('/add_bookmark/<int:gig_id>', methods=['POST'])
def add_bookmark_route(gig_id):
    netid = auth.authenticate()
    if database.is_banned(netid):
        html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
        response = flask.make_response(html_code)
        return response
    result = database.add_bookmark(netid, gig_id)
    if result == True:
        return flask.jsonify({'status': 'success', 'action': 'added'})
    elif result == "already_exists":
        return flask.jsonify({'status': 'success', 'action': 'exists'})
    else:
        return flask.jsonify({'status': 'error'})

@app.route('/remove_bookmark/<int:gig_id>', methods=['POST'])
def remove_bookmark(gig_id):
    netid = auth.authenticate()
    if database.is_banned(netid):
        html_code = flask.render_template('banneduser.html', name=database.get_user(netid).get_name())
        response = flask.make_response(html_code)
        return response
    try:
        result = database.remove_bookmark(netid, gig_id)
        if result == "already_exists":
            return flask.jsonify({'status': 'success', 'action': 'removed'})
        if result == True:
            return flask.jsonify({'status': 'success', 'action': 'removed'})
        else:
            return flask.jsonify({'status': 'error'})
    except Exception as e:
        return flask.jsonify({'status': 'error'})

# -----------------------------------------------------------------------

def pagination_pages(current_page, total_pages, window=3):
    # Ensure window size is reasonable
    window = max(2, window)
    pages = [1, total_pages]
    # Add the current page and the 'window' pages on either side of it
    pages.extend([
        current_page,
        *range(max(1, current_page - window), min(total_pages + 1, current_page + window + 1))
    ])
    # Ensure the start and end ranges are within bounds
    pages.extend([
        *range(2, min(window + 2, total_pages)),
        *range(max(1, total_pages - window), total_pages)
    ])
    # Remove duplicates and sort
    pages = sorted(set(pages))

    # Insert ellipses where there are gaps
    final_pages = []
    for i, page in enumerate(pages):
        if i > 0 and page - pages[i - 1] > 1:
            final_pages.append('...')
        final_pages.append(page)
    return final_pages
# -----------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8000)