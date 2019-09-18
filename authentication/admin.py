from django.contrib import admin
from .models import VivaroUser

@admin.register(VivaroUser)
class UserAdmin(admin.ModelAdmin):
    exclude = ('is_authenticated',)