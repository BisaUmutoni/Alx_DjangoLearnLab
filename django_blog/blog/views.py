from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'  # Specify the template for the login page

class CustomLogoutView(LogoutView):
    template_name = 'blog/logout.html'
    
    def register(request):
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Registration successful.')
                return redirect('login')
            else:
                messages.error(request, 'Registration failed. Please check the form.')
        else:
            form = CustomUserCreationForm()
            return render(request, 'register.html', {'form': form})
        
    
    def login_view(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
        
    def logout_view(request):
        logout(request)
        return redirect('login')
    
    @login_required
    def profile(request):
        if request.method == 'POST':
            user = request.user
            user.email = request.POST['email']
            user.save()
            messages.success(request, 'Profile updated successfully.')
        return render(request, 'profile.html', {'user': request.user})
