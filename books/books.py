"""
My book navigator
"""

from flask import Flask, render_template, request
from bookdb import BookDB



app = Flask(__name__)

app.debug = True # development only - remove on production machines

# View functions generate HTTP responses including HTML pages and headers
all_books=BookDB()


#Show the welcome page
@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')


#Show the index page
@app.route('/index.html')
def index():
    return render_template('index.html',books=all_books)


#Show details page
@app.route('/book.html')
def book_info():
    #render the template for the selected book based on the id tag
    return render_template('book.html',book=all_books.title_info(request.args['id']))

# No function needed for other routes - Flask will send 404 page

if __name__ == '__main__':
    app.run()

