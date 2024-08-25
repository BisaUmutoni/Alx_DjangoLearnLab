# relationship_app/urls.py
from django.urls import path
from . import views
from .views import list_books
from .views import LibraryDetailView
from . views import list_books

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
#from .views import admin_view, librarian_view, member_view

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication URLs
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.registerView, name='register'),
    path('home/', views.homeView, name='home'),
    path('admin/', views.admin_view, name='admin'),
    path('librarian/', views.librarian_view, name='admin'),
    path('member/', views.member_view, name='admin'),
    path('books/add_book/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit_book/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    
]

