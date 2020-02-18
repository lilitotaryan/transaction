from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class Company(admin.ModelAdmin):
    exclude = ('last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'date_joined')


# @admin.register(EventUser)
# class EventUser(admin.ModelAdmin):
#     exclude = ('last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'is_active', 'date_joined')


