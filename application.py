#!/usr/bin/env python
# -----------------------------------------------------------------------
# application.py
# Author: Taylan Aydin
# -----------------------------------------------------------------------

class Application:

    def __init__(self, appl_netid, gigID, msg, status):
        self._appl_netid = appl_netid
        self._gigID = gigID
        self._msg = msg
        self._status = status

    def get_applicant_netid(self):
        return self._appl_netid

    def get_gigID(self):
        return self._gigID

    def get_message(self):
        return self._msg
    
    def get_status(self):
        return self._status

    def to_tuple(self):
        return (self._appl_netid, self._gigID, self._msg)

# -----------------------------------------------------------------------


def _test():
    myapp = Application(
        'ta0639',
        '14',
        'Hey! I am interested in taking your graduation ' +
        'photos!\nI have a lot of experience and would love to ' +
        'talk about this further. Hit me up!')
    print(myapp.get_applicant_netid())
    print(myapp.get_gigID())
    print(myapp.get_message())
    print()
    print(myapp.to_tuple())


if __name__ == '__main__':
    _test()
