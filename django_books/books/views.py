# Create your views here.
from django.http import HttpResponse
from books.models import book
from bookdb import BookDB
from django.template import Context,loader

def index(books):
    t = loader.get_template('index.html')
    c = Context({
        'all_books': book.objects.all().order_by("title"),
    })
    return HttpResponse(t.render(c))

def detail(request,find_book_id):
    print find_book_id
    detail_book=book.objects.get(book_id=find_book_id)
    print detail_book.title
    t = loader.get_template('detail.html')
    c = Context({
        'book': detail_book,
    })
    return HttpResponse(t.render(c))
def my_admin(request):
    book_count=book.objects.all().count()
    t = loader.get_template('my_admin.html')
    c = Context({
        'book_count': book_count,
    })
    return HttpResponse(t.render(c))

def my_admin_purge(request):
    book.objects.all().delete()
    book_count=book.objects.all().count()
    t = loader.get_template('my_admin.html')
    c = Context({
        'book_count': book_count,
    })
    return HttpResponse(t.render(c))
   




def my_admin_load_BooksDB(request):
    my_books=BookDB()

    book_count=-1
    for my_book in my_books.titles():

        db_book=book()
        
        db_book.book_id=my_book['id']
        db_book.isbn=my_books.title_info(my_book['id'])['isbn'].replace('-','')
        
        db_book.title= my_books.title_info(my_book['id'])['title']
        db_book.author= my_books.title_info(my_book['id'])['author']
        db_book.publisher= my_books.title_info(my_book['id'])['publisher']
        print db_book.book_id,db_book.isbn        
        db_book.save()
        db_book=None
        book_count=book.objects.all().count()
        t = loader.get_template('my_admin.html')
        c = Context({
                'book_count': book_count,
            })
    return HttpResponse(t.render(c))

