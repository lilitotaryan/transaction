from django.contrib import admin
from .models import VivaroUser


@admin.register(VivaroUser)
class UserAdmin(admin.ModelAdmin):
    class FlatPageAdmin(admin.ModelAdmin):
        fieldsets = (
            (None, {
                'fields': (('first_name', 'last_name'), 'username', 'email', 'password', 'phone_number', 'is_user', 'is_partner')
            }),
        ('Permissions',
         {'fields': (
             'is_user',
             'is_partner'
         )}),
        )

