from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Book
from .models import Library
from django.db import models
from django.views.generic.detail import DetailView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def LoginView(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page.
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'relationship_app/login.html')

def LogoutView(request):
    logout(request)
    return redirect('login')  

def homeView(request):
    return render(request, 'relationship_app/home.html')


def registerView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# views.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

# Check for Admin role
def admin_check(user):
    return user.is_superuser and user.userprofile.role == 'Admin'
@user_passes_test(admin_check)
def Admin(request):
    return render(request, 'relationship_app/admin_view.html')

# Check for Librarian role
def librarian_check(user):
    return user.userprofile.role == 'Librarian'

@user_passes_test(librarian_check)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


# Check for Member role
def member_check(user):
    return user.userprofile.role == 'Member'
@user_passes_test(member_check)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
