#!/usr/bin/env python

#-----------------------------------------------------------------------
# book.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

class Book:

    def __init__(self, author, title, price):
        self._author = author
        self._title = title
        self._price = price

    def get_author(self):
        return self._author

    def get_title(self):
        return self._title

    def get_price(self):
        return self._price

    def to_tuple(self):
        return (self._author, self._title, self._price)

#-----------------------------------------------------------------------

def _test():
    book = Book('Kernighan', 'The Practice of Programming', 40.74)
    print(book.get_author())
    print(book.get_title())
    print(book.get_price())
    print(book.to_tuple())

if __name__ == '__main__':
    _test()
