from rest_framework import permissions
# from .models import UserAction, Session


class PartnerPermission(permissions.BasePermission):
    message = 'The user is not partner'

    def has_object_permission(self, request, view, obj):
        if request.methos in permissions.SAFE_METHODS:
            return True
        return obj.is_partner
