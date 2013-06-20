from sqlite3 import connect

DB_FILE = 'books.db'
SELECT_SQL = '''
    SELECT title, authors, location, google_link,
       description, publisher, pages, isbn, google_id
    FROM books
'''
HTML_TEMPLATE = '''
<!doctype HTML>
<html lang="en">
  <head>
    <meta charset=utf-8>
    <title>Lisa and Squirrel's Books</title>
    <style>
      table, th, td
      {
        border: 1px solid black;
      }
    </style>
  </head>
  <body>
    <h1>Lisa and Squirrel's Books</h1>
    <table>
      <tr>
        <th>Title</th>
        <th>Author(s)</th>
        <th>Location</th>
        <th>Link</th>
        <th>Description</th>
        <th>Publisher</th>
        <th>Pages</th>
        <th>ISBN</th>
        <th>Google ID</th>
      </tr>
      %s
    </table>
  </body>
</html>
'''
ROW_TEMPLATE = '''
<tr>
  <td>%s</td>
  <td>%s</td>
  <td>%s</td>
  <td>%s</td>
  <td>%s</td>
  <td>%s</td>
  <td>%s</td>
  <td>%s</td>
  <td>%s</td>
</tr>
'''

def html():
    connection = connect(DB_FILE)
    cursor = connection.cursor()
    rows = cursor.execute(SELECT_SQL)
    html_rows = []
    for row in rows:
        row = list(row)
        row[3] = '<a href="%s">%s</a>' % (row[3], row[0])
        html_rows.append(ROW_TEMPLATE % tuple(row))
    html = HTML_TEMPLATE % '\n'.join(html_rows)
    with open('books.html', 'w') as f:
        f.write(html)

html()
