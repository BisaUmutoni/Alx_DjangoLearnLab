from django.shortcuts import render
from .models import Book
from .models import Library

def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app\list_books.html', {'books': books})

class LibraryDetailView():
    model = Library
    template_name = 'relationship_app\library_detail.html'
    context_object_name = 'library'


