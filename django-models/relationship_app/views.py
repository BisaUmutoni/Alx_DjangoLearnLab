from django.shortcuts import render
from .models import Book
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Library

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    response_message = '\n'.join([f"{book.title} by {book.author.name}" for book in books])
    return HttpResponse (response_message, content_type = "text/plain")

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    content_object_name = 'library'