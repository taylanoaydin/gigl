#!/usr/bin/env python
#-----------------------------------------------------------------------
# database.py
# Author: Taylan Aydin
#-----------------------------------------------------------------------

import os
import sys
import psycopg2
import dotenv
import queue
import application as app
import gig
import user
#-----------------------------------------------------------------------

dotenv.load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']

_connection_pool = queue.Queue()

#-----------------------------------------------------------------------
def _get_connection():
    try:
        conn = _connection_pool.get(block=False)
    except queue.Empty:
        conn = psycopg2.connect(DATABASE_URL)
    return conn

def _put_connection(conn):
    _connection_pool.put(conn)

#-----------------------------------------------------------------------
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
        return 0
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
        return 0
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
        return 0
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
        return 0
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
        return 0
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
        return 0
    finally:
        _put_connection(connection)
    return thisapp

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
        return 0
    finally:
        _put_connection(connection)
    return thisuser

#-----------------------------------------------------------------------
# FUNCTIONS THAT POTENTIALLY CHANGE DATABASE

# Checks if user with the given netid already exists, if not, adds them
# to database (used after login).
def check_and_add_user(netid):
    return

# Deletes gig with the given gigID from both applications and gigs.
# returns false if gigID doesn't exist, true otherwise
def delete_gig_from_db(gigID):
    return

# Creates gig with the given parameters. Unique gigID is automatically 
# created for any gig.
def create_gig(netid, title, category, description, qualf, startfrom, 
              until, posted):
    return

# Sends application from user with netid to gig with gigID with the
# given message. 
def send_application(netid, gigID, message):
    return

#-----------------------------------------------------------------------

# BOOLEAN RETURN FUNCTIONS

# true if netid posted gig with gigID, false otherwise
def owns_gig(netid, gigID):
    return


#-----------------------------------------------------------------------
def _test():
    return

if __name__ == '__main__':
    _test()
