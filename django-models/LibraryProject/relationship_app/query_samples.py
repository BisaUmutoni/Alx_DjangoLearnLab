# relationship_app/query_samples.py

import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Setup Django settings
# settings.configure(
#     DEBUG=True,
#     INSTALLED_APPS=[
#         'django.contrib.contenttypes',
#         'django.contrib.auth',
#         'relationship_app',
#     ],
#     DATABASES={
#         "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME":"djangodb",
#         "USER":"root",
#         "PASSWORD":"Maralba16!MYSQL",
#         "HOST":"localhost",
#         "PORT":"3306",
#         }
#     }
# )
# django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_all_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    print(f"Books by {author_name}:")
    for book in books:
        print(f"- {book.title}")

def list_all_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    print(f"Books in {library_name}:")
    for book in books:
        print(f"- {book.title}")

def retrieve_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = library.librarian
    print(f"Librarian for {library_name}:")
    print(f"- {librarian.name}")

if __name__ == "__main__":
    # You can modify these variables for testing
    query_all_books_by_author('J.K. Rowling')
    list_all_books_in_library('City Library')
    retrieve_librarian_for_library('City Library')
