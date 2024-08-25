from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Definition for Author Model
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Definition for Book Model    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Definition for Library Model    
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

# Definition for Librarian Model    
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length= 200)
    def __str__(self):
        return self.user.username

class UserRole(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f'{self.user.username} - {self.role}'
    
    
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
       UserProfile.objects.create(user=instance)
    instance.UserProfile.save()