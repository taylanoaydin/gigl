#!/usr/bin/env python
# -----------------------------------------------------------------------
# database.py
# Author: Taylan Aydin
# -----------------------------------------------------------------------

import os
import sys
import psycopg2
import dotenv
from cas_details import cas_details
import queue
import application as app
import gig
import user
from datetime import datetime

# -----------------------------------------------------------------------

dotenv.load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']

_connection_pool = queue.Queue()

# -----------------------------------------------------------------------


def _get_connection():
    try:
        conn = _connection_pool.get(block=False)
    except queue.Empty:
        conn = psycopg2.connect(DATABASE_URL)
    return conn


def _put_connection(conn):
    _connection_pool.put(conn)


def _close_all_connections():
    while not _connection_pool.empty():
        connection = _connection_pool.get()
        connection.close()

# -----------------------------------------------------------------------
# GET FUNCTIONS FOR INFORMATION RETRIEVAL! NO CHANGES MADE TO          #
# DATABASE                                                             #

# 2 search features: a keyword in any of the fields,
# and search within a list of categories (or all of them)
# default returns Gig objects sorted rev-chron by submission date
# Returns exception if there was an error in database handling


def get_gigs(keyword='', categories=None):
    if categories is None:
        categories = []
    gigs = []
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            kw = '%' + keyword + '%'
            all_args = [kw for _ in range(3)]
            query = """SELECT * FROM gigs
                       WHERE (title ILIKE %s OR
                             description ILIKE %s OR
                             qualf ILIKE %s)"""
            if len(categories) != 0:
                query += " AND category = ANY(%s)"
                all_args.append(categories)
            query += " ORDER BY posted DESC"

            cursor.execute(query, all_args)
            table = cursor.fetchall()
            for row in table:
                a_gig = gig.Gig(*row)
                gigs.append(a_gig)
    except Exception as ex:
        # Log the exception as in gigl.py
        app.logger.error(f"Database Error: {ex}")
        raise  # Reraise the exception or handle it as needed
    finally:
        _put_connection(connection)
    return gigs

# returns Gig object for the gig with gigID


def get_gig_details(gigID):
    connection = _get_connection()
    thisgig = None
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM gigs WHERE gigID = %s"
            cursor.execute(query, [gigID])
            gigdetails = cursor.fetchone()

            if gigdetails is None:
                return None

            thisgig = gig.Gig(*gigdetails)
    except Exception as ex:
        app.logger.error(f"Database Error: {ex}")
        raise
    finally:
        _put_connection(connection)
    return thisgig

# returns list of Gig's posted by netid


def get_gigs_posted_by(netid):
    connection = _get_connection()
    gigs = []
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM gigs WHERE netid = %s"
            cursor.execute(query, [netid])
            postedgigs = cursor.fetchall()

            for row in postedgigs:
                thisgig = gig.Gig(*row)
                gigs.append(thisgig)
    except Exception as ex:
        app.logger.error(f"Database Error: {ex}")
        raise
    finally:
        _put_connection(connection)
    return gigs

# returns list of Application's sent to gig with gigID


def get_apps_for(gigID):
    connection = _get_connection()
    apps = []
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM apps WHERE gigID = %s"
            cursor.execute(query, [gigID])
            received_apps = cursor.fetchall()

            for row in received_apps:
                thisapp = app.Application(*row)
                apps.append(thisapp)
    except Exception as ex:
        app.logger.error(f"Database Error: {ex}")
        raise
    finally:
        _put_connection(connection)
    return apps


# returns list of Application's sent by user with netid (to any gig)
def get_apps_by(netid):
    connection = _get_connection()
    apps = []
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM apps WHERE netid = %s"
            cursor.execute(query, [netid])
            sent_apps = cursor.fetchall()

            for row in sent_apps:
                thisapp = app.Application(*row)
                apps.append(thisapp)
    except Exception as ex:
        app.logger.error(f"Database Error: {ex}")
        raise
    finally:
        _put_connection(connection)
    return apps

# returns the single application sent by user with netid to gig with
# gigID. Returns None if no application sent by netid to gigID.
# note to devs: compare return value with None to see if
# user already applied


