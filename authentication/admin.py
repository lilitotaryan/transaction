from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Session, Category, Address


@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ['email', 'is_active', "phone_number"]
    exclude = ('last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'date_joined')
    show_change_link = True


@admin.register(Session)
class Session(admin.ModelAdmin):
    list_display = ['token', 'user', 'is_expired']


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Address)
class Address(admin.ModelAdmin):
    list_display = ['hash', 'address1', 'city']