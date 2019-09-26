from rest_framework import permissions
from .models import UserAction, Session
from django.http import HttpResponse
from django.conf import settings
from .errors import UserLoggedIn, NoUserLoggedIn
from pay.errors import ForbiddenAction
from .utils import error_handler

class AlreadyAuthenticatedPermission(permissions.BasePermission):

    def has_permission(self, request, view):
            session = Session.objects.get(token=request.data.get("session_token"))
            return session.action.loged_in

    @property
    def message(self):
        return error_handler(UserLoggedIn)

class AuthenticatedPermission(permissions.BasePermission):

    def has_permission(self, request, view):
            session = Session.objects.get(token=request.data.get("session_token"))
            return session.action.loged_out

    @property
    def message(self):
        return error_handler(NoUserLoggedIn)

class CheckApiToken(permissions.BasePermission):
    message = 'Unauthorized'

    def has_permission(self, request, view):
        x_api_key = request.META.get('HTTP_X_API_KEY')
        return settings.API_TOKEN == x_api_key

    @property
    def message(self):
        return error_handler(ForbiddenAction)
