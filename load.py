from csv import reader
from sqlite3 import connect
from sys import argv

DB_FILE = 'books.db'
CREATE_SQL = '''
    CREATE TABLE IF NOT EXISTS books
    (id INTEGER PRIMARY KEY,
     isbn TEXT, location TEXT, google_id TEXT, title TEXT, authors TEXT,
     publisher TEXT, description TEXT, pages INTEGER, google_link TEXT)
'''
INDEX_SQL = 'CREATE UNIQUE INDEX IF NOT EXISTS isbn ON books (isbn)'
INSERT_SQL = 'INSERT INTO books (isbn, location) VALUES (?, ?)'

def insert():
    connection = connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute(CREATE_SQL)
    cursor.execute(INDEX_SQL)
    connection.commit()

    csv_file = argv[1]
    with open(csv_file, 'rb') as f:
        book_reader = reader(f)
        for row in book_reader:
            print row
            isbn = row[0]
            location = row[1]
            cursor.execute(INSERT_SQL, (isbn, location))

    connection.commit()
    connection.close()

insert()
