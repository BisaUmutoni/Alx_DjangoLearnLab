from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView


class CustomLoginView(LoginView):
    template_name = 'blog/login.html'  # Specify the template for the login page

class CustomLogoutView(LogoutView):
    template_name = 'blog/logout.html'

class HomePageView(TemplateView):
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
            # return HttpResponse redirect
    
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


from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post

class ListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

class DetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class CreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class DeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
