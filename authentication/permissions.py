import secrets

from rest_framework import permissions

from api_exceptions import InvalidHeaders, UserNotFound
from authentication.decorators import error_handler
from .models import Session
from django.http import HttpResponse
from django.conf import settings
from .errors import SessionAlreadyExpired


class LoggedInPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise UserNotFound
        if not request.user.is_verified:
            raise UserNotFound
        return True

    # @property
    # def message(self):
    #     return error_handler(UserLoggedIn)


class SessionExpiredPermission(permissions.BasePermission):

    @error_handler
    def has_permission(self, request, view):
        session_token = request.META.get('HTTP_USER_SESSION')
        if session_token:
            try:
                session = Session.objects.get(token=session_token)
            except (Session.DoesNotExist, Session.MultipleObjectsReturned):
                raise UserNotFound
            if not session.is_unexpired():
                raise SessionAlreadyExpired()
            return True
        raise InvalidHeaders


class ApiTokenPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY')
        if api_key is not None:
            if settings.API_TOKEN == api_key:
                return True
        raise InvalidHeaders



