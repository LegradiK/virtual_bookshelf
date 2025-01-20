import sqlite3


db = sqlite3.connect("books-collection.db")

cursor = db.cursor()

# Creating SQLite database / check details on Section 64, video 436
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# inserting a new set of data into the table of the database
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")

db.commit()