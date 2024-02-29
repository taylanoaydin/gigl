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
from forms import ApplyForm, DeleteGigForm, PostGigForm, EditGigForm, SearchForm, ProfileSearchForm, BioEditForm, LinkEditForm, SpecialtySelectForm, SetStatusForm
from flask import current_app
from flask import render_template, request, make_response
from util import profileIDChecker
from urllib.parse import urlparse
from exc import DatabaseError, ServerError, AuthenticationError, EmailSendingError


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

all_admins = ['cos-gigl', 'jl9926',  'motoaki', 'sk3686']


# -----------------------------------------------------------------------
# Define error handlers
@app.errorhandler(AuthenticationError)
@app.errorhandler(401)
def authentication_error_handler(error):
    return render_template('error_auth.html'), 401


@app.errorhandler(404)
def not_found_error_handler(error):
    return render_template('error_404.html'), 404


@app.errorhandler(500)
@app.errorhandler(DatabaseError)
@app.errorhandler(ServerError)
def internal_error_handler(error):
    app.logger.error(f"Internal Server Error: {error}")
    return render_template('error_500.html'), 500
# -----------------------------------------------------------------------


# This makes 'app' importable from other modules
def get_app():
    return app


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
        return True


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
        return True


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
        return True
# -----------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    try:
        html_code = flask.render_template('index.html')
        response = flask.make_response(html_code)
        return response
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
            username = database.get_user(netid).get_name()
            email = netid + "@princeton.edu"
            send_email_welcome(email, "Welcome to Gigl!", username)
        else:
            if database.is_banned(netid):
                html_code = flask.render_template(
                    'banneduser.html', name=database.get_user(netid).get_name())
                response = flask.make_response(html_code)
                return response
            database.update_activity(netid)
    except Exception as e:
        raise DatabaseError

    try:
        # Initialize the form with the query parameters from the request
        search_form = SearchForm()
        if search_form.validate_on_submit():
            keyword = search_form.keyword.data
            category = search_form.category.data
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
    except Exception as e:
        raise ServerError

    try:
        username = database.get_user(netid).get_name()
        popular_gigs = database.get_popular_gigs()  # Function to be implemented
        # Adjust to fetch based on user preferences
        featured_gigs = database.get_featured_gigs()
        new_gigs = database.get_new_gigs()  # Function to be implemented
    except Exception as e:
        raise DatabaseError
    
    try:
        html_code = flask.render_template('home.html', usrname=username,
                                            search_form=search_form,
                                            popular_gigs=popular_gigs,
                                            featured_gigs=featured_gigs,
                                            author=database.get_user,
                                            profileIDChecker=profileIDChecker,
                                            is_bookmarked=database.is_bookmarked,
                                            netid=netid,
                                            new_gigs=new_gigs,
                                            active_page='home')
        response = flask.make_response(html_code)
        return response
    except DatabaseError as e:
        raise e
    except Exception as e:
        raise ServerError


# -----------------------------------------------------------------------


@app.route('/searchresults', methods=['GET', 'POST'])
def search_results():
    netid = auth.authenticate()
    try: 
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template(
                'banneduser.html', name=database.get_user(netid).get_name())
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

        category = flask.request.args.get('cat')
        keyword = flask.request.args.get('kw')
        search_form.category.data = category

        gigs = database.get_gigs(keyword=keyword, categories=[
                                    category] if category else [])

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
            author=database.get_user,
            profileIDChecker=profileIDChecker,
            is_bookmarked=database.is_bookmarked,
            netid=netid,
            is_banned=database.is_banned,
            active_page='searchresults')

        response = make_response(html_code)
        return response

    except DatabaseError as e:
        raise e
    except Exception as e:
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

       try:
            gig = database.get_gig_details(id)
            gigTitle = gig.get_title()
            gigNetID = gig.get_netid()
       except:
           flask.abort(404)

       if database.is_banned(gigNetID):
           flask.abort(404)
       gigAuthor = database.get_user(gigNetID).get_name()
       gigCategory = gig.get_category()
       gigDescription = gig.get_description()
       gigQualifications = gig.get_qualifications()
       gigStartDate = gig.get_stylized_fromdate()
       gigEndDate = gig.get_stylized_til_date()
       gigPostedDate = gig.get_stylized_post_date()
       gigHprice = gig.get_hprice()


       owns = database.owns_gig(netid, id)  # boolean
       isAdmin = (netid in all_admins)
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
   except DatabaseError as e:
       raise e
   except Exception as e:
       flask.abort(500)  # This will trigger the internal_error_handler
   
   try:
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
   except DatabaseError as e:
       raise e
   except Exception as e:
       flask.abort(500) 
   
   try:
        setstatusforms = {}
        if owns:
            for app in all_apps:
                setstatusform = SetStatusForm()
                setstatusform.status.data = app.get_status()
                setstatusform.gigID.data = app.get_gigID()
                setstatusform.applicantID.data = app.get_applicant_netid()
                setstatusforms[app.get_applicant_netid()] = setstatusform
        gig_form = EditGigForm()
        gig_form.qualifications.data = gigQualifications
        gig_form.title.data = gigTitle
        gig_form.description.data = gigDescription
        gig_form.categories.data = gigCategory
        gig_form.price.data = gigHprice


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
                                            get_usr = database.get_user,
                                            setstatusforms=setstatusforms,
                                            gig_form=gig_form,
                                            profileIDChecker=profileIDChecker,
                                            gigHprice = gigHprice)
        response = flask.make_response(html_code)
        return response
   except DatabaseError as e:
       raise e
   except Exception as e:
       flask.abort(500)
