"""
Minimal Flask + forms demo

Send HTML page that echoes message from HTTP request
To get started, point browser at echo_flask.html
"""

from flask import Flask, render_template, request
from bookdb import BookDB

# form_page is now a template

# No need for message page
# Flask converts view function return string to HTML page

app = Flask(__name__)

app.debug = True # development only - remove on production machines

# View functions generate HTTP responses including HTML pages and headers
all_books=BookDB()
print all_books.titles()


@app.route('/index.html')
def index():
    return render_template('index.html',books=all_books)

@app.route('/book.html')
def book_info():
    # Flask Quickstart suggests request.form should work, but here it is empty
    # Flask converts return string to HTML page
    print all_books.title_info(request.args['id'])
    return render_template('book.html',book=all_books.title_info(request.args['id']))

# No function needed for other routes - Flask will send 404 page

if __name__ == '__main__':
    app.run()

