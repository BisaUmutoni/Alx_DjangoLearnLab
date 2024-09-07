from django.db import models

# Create your models here.

class Author(models.Model):
    # The Author class model stores the name of the author
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model): 
    # The Book class model stores the name of the attributes and a foreign key to Author
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField() 
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title