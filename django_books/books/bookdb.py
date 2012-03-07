"""
From Brian Dorsey's Internet Programming in Python, Winter 2011
"""

class BookDB():
    def titles(self):
        titles = [dict(id=id, title=database[id]['title']) for id in database.keys()]
        print titles
        return titles

    def title_info(self, id):
        return database[id]


        
# let's pretend we're getting this information from a database somewhere
database = {
    'id1' : {'title' : 'CherryPy Essentials: Rapid Python Web Application Development',
             'isbn' : '978-1904811848',
             'publisher' : 'Packt Publishing (March 31, 2007)',
             'author' : 'Sylvain Hellegouarch',
           },
    'id2' : {'title' : 'Python for Software Design: How to Think Like a Computer Scientist',
             'isbn' : '978-0521725965',
             'publisher' : 'Cambridge University Press; 1 edition (March 16, 2009)',
             'author' : 'Allen B. Downey',
           },
    'id3' : {'title' : 'Foundations of Python Network Programming',
             'isbn' : '978-1430230038',
             'publisher' : 'Apress; 2 edition (December 21, 2010)',
             'author' : 'John Goerzen',
           },
    'id4' : {'title' : 'Python Cookbook, Second Edition',
             'isbn' : '978-0-596-00797-3',
             'publisher' : 'O''Reilly Media',
             'author' : 'Alex Martelli, Anna Ravenscroft, David Ascher',
           },
    'id5' : {'title' : 'The Pragmatic Programmer: From Journeyman to Master',
             'isbn' : '978-0201616224',
             'publisher' : 'Addison-Wesley Professional (October 30, 1999)',
             'author' : 'Andrew Hunt, David Thomas',
           },
}


books=BookDB()
longest_isbn=0
longest_title=0
longest_author = 0
longest_publisher=0

for book in books.titles():
    if len(books.title_info(book['id'])['title'])>longest_title:
        longest_title=len(books.title_info(book['id'])['title'])

    if len(books.title_info(book['id'])['isbn'])>longest_isbn:
        longest_isbn=len(books.title_info(book['id'])['isbn'])
    if len(books.title_info(book['id'])['publisher'])>longest_publisher:
        longest_publisher=len(books.title_info(book['id'])['publisher'])
    if len(books.title_info(book['id'])['author'])>longest_author:
        longest_author=len(books.title_info(book['id'])['author'])
        

print "longest isbn:     %i" % (longest_isbn * 1.5)
print "longest title:    %i" % (longest_title * 1.5)
print "longest author:   %i" % (longest_author * 1.5)
print "longest publisher %i" % (longest_publisher * 1.5)