def get_application(netid, gigID):
    connection = _get_connection()
    thisapp = None
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM apps WHERE gigID = %s AND netid = %s"
            cursor.execute(query, [gigID, netid])
            row = cursor.fetchone()

            if row is None:
                return None

            thisapp = app.Application(*row)
    except Exception as ex:
        app.logger.error(f"Database Error: {ex}")
        raise
    finally:
        _put_connection(connection)
    return thisapp

# RETURNS ALL INFORMATION ABOUT PERSON WITH NETID = netid


def get_user(netid):
    connection = _get_connection()
    thisuser = None
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE netid = %s"
            cursor.execute(query, [netid])
            row = cursor.fetchone()

            if row is None:
                return None

            thisuser = user.User(*row)
    except Exception as ex:
        app.logger.error(f"Database Error: {ex}")
        raise
    finally:
        _put_connection(connection)
    return thisuser

# returns list of visible users with only RELEVANT information for the
# overall profile search: netid, name, specialty, last_active


def get_freelancers(keyword='', specialty=''):
    users = []
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            kw = '%' + keyword + '%'
            all_args = [kw]
            query = """SELECT netid, name, specialty, last_active FROM users
                       WHERE name ILIKE %s AND visible"""
            if specialty != '':
                query += " AND specialty=%s"
                all_args.append(specialty)
            query += " ORDER BY last_active DESC"

            cursor.execute(query, all_args)
            table = cursor.fetchall()
            for row in table:
                thisuser = user.User(
                    netid=row[0],
                    name=row[1],
                    specialty=row[2],
                    last_active=row[3])
                users.append(thisuser)
            return users
    except Exception as ex:
        app.logger.error(f"Database Error: {ex}")
        raise
    finally:
        _put_connection(connection)
# -----------------------------------------------------------------------
# FUNCTIONS THAT POTENTIALLY CHANGE DATABASE

# Checks if user with the given netid already exists, if not, adds them
# to database (used after login). Returns true if successful, exception else
# if there was any error in the addition of the user to the database


def check_and_add_user(netid):
    usr = get_user(netid)
    if usr is None:
        connection = _get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('BEGIN')

                usrname = cas_details(netid)[0]
                query = "INSERT INTO users (netid, name, visible, bio, links, specialty, last_active) VALUES (%s, %s, 'n', '', '', '', %s)"
                cursor.execute(query, [netid, usrname, datetime.now().date()])

                cursor.execute('COMMIT')

                return "user_created"
        except Exception as ex:
            # Log the exception as in gigl.py
            app.logger.error(f"Database Error: {ex}")
            raise  # Reraise the exception or handle it as needed
        finally:
            _put_connection(connection)
    return True

# Deletes gig with the given gigID from both applications and gigs.
# raises exception if there was an error and it couldn't be deleted, true
# otherwise


def delete_gig_from_db(gigID):
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('BEGIN')

            q1 = "DELETE FROM apps WHERE gigID = %s"
            cursor.execute(q1, [gigID])

            q2 = "DELETE FROM gigs WHERE gigID = %s"
            cursor.execute(q2, [gigID])

            cursor.execute('COMMIT')
    except Exception as ex:
        app.logger.error(f"Database Error: {ex}")
        raise
    finally:
        _put_connection(connection)
    return True

# Creates gig with the given parameters. Unique gigID is automatically
# created for any gig. Returns gigID normally, -1 if there was any
# problem adding to db


def create_gig(netid, title, category, description, qualf, startfrom,
               until, posted):
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('BEGIN')

            query = """INSERT INTO gigs
            (netid, title, category, description,
            qualf, startfrom, until, posted)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING gigID"""

            cursor.execute(
                query, [
                    netid, title, category, description, qualf, startfrom, until, posted])
            gigID = cursor.fetchone()[0]

            cursor.execute('COMMIT')
            return gigID
    except Exception as ex:
        return -1
    finally:
        _put_connection(connection)

# Sends application from user with netid to gig with gigID with the
# given message.


def send_application(netid, gigID, message):
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            validgig = "SELECT * FROM gigs WHERE gigID = %s"

            cursor.execute(validgig, [gigID])
            row = cursor.fetchone()

            if row is None:
                return False

            cursor.execute('BEGIN')

            query = """INSERT INTO apps
                (netid, gigID, message) VALUES
                (%s, %s, %s)"""
            cursor.execute(query, [netid, gigID, message])

            cursor.execute('COMMIT')
            return True
    except Exception as ex:
        app.logger.error(f"Database Error: {ex}")
        raise
    finally:
        _put_connection(connection)


