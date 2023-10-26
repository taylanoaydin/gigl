#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import sqlite3
import contextlib
import book as bookmod

#-----------------------------------------------------------------------

_DATABASE_URL = 'file:penny.sqlite?mode=ro'

#-----------------------------------------------------------------------

def get_books(author):

    books = []

    with sqlite3.connect(_DATABASE_URL, isolation_level=None,
        uri=True) as connection:

        with contextlib.closing(connection.cursor()) as cursor:

            query_str = "SELECT author, title, price FROM books "
            query_str += "WHERE author LIKE ?"
            cursor.execute(query_str, [author+'%'])

            table = cursor.fetchall()
            for row in table:
                book = bookmod.Book(row[0], row[1], row[2])
                books.append(book)

    return books

#-----------------------------------------------------------------------

def _test():
    books = get_books('ker')
    for book in books:
        print(book.get_author())
        print(book.get_title())
        print(book.get_price())
        print()

if __name__ == '__main__':
    _test()
