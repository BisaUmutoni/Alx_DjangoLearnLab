from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
     # BookSerializer serializes the Book model and validates the publication year
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    #he future
    def validate_publication_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError("The publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    # AuthorSerializer serializes the Author model and includes a nested BookSerializer
    books = BookSerializer(many=True, read_only=True)  # Nested relationship

    class Meta:
        model = Author
        fields = ['name', 'books']
