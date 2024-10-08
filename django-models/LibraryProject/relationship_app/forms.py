from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserProfileForm(UserCreationForm):  
    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            # Save profile details
            UserProfile.objects.create(
                user=user,
                password=user.password,
            )
        return user

