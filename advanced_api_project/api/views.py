from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

from .permissions import IsAuthorOrReadOnly

# ListView for retrieving all books
class BookListView(generics.ListAPIView): # View to list all books in the database.
    #Accessible to all users.
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow all users to read

# DetailView for retrieving a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Allow all users to read

# CreateView for adding a new book
class BookCreateView(generics.CreateAPIView):
    # View to create a new book.
    # Only authenticated users can perform this action.
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthorOrReadOnly]  # Only authenticated users can create

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # Current user assigned automatic as author

# UpdateView for modifying an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthorOrReadOnly]  # Only authenticated users can update

    def perform_update(self, serializer):
        serializer.save() # Save the serializer



# DeleteView for removing a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthorOrReadOnly]  # Only authenticated users can delete


