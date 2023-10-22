#!/usr/bin/env python
#-----------------------------------------------------------------------
# user.py
# Author: Taylan Aydin
#-----------------------------------------------------------------------

class User:

    def __init__(self, netid, name):
        self._netid = netid
        self._name = name

    def get_netid(self):
        return self._netid

    def get_name(self):
        return self._name

    def to_tuple(self):
        return (self._netid, self._name)

#-----------------------------------------------------------------------

def _test():
    tyl = User('ta0639', 'Taylan Aydin')
    print(tyl.get_name())
    print(tyl.get_netid())
    print(tyl.to_tuple())

if __name__ == '__main__':
    _test()
