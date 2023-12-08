#!/usr/bin/env python
# -----------------------------------------------------------------------
# user.py
# Author: Taylan Aydin
# -----------------------------------------------------------------------
class User:

    def __init__(
            self,
            netid,
            name,
            visible=False,
            bio='',
            links='',
            specialty='',
            last_active='',
            banned=False):
        self._netid = netid
        self._name = name
        self._visible = visible
        self._bio = bio
        self._links = links.split(',') if links else []
        self._specialty = specialty
        self._last_active = last_active
        self._banned = banned


    def get_netid(self):
        return self._netid

    def get_name(self):
        return self._name

    def is_visible(self):
        return self._visible

    def get_bio(self):
        return self._bio

    def get_links(self):  # returns in list format
        return self._links

    def get_specialty(self):
        return self._specialty

    def get_active(self):
        return self._last_active

    def is_banned(self):
        return self._banned

    def to_tuple(self):
        return (self._netid, self._name)

# -----------------------------------------------------------------------


def _test():
    tyl = User('ta0639', 'Taylan Aydin')
    print(tyl.get_name())
    print(tyl.get_netid())
    print(tyl.to_tuple())


if __name__ == '__main__':
    _test()
