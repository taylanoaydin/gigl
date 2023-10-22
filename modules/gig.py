#!/usr/bin/env python
#-----------------------------------------------------------------------
# user.py
# Author: Taylan Aydin
#-----------------------------------------------------------------------

class Gig:

    def __init__(self, netid, gigID, 
                 title, cat, desc, qual, from_date, til_date, post_date):
        self._netid = netid
        self._gigID = gigID
        self._title = title
        self._cat = cat
        self._desc = desc
        self._qual = qual
        self._from_date = from_date
        self._til_date = til_date
        self._post_date = post_date

    def get_netid(self):
        return self._netid

    def get_gigID(self):
        return self._gigID
    
    def get_title(self):
        return self._title
    
    def get_category(self):
        return self._cat
    
    def get_description(self):
        return self._desc
    
    def get_qualifications(self):
        return self._qual
     
    def get_fromdate(self):
        return self._from_date
    
    def get_til_date(self):
        return self._til_date
    
    def get_post_date(self):
        return self._post_date

#-----------------------------------------------------------------------

def _test():
  photoshoot = Gig()

if __name__ == '__main__':
    _test()