# -----------------------------------------------------------------------


@app.route('/apply_result', methods=['GET'])
def apply_result():
    netid = auth.authenticate()
    try:
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template(
                'banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
        database.update_activity(netid)

        gigID = flask.request.args.get('gigID')
        html_code = flask.render_template('apply_err.html', gigID=gigID)
        response = flask.make_response(html_code)
        return response
    except DatabaseError as e:
        raise e
    except Exception as e:
        flask.abort(500)  # This will trigger the internal_error_handler


# -----------------------------------------------------------------------
@app.route('/postgig', methods=['GET', 'POST'])
def postgig():
    netid = auth.authenticate()
    try:
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template(
                'banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
        database.update_activity(netid)

        user = database.get_user(netid)
        gig_form = PostGigForm()
        if gig_form.validate_on_submit():
            print("wow")
            gig_id = database.create_gig(
                netid,
                gig_form.title.data,
                gig_form.categories.data,
                gig_form.description.data,
                gig_form.qualifications.data,
                gig_form.start_date.data,
                gig_form.end_date.data,
                datetime.now().date(),
                gig_form.price.data)
            return flask.redirect(
                flask.url_for(
                    'gigposted_success',
                    gigID=gig_id))
        else:
            pass

        username = user.get_name()
        user_email = f"{netid}@princeton.edu"
        html_code = flask.render_template('postgig.html', username=username,
                                          user_email=user_email,
                                          gig_form=gig_form,
                                          active_page='postgig')
        response = flask.make_response(html_code)
        return response
    except DatabaseError as e:
        raise e
    except Exception as e:
        flask.abort(500)  # This will trigger the internal_error_handler
# -----------------------------------------------------------------------
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    netid = auth.authenticate()
    try:
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template(
                'banneduser.html', name=database.get_user(netid).get_name())
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
        bioeditform.bio.data = bio
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
            specialtyform=specialtyform,
            get_this_gig=database.get_gig_details,
            active_page='profile')  # Pass the visibility status to the template
        response = flask.make_response(html_code)
        return response
    except DatabaseError as e:
        raise e
    except Exception as e:
        raise ServerError
# -----------------------------------------------------------------------


@app.route('/profilesearch', methods=['GET', 'POST'])
def profilesearch():
    netid = auth.authenticate()
    try:
        isAdmin = (netid in all_admins)
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template(
                'banneduser.html', name=database.get_user(netid).get_name())
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

        # Retrieve the current page number and set items per page
        page = request.args.get('page', 1, type=int)
        per_page = 5  # Define the number of items per page

        specialty = request.args.get('spec', '')
        keyword = request.args.get('kw', '')
        psearch_form.specialty.data = specialty

        if isAdmin:
            freelancers, total_freelancers = database.get_all_users(
                keyword=keyword, specialty=specialty, page=page, per_page=per_page)
        else:
            freelancers, total_freelancers = database.get_freelancers(
                keyword=keyword, specialty=specialty, page=page, per_page=per_page)

        total_pages = (total_freelancers + per_page - 1) // per_page

        # Render the template with the search results and the form
        html_code = render_template(
            'profilesearch.html',
            psearch_form=psearch_form,
            freelancers=freelancers,
            spec=specialty,
            total_pages=total_pages,
            current_page=page,
            kw=keyword,
            isAdmin=isAdmin,
            active_page='profilesearch')

        response = make_response(html_code)

        return response
    except DatabaseError as e:
        raise e
    except Exception as e:
        raise ServerError


# -----------------------------------------------------------------------


@app.route('/gigdeleted/<int:id>', methods=['POST'])
def gigdeleted(id):
    netid = auth.authenticate()
    try:
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template(
                'banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
        database.update_activity(netid)
        owns = database.owns_gig(netid, id)
        isAdmin = (netid in all_admins)
        delete_form = DeleteGigForm(request.form)
        if delete_form.validate_on_submit():
            print('delete submitted')
            if owns or isAdmin:
                database.delete_gig_from_db(id)
                flask.flash("Your Gig has been successfully deleted!", "success")
            else:
                flask.flash("You are not authorized to delete this gig.", "error")

        html_code = flask.render_template('gigdeleted.html')
        response = flask.make_response(html_code)
        return response
    except DatabaseError as e:
        raise e
    except Exception as e:
        raise ServerError


# -----------------------------------------------------------------------
@app.route('/gigposted_success/<int:gigID>', methods=['GET'])
def gigposted_success(gigID):
    netid = auth.authenticate()
    try:
        database.check_and_add_user(netid)
        if database.is_banned(netid):
            html_code = flask.render_template(
                'banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
        database.update_activity(netid)

        return flask.render_template('gigposted.html', gigID=gigID)
    except DatabaseError as e:
        raise e
    except Exception as e:
        raise ServerError


# -----------------------------------------------------------------------
@app.route('/logout', methods=['GET'])
def logout():
    # Log out of the CAS session, and then the application.
    return auth.logoutcas()
# -----------------------------------------------------------------------

@app.route('/freelancer/<netid>', methods=['GET', 'POST'])
def freelancer_profile(netid):
    id = auth.authenticate()
    try:
        isAdmin = (id in all_admins)
        # Fetch freelancer details from the database using netid
        database.check_and_add_user(id)
        if database.is_banned(id):
            html_code = flask.render_template(
                'banneduser.html', name=database.get_user(id).get_name())
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
        if freelancer and ((freelancer.is_visible() and not freelancer.is_banned()) or isAdmin):
            return render_template('freelancer.html', freelancer=freelancer, isAdmin=isAdmin)
        else:
            # Handle the case where the freelancer does not exist or is not
            # visible
            return render_template('error_404.html'), 404

    except DatabaseError as e:
        raise e
    except Exception as e:
        raise ServerError


# ----------------------------------------------------------------------
@app.route('/changespecialty', methods=['POST'])
def changespecialty():
    netid = auth.authenticate()
    if database.is_banned(netid):
        html_code = flask.render_template(
            'banneduser.html', name=database.get_user(netid).get_name())
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
# -----------------------------------------------------------------------


@app.route('/editbio', methods=['POST'])
def editbio():
    netid = auth.authenticate()
    if database.is_banned(netid):
        html_code = flask.render_template(
            'banneduser.html', name=database.get_user(netid).get_name())
        response = flask.make_response(html_code)
        return response
    bioeditform = BioEditForm(flask.request.form)
    if bioeditform.validate_on_submit():
        newbio = bioeditform.bio.data
        database.update_bio(netid, newbio)
        bioeditform.bio.data = newbio
        html_code = flask.render_template(
            'bio_in_profile.html', bio=newbio, bioeditform=bioeditform)
        response = flask.make_response(html_code)
        return response
    else:
        errs = bioeditform.errors
        bio = database.get_user(netid).get_bio()
        bioeditform.bio.data = bio
        html_code = flask.render_template(
            'bio_in_profile_error.html',
            bio=bio,
            bioeditform=bioeditform,
            errs=errs)
        response = flask.make_response(html_code)
        return response
# ----------------------------------------------------------------------


@app.route('/editlinks', methods=['POST'])
def editlinks():
    netid = auth.authenticate()
    if database.is_banned(netid):
        html_code = flask.render_template(
            'banneduser.html', name=database.get_user(netid).get_name())
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
        err = linkeditform.errors
        linkeditform = LinkEditForm()
        links = database.get_user(netid).get_links()
        html_code = flask.render_template(
            'links_in_profile_error.html',
            links=links,
            linkeditform=linkeditform,
            errs=err)
        response = flask.make_response(html_code)
        return response


@app.route('/update_status', methods=['POST'])
def update_status():
    netid = auth.authenticate()
    try:
        if database.is_banned(netid):
            html_code = flask.render_template(
            'banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
        status_form = SetStatusForm(flask.request.form)
        if status_form.validate():
            if not database.owns_gig(netid, status_form.gigID.data):
                return flask.jsonify({'status': False})
            database.update_status(
                status_form.gigID.data, status_form.applicantID.data, status_form.status.data)
            return flask.jsonify({'status': True})
        else:
            return flask.jsonify({'status': False})
    except Exception as e:
        return flask.jsonify({'status': False})


@app.route('/add_bookmark/<int:gig_id>', methods=['POST'])
def add_bookmark_route(gig_id):
    netid = auth.authenticate()
    if database.is_banned(netid):
        html_code = flask.render_template(
            'banneduser.html', name=database.get_user(netid).get_name())
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
        html_code = flask.render_template(
            'banneduser.html', name=database.get_user(netid).get_name())
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

@app.route('/update_gig/<int:gig_id>', methods=['POST'])
def update_gig(gig_id):
    netid = auth.authenticate()
    try:
        if database.is_banned(netid):
            html_code = flask.render_template(
                'banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
        gig_form = EditGigForm(flask.request.form)

        if not database.owns_gig(netid, gig_id):
            html_code = flask.render_template(
                'banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response

        gig = database.get_gig_details(gig_id)

        if gig is None:
            html_code = flask.render_template(
                'banneduser.html', name=database.get_user(netid).get_name())
            response = flask.make_response(html_code)
            return response
        
        if gig_form.validate_on_submit():
            newTitle = gig_form.title.data
            newDescription = gig_form.description.data
            newQualifications = gig_form.qualifications.data
            newCategories = gig_form.categories.data
            gigHprice = gig_form.price.data

            gigAuthor = database.get_user(netid).get_name()
            gigStartDate = gig.get_stylized_fromdate()
            gigEndDate = gig.get_stylized_til_date()
            gigPostedDate = gig.get_stylized_post_date()

            owns = True

            database.update_gig_details(gig_id, netid, gig_form.title.data, gig_form.description.data, gig_form.qualifications.data, gig_form.categories.data, gig_form.price.data)
            html_code = flask.render_template('gig_in_edit.html',
                                        gigTitle=newTitle,
                                        gigPoster=gigAuthor,
                                        gigCategory=newCategories,
                                        gigDescription=newDescription,
                                        gigQualifications=newQualifications,
                                        gigStartDate=gigStartDate,
                                        gigEndDate=gigEndDate,
                                        gigPostedDate=gigPostedDate,
                                        is_owner=owns,
                                        gigID=id,
                                        gigHprice=gigHprice,
                                        get_usr = database.get_user,
                                        gig_form=gig_form)
            response = flask.make_response(html_code)
            return response
        else:
            errs = gig_form.errors
            print(errs)
            gig_form = EditGigForm()

            gigAuthor = database.get_user(netid).get_name()
            gigStartDate = gig.get_stylized_fromdate()
            gigEndDate = gig.get_stylized_til_date()
            gigPostedDate = gig.get_stylized_post_date()
            gigTitle = gig.get_title()
            gigDescription = gig.get_description()
            gigQualifications = gig.get_qualifications()
            gigCategory = gig.get_category()
            gigHprice = gig.get_hprice()

            owns = True
            html_code = flask.render_template('gig_in_edit_error.html',
                                        gigTitle=gigTitle,
                                        gigPoster=gigAuthor,
                                        gigCategory=gigCategory,
                                        gigDescription=gigDescription,
                                        gigQualifications=gigQualifications,
                                        gigStartDate=gigStartDate,
                                        gigEndDate=gigEndDate,
                                        gigPostedDate=gigPostedDate,
                                        is_owner=owns,
                                        gigID=id,
                                        gigHprice=gigHprice,
                                        get_usr = database.get_user,
                                        gig_form=gig_form,
                                        errs=errs)
            response = flask.make_response(html_code)
            return response
    except DatabaseError as e:
        raise e
    except Exception as e:
        raise ServerError

# -----------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8888)
