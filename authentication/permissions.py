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
        if request.user.is_anonymous():
            raise UserNotFound
        return request.user.is_anonymous()

    # @property
    # def message(self):
    #     return error_handler(UserLoggedIn)


class SessionExpiredPermission(permissions.BasePermission):

    @error_handler
    def has_permission(self, request, view):
        try:
            session_token = request.user.session
        except AttributeError:
            raise UserNotFound
        if session_token:
            try:
                session = Session.objects.get(token=request.user.session)
            except (Session.DoesNotExist, Session.MultipleObjectsReturned):
                raise UserNotFound
            if not session.is_unexpired():
                raise SessionAlreadyExpired()
            return session.is_expired

    # @property
    # def message(self):
    #     return error_handler(NoUserLoggedIn)


class ApiTokenPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY')
        if api_key is not None:
            if settings.API_TOKEN == api_key:
                return True
        raise InvalidHeaders



