from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Admin, EventUser

@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    pass

# @admin.register(Admin)
# class Admin(admin.ModelAdmin):
#     pass


@admin.register(EventUser)
class EventUser(admin.ModelAdmin):
    exclude = ('last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'is_active', 'date_joined')
