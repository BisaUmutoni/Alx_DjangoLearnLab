# relationship_app/urls.py
from django.urls import path
from . import views
from .views import list_books, LibraryDetailView
from . views import list_books
from .views import login_view, logout_view, register_view

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('home/', register_view, name='home'),
]