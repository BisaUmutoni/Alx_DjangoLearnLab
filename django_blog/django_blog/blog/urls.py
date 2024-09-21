"""
URL configuration for django_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CustomLoginView, CustomLogoutView, HomePageView
from .views import ListView, DetailView, CreateView, UpdateView, DeleteView
from .views import PostByTagListView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', HomePageView.register, name='register'),
    path('profile/', HomePageView.profile, name='profile'),
    path('', HomePageView.as_view(template_name='blog/home.html'), name='home'),

    path('posts/', ListView.as_view(), name='post_list'),
    path('post/<int:pk>/', DetailView.as_view(), name='post_detail'),
    path('post/new/', CreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', UpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', DeleteView.as_view(), name='post_delete'),

    path('post/<int:pk>/comments/new/', views.CommentCreateView, name='add_comment'),
    path('comment/<int:pk>/update/', views.CommentUpdateView, name='edit_comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView, name='delete_comment'),

    path('search/', views.search_posts, name='search_posts'),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts_by_tag'),

]



from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
{"conversationId":"7ff18161-ceed-4653-9d0d-00faeac9bb01","source":"instruct"}