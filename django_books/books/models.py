from django.db import models
import settings
from os import path
# Create your models here.

class book(models.Model):
    book_id   = models.CharField(max_length=3,primary_key=True)
    title     = models.CharField(max_length=100)
    isbn      = models.CharField(max_length=25)
    author    = models.CharField(max_length=70)
    publisher = models.CharField(max_length=85)

    def get_cover_file(self):
        if  path.isfile(settings.STATIC_ROOT  + 'images/' + self.isbn + '.jpeg'):
            return settings.STATIC_URL  + 'images/' + self.isbn + '.jpeg'
        else:
            return settings.STATIC_URL  + 'images/no_cover.jpeg'
    
        
        
    