def set_visibility(netid, visible):
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('BEGIN')
            query = "UPDATE users "
            if visible:
                query += "SET visible='y'"
            else:
                query += "SET visible='n'"
            query += " WHERE netid = %s"

            cursor.execute(query, [netid])
            cursor.execute('COMMIT')
            return True
    except Exception as ex:
        app.logger.error(f"Database Error: {ex}")
        raise
    finally:
        _put_connection(connection)


def update_activity(netid):
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('BEGIN')
            query = "UPDATE users SET last_active = %s"
            query += " WHERE netid = %s"

            cursor.execute(query, [datetime.now().date(), netid])
            cursor.execute('COMMIT')
            return True
    except Exception as ex:
        app.logger.error(f"Database Error: {ex}")
        raise
    finally:
        _put_connection(connection)


def update_bio(netid, newbio):
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('BEGIN')
            query = "UPDATE users SET bio = %s"
            query += " WHERE netid = %s"

            cursor.execute(query, [newbio, netid])
            cursor.execute('COMMIT')
            return True
    except Exception as ex:
        return False
    finally:
        _put_connection(connection)


def update_links(netid, links):
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('BEGIN')
            query = "UPDATE users SET links = %s"
            query += " WHERE netid = %s"

            csv_links = ','.join(links)
            cursor.execute(query, [csv_links, netid])
            cursor.execute('COMMIT')
            return True
    except Exception as ex:
        return False
    finally:
        _put_connection(connection)

def ban_user(netid):
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            if is_banned(netid):
                return True
            cursor.execute('BEGIN')
            query = "INSERT INTO banned_users (netid) VALUES (%s)"

            cursor.execute(query, [netid])
            cursor.execute('COMMIT')
            return True
    except Exception as ex:
        return False
    finally:
        _put_connection(connection)

def is_banned(netid): # finish
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT FROM banned_users WHERE netid=%s"
            cursor.execute(query, [netid])
            row = cursor.fetchone()
            
            return not (row is None)
    except Exception as ex:
        raise ex
    finally:
        _put_connection(connection)
# -----------------------------------------------------------------------

# BOOLEAN RETURN FUNCTIONS

# true if netid posted gig with gigID, exception otherwise


def owns_gig(netid, gigID):
    try:
        thisgig = get_gig_details(gigID)
        return (thisgig is not None) and (thisgig.get_netid() == netid)
    except Exception as ex:
        app.logger.error(f"Database Error: {ex}")
        raise

# -----------------------------------------------------------------------

def add_bookmark(netid, gigID):
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            # Check if the bookmark already exists
            check_query = "SELECT COUNT(*) FROM bookmarks WHERE netid = %s AND gigID = %s"
            cursor.execute(check_query, [netid, gigID])
            if cursor.fetchone()[0] > 0:
                return "already_exists"  # Bookmark already exists

            # If not, add the new bookmark
            query = "INSERT INTO bookmarks (netid, gigID) VALUES (%s, %s)"
            cursor.execute(query, [netid, gigID])
            connection.commit()
            return True
    except Exception as ex:
        print(ex)
        connection.rollback()
        return False
    finally:
        _put_connection(connection)

def remove_bookmark(netid, gigID):
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM bookmarks WHERE netid = %s AND gigID = %s"
            cursor.execute(query, [netid, gigID])
            connection.commit()
            return True
    except Exception as ex:
        print(ex)
        connection.rollback()
        return False
    finally:
        _put_connection(connection)

def is_bookmarked(netid, gigID):
    connection = _get_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) FROM bookmarks WHERE netid = %s AND gigID = %s"
            cursor.execute(query, [netid, gigID])
            count = cursor.fetchone()[0]
            return count > 0
    except Exception as ex:
        print(ex)
        return False
    finally:
        _put_connection(connection)

def _test():
    check_and_add_user('cos-gigl')
    _close_all_connections()
    return


if __name__ == '__main__':
    _test()
