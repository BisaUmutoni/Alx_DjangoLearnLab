from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, permission_required
from .models import Book
from .models import Library
from .models import UserProfile

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from .forms import BookForm

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

# # User Authentication Views
# class CustomLoginView(LoginView):
#     template_name = 'relationship_app/login.html'
#     redirect_authenticated_user = True

# class CustomLogoutView(LogoutView):
#     template_name = 'relationship_app/logout.html'

# class HomePageView(TemplateView):
#     template_name = 'relationship_app/home.html'

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


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

# Check for Admin role
def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Check for Librarian role
def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == 'Librarian'
@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


# Check for Member role
def is_member(user):
    return user.is_authenticated and user.userprofile.role == 'Member'
@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
