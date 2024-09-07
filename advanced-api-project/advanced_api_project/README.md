Advanced API Project
This project is built with Django REST Framework to manage a collection of Books and their Authors. The application uses both generic views and custom views to handle CRUD operations while enforcing permissions to ensure only authenticated users can create, update, or delete resources. Additionally, only the authors of books are allowed to modify or delete their own entries.

Project Overview
Framework: Django REST Framework
Features: Custom views, generic views, permission enforcement, nested serializers
Models:
Author: Stores the name of the author.
Book: Stores the title, publication year, and links to an author (ForeignKey relationship).


Here’s a draft for your README.md file, explaining the views, endpoints, and how the permissions are set up for your Django REST Framework project.

Advanced API Project
This project is built with Django REST Framework to manage a collection of Books and their Authors. The application uses both generic views and custom views to handle CRUD operations while enforcing permissions to ensure only authenticated users can create, update, or delete resources. Additionally, only the authors of books are allowed to modify or delete their own entries.

Project Overview
Framework: Django REST Framework
Features: Custom views, generic views, permission enforcement, nested serializers
Models:
Author: Stores the name of the author.
Book: Stores the title, publication year, and links to an author (ForeignKey relationship).
API Endpoints
Book Endpoints
Method	Endpoint	Description	Permissions
GET	/api/books/	List all books	Public
GET	/api/books/<int:pk>/	Retrieve a specific book by ID	Public
POST	/api/books/create/	Create a new book	Authenticated users only
PUT	/api/books/update/<int:pk>/	Update an existing book	Author of the book only
DELETE	/api/books/delete/<int:pk>/	Delete a book	Author of the book only
Author Endpoints
Method	Endpoint	Description	Permissions
GET	/api/authors/	List all authors	Public
GET	/api/authors/<int:pk>/	Retrieve a specific author by ID	Public
View Descriptions
1. BookListView
Endpoint: /api/books/

HTTP Method: GET

Description: This view returns a list of all the books in the system. It uses Django REST Framework’s ListAPIView, which provides built-in functionality for listing records.

Permissions: AllowAny, meaning that this view is open to all users, whether authenticated or not.

View Definition:

python
Copy code
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
2. BookDetailView
Endpoint: /api/books/<int:pk>/

HTTP Method: GET

Description: Retrieves details of a single book by its ID.

Permissions: AllowAny, meaning anyone can view a book’s details.

View Definition:

python
Copy code
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
3. BookCreateView
Endpoint: /api/books/create/

HTTP Method: POST

Description: Allows authenticated users to create a new book.

Permissions: IsAuthenticated, meaning only logged-in users can create a book.

View Definition:

python
Copy code
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
4. BookUpdateView
Endpoint: /api/books/update/<int:pk>/

HTTP Method: PUT

Description: Allows the author of a book to update its details. This view enforces the custom permission IsAuthorOrReadOnly.

Permissions: IsAuthorOrReadOnly, meaning only the author of the book can modify it.

View Definition:

python
Copy code
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthorOrReadOnly]
5. BookDeleteView
Endpoint: /api/books/delete/<int:pk>/

HTTP Method: DELETE

Description: Allows the author of a book to delete it. This view enforces the custom permission IsAuthorOrReadOnly.

Permissions: IsAuthorOrReadOnly, meaning only the author of the book can delete it.

View Definition:

python
Copy code
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthorOrReadOnly]
Permissions Setup
Built-In Permissions
IsAuthenticated: This permission ensures that only authenticated users can create new books. It’s applied to BookCreateView, making sure users are logged in before they can add new content.

AllowAny: Used for views where no authentication is required (e.g., BookListView, BookDetailView). These views allow anyone to access the data, even if they are not logged in.

Custom Permission: IsAuthorOrReadOnly
The custom permission IsAuthorOrReadOnly ensures that only the author of a book can update or delete it. Other users can still view the book, but they can't modify or delete it unless they are the author.
Testing the API

Conclusion
This project demonstrates how to use Django REST Framework to build a fully functional API with generic views, custom permissions, and nested serializers. We’ve also implemented role-based permissions to restrict access to certain actions based on user roles.

