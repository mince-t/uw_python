# Create your views here.
from django.http import HttpResponse
from books.models import book
from bookdb import BookDB
from django.template import Context,loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from django.core.context_processors import csrf
from django.shortcuts import render_to_response


def index(books):
    t = loader.get_template('index.html')
    c = Context({
        'all_books': book.objects.all().order_by("title"),
    })
    return HttpResponse(t.render(c))



def detail(request,find_book_id):
    try:
        detail_book=book.objects.get(book_id=find_book_id)
        
        t = loader.get_template('detail.html')
        c = Context({
            'book': detail_book,
        })
    except ObjectDoesNotExist:
        t = loader.get_template('404.html')
        c = Context({
            'book': 1,
        })  
    return HttpResponse(t.render(c))



def my_admin_logout(request):
    logout(request)
    return HttpResponseRedirect("/books/my_admin/")


def my_admin_login(request):
    t = loader.get_template('admin_login.html')
    c = Context({
        'book_count': 1,
    })
    return HttpResponse(t.render(c))

"""
    Very generic error handler.
"""
def gen_err(error_message,return_url):
    
    
    c = Context({
        #The error message to dispaly
        'error_message': error_message,
        #Where to go back to
        'return_path': return_url,
    })

    return render_to_response("gen_err.html", c)

"""
    Very generic message page.
"""
def gen_msg(message,next_url):
    
    
    c = Context({
        #The error message to dispaly
        'message': message,
        #Where to go back to
        'next_page': next_url,
    })

    return render_to_response("gen_msg.html", c)



@login_required(login_url='/books/my_admin/login/')
def my_admin_modify_book(request,modify_type,book_id=''):


    
    c = Context({
        'modify_type': modify_type,
    })

    # If we are responding to a postback in a real world 
    # scenerio, there would probably be  a confirmation 
    # page or message to keep this manageable for a homework 
    # assignment, I'm skipping that
   
    if request.POST:
        #If all required elelements for a book record exist
        #and we have an acceptible modifier
        #[in the real world I would do more to vet the inputs]
        if request.POST['title'] and request.POST['author'] and request.POST['isbn'] and (book_id or request.POST['book_id'])and ((modify_type=="add") or (modify_type=="edit")):
            
            #If we were told to edit a book
            if modify_type=='edit':

                #Perform the edit
                edit_book=book.objects.get(book_id=book_id)
                edit_book.title=request.POST['title']
                edit_book.isbn=request.POST['isbn']
                edit_book.author=request.POST['author']
                edit_book.publisher=request.POST['publisher']
                edit_book.save()
                
                #send back to main admin
                return gen_msg("Record updated.","/books/my_admin/")

            elif modify_type=='add':
                save_book(request.POST['book_id'],request.POST['isbn'],request.POST['title'],request.POST['author'],request.POST['publisher'])
                return gen_msg("Record added.","/books/my_admin/")
        else:
            if modify_type=='edit':
                return gen_err("You must supply title, author and isbn.  Click the link below to try again.",request.path)
            elif modify_type=='add':
                return gen_err("You must supply book id,title, author and isbn.  Click the link below to try again.",request.path)
            else:
                return gen_err("You did something really wrong.  Start from scratch!","/books/my_admin/")
    else:
        if modify_type=='edit':
            if book_id!='':
                print book_id
                c['current_book']=book.objects.get(book_id=book_id)
            else:
                return gen_err("You did something really wrong.  Start from scratch!","/books/my_admin/")
        
        
    
        
    c.update(csrf(request))
    return render_to_response("modify_book.html", c)
    

@login_required(login_url='/books/my_admin/login/')
def my_admin(request):
    
    if request.POST:
        print "post"
        if 'operation' in request.POST.keys():
            if request.POST['operation']=='delete book':
                print "deleting book id " + request.POST['book']
                #book.objects.filter("book_id=" + request.POST['book'] ).delete()
                book.objects.get(book_id=request.POST['book']).delete()
            elif request.POST['operation']=='edit book':
                return HttpResponseRedirect("/books/my_admin/modify_book/edit/" + request.POST['book'] + "/")
            elif request.POST['operation']=='new book':
                return HttpResponseRedirect("/books/my_admin/modify_book/add//")
            elif request.POST['operation']==u'purge books':
                print 'purging books'
                book.objects.all().delete()
            elif request.POST['operation']==u'import books':
                my_admin_load_BooksDB()

            
    #t = loader.get_template('my_admin.html')
    c = Context({
        'all_books': book.objects.all().order_by("title"),
    })


    
    c.update(csrf(request))
    # ... view code here
    return render_to_response("my_admin.html", c)

    
    #return HttpResponse(t.render(c))








@login_required(login_url='/books/my_admin/login/')
def my_admin_purge(request):
    book.objects.all().delete()
    return my_admin(request)
   

def save_book(book_id,isbn,title,author,publisher):
        new_book=book()
        
        new_book.book_id=book_id
        new_book.isbn=isbn
        
        new_book.title= title
        new_book.author= author
        new_book.publisher= publisher
        new_book.save()
def my_admin_load_BooksDB():
    my_books=BookDB()

    book_count=-1
    for my_book in my_books.titles():

        
        save_book(  my_book['id'], my_books.title_info(my_book['id'])['isbn'].replace('-',''),my_books.title_info(my_book['id'])['title'], my_books.title_info(my_book['id'])['author'], my_books.title_info(my_book['id'])['publisher']  )
        
        
    
    

