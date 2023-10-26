DROP TABLE IF EXISTS books;

CREATE TABLE books (author TEXT, title TEXT, price REAL);

INSERT INTO books (author, title, price)
   VALUES ('Kernighan','The Practice of Programming',40.74);
INSERT INTO books (author, title, price)
   VALUES ('Kernighan','The C Programming Language',24.99);
INSERT INTO books (author, title, price)
   VALUES ('Sedgewick','Algorithms in C',61.59);
