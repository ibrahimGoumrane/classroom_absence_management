# apps/users/admin.py
from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstName', 'lastName', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'firstName', 'lastName')
    list_filter = ('role', 'is_active', 'is_staff')

admin.site.register(User, UserAdmin)
