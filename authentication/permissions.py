from rest_framework import permissions
from .models import Session
from django.http import HttpResponse
from django.conf import settings
from .errors import UserLoggedIn, NoUserLoggedIn
from .utils import error_handler


class LoggedInPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # Todo error handling
        return request.user.is_anonymous()

    # @property
    # def message(self):
    #     return error_handler(UserLoggedIn)


class SessionExpiredPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # todo check for errors if request.user is AnonymousUser
        try:
            session_token = request.user.session
        except AttributeError:
            session_token = ""
        if session_token:
            try:
                session = Session.objects.get(token=request.user.session)
            except (Session.DoesNotExist, Session.MultipleObjectsReturned):
                # todo error handling
                return False
            return session.is_expired

    @property
    def message(self):
        return error_handler(NoUserLoggedIn)


class ApiTokenPermission(permissions.BasePermission):
    # message = 'Unauthorized'

    def has_permission(self, request, view):
        x_api_key = request.META.get('HTTP_X_API_KEY')
        if x_api_key is not None:
            return settings.API_TOKEN == x_api_key
        # todo error handling
        return False

    # @property
    # def message(self):
    #     return error_handler(ForbiddenAction)
