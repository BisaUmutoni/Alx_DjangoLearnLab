from django.shortcuts import render
from .models import Book
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Library

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    content_object_name = 'library'


