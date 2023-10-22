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
def get_gigs(keyword='', category=[]):
  return

def get_gig_details():
  return

def get_gigs_posted_by():
  return

def get_apps_for():
  return

def get_apps_by():
  return


#-----------------------------------------------------------------------
def _test():
  photoshoot = Gig()

if __name__ == '__main__':
    _test()
