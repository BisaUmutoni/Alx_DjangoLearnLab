from django.shortcuts import render
from .models import Book, Library
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView():
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

