from rest_framework import permissions
from .models import UserAction, Session

class AlreadyAuthenticatedPermission(permissions.BasePermission):
    message = 'User is already logged in'

    def has_permission(self, request, view):
            session = Session.objects.get(token=request.data.get("session_token"))
            return session.action.loged_in


class AuthenticatedPermission(permissions.BasePermission):
    message = 'No user is logged in'

    def has_permission(self, request, view):
            session = Session.objects.get(token=request.data.get("session_token"))
            return session.action.loged_out
