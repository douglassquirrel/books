from json import loads
from sqlite3 import connect
from urllib import urlopen

DB_FILE = 'books.db'
SELECT_SQL = 'SELECT isbn FROM books WHERE google_id IS NULL'
UPDATE_SQL = '''
    UPDATE books SET google_id=?, title=?, authors=?, publisher=?,
                     description=?, pages=?, google_link=?
                 WHERE isbn=?
'''
GOOGLE_TEMPLATE = 'https://www.googleapis.com/books/v1/volumes?q=isbn:%s'

def lookup():
    connection = connect(DB_FILE)
    cursor = connection.cursor()

    incomplete_rows = list(cursor.execute(SELECT_SQL))
    for row in incomplete_rows:
        isbn = row[0]
        print 'Now updating isbn %s' % isbn
        url = GOOGLE_TEMPLATE % isbn
        google_data = loads(get(url))
        if google_data['totalItems'] == 0:
            print 'No data or bad isbn - skipping %s' % isbn
            continue
        parsed_data = parse(google_data)
        update(isbn, parsed_data, connection)

    connection.close()

def get(url):
    return urlopen(url).read()

def parse(google_data):
    parsed_data = {}
    item_data = google_data['items'][0]
    parsed_data['google_id'] = item_data.get('id', None)
    volume_info = item_data.get('volumeInfo', {})
    parsed_data['title'] = volume_info.get('title', None)
    authors = volume_info.get('authors', None)
    if authors:
        parsed_data['authors'] = ','.join(authors)
    else:
        parsed_data['authors'] = None
    parsed_data['publisher'] = volume_info.get('publisher', None)
    parsed_data['description'] = volume_info.get('description', None)
    parsed_data['pages'] = volume_info.get('pageCount', None)
    parsed_data['google_link'] = volume_info.get('canonicalVolumeLink', None)
    return parsed_data

def update(isbn, parsed_data, connection):
    cursor = connection.cursor()
    cursor.execute(UPDATE_SQL,
                   (parsed_data['google_id'],
                    parsed_data['title'],
                    parsed_data['authors'],
                    parsed_data['publisher'],
                    parsed_data['description'],
                    parsed_data['pages'],
                    parsed_data['google_link'],
                    isbn))
    connection.commit()

lookup()
