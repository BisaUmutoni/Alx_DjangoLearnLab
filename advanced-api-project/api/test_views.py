
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from api.models import Book, Author
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test author and books
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=self.author
        )
        self.book_url = reverse('book-detail', args=[self.book.id])
        self.books_url = reverse('book-list')

    # Add authentication headers
    def authenticate(self):
        self.client.login(username='testuser', password='testpassword')
def test_create_book(self):
    self.authenticate()  # Ensure the user is authenticated
    data = {
        'title': 'New Book',
        'publication_year': 2024,
        'author': self.author.id
    }
    response = self.client.post(self.books_url, data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['title'], 'New Book')

def test_get_book(self):
    response = self.client.get(self.book_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['title'], self.book.title)

def test_update_book(self):
    self.authenticate()
    data = {
        'title': 'Updated Book Title',
        'publication_year': 2023,
        'author': self.author.id
    }
    response = self.client.put(self.book_url, data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['title'], 'Updated Book Title')

def test_delete_book(self):
    self.authenticate()
    response = self.client.delete(self.book_url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

def test_filter_books_by_title(self):
    response = self.client.get(self.books_url, {'title': 'Test Book'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
