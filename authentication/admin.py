from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Session

@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ['email', 'is_active', "phone_number"]
    exclude = ('last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'date_joined')
    show_change_link = True


@admin.register(Session)
class Session(admin.ModelAdmin):
    list_display = ['token', 'user', 'is_expired']

# class StateAdmin(admin.ModelAdmin):
#     inlines = (CustomUser, )