from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^books/my_admin/$','books.views.my_admin'),
    url(r'^books/my_admin/admin_action/$','books.views.my_admin'),
    url(r'^books/my_admin/logout/$','books.views.my_admin_logout'),
    url(r'^books/my_admin/login/$','django.contrib.auth.views.login',{'template_name':'admin_login.html'}),
    url(r'^books/my_admin/purge/$','books.views.my_admin_purge'),
    url(r'^books/my_admin/load_BooksDB/$','books.views.my_admin_load_BooksDB'),
    url(r'^books/$','books.views.index'),
    url(r'^books/gen_err/$','books.views.gen_err'),
    url(r'^books/my_admin/modify_book/(?P<modify_type>\S+)/(?P<book_id>\S*)/$','books.views.my_admin_modify_book'),
    url(r'^books/(?P<find_book_id>\S+)/$','books.views.detail'),
                
    # Examples:
    # url(r'^$', 'django_books.views.home', name='home'),
    # url(r'^django_books/', include('django_books.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
