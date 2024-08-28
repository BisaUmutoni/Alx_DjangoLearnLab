from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUserAdmin
from .models import CustomUser
from .models import Book

admin.site.register(Book)

class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'publication_year')
  search_fields = ('title', 'author')
  list_filter = ('publication_year')

admin.site.register(CustomUser, CustomUserAdmin)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'date_of_birth', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'date_of_birth', 'profile_photo'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)

