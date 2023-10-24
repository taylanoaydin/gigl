#!/usr/bin/env python
#-----------------------------------------------------------------------
# database.py
# Author: Taylan Aydin
#-----------------------------------------------------------------------

import os
import sys
import psycopg2
import dotenv
#-----------------------------------------------------------------------

dotenv.load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']

#-----------------------------------------------------------------------

# GET FUNCTIONS FOR INFORMATION RETRIEVAL! NO CHANGES MADE TO          #
# DATABASE                                                             #

# 2 search features: a keyword in any of the fields,
# and search within a list of categories (or all of them)
# default returns Gig objects sorted rev-chron by submission date

def get_gigs(keyword='', categories=[]):
    conn = psycopg2.connect(DATABASE_URL) # connects to database
    cursor = conn.cursor() # sets up cursor for SQL commands 

    # If no categories are selected, retrieve all gigs that match the keyword
    if not categories:
        query = "SELECT * FROM gigs WHERE title LIKE %s OR description LIKE %s OR qualf LIKE %s ORDER BY posted DESC"
        cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    else:
        query = "SELECT * FROM gigs WHERE (title LIKE %s OR description LIKE %s OR qualf LIKE %s) AND category IN %s ORDER BY posted DESC"
        cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', tuple(categories))) # "IN" requires tuple format 

    gigs = cursor.fetchall()
    cursor.close()
    conn.close()
    return gigs #returns tuple of gigs with their respective details 

# returns Gig object for the gig with gigID
def get_gig_details(gigID):
    return

# returns list of Gig's posted by netid
def get_gigs_posted_by(netid):
    return

# returns list of Application's sent to gig with gigID
def get_apps_for(gigID):
    return

# returns list of Application's sent by user with netid (to any gig)
def get_apps_by(netid):
    return

# returns the single application sent by user with netid to gig with
# gigID. Returns None if no application sent by netid to gigID.
# note to devs: compare return value with None to see if 
# user already applied
def get_application(netid, gigID):
    return

#-----------------------------------------------------------------------
# FUNCTIONS THAT POTENTIALLY CHANGE DATABASE

# Checks if user with the given netid already exists, if not, adds them
# to database (used after login).
def check_and_add_user(netid, name):
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
  

if __name__ == '__main__':
    _test()
