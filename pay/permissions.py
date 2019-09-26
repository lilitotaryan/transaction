from rest_framework import permissions
from authentication.models import Partner
from django.conf import settings
from authentication.errors import PartnerNotFound
from .errors import IncompatibleCurrencies, ForbiddenAction
from authentication.utils import error_handler


class PartnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view):
        if request.methos in permissions.SAFE_METHODS:
            return True
        return Partner.objects.get(partner_id=request.validated_data.get("partner_id"))

    @property
    def message(self):
        return error_handler(PartnerNotFound)


class CheckServiceToken(permissions.BasePermission):

    def has_permission(self, request, view):
        x_api_key = request.META.get('HTTP_X_API_KEY')
        return settings.SERVICE_TOKEN == x_api_key

    @property
    def message(self):
        return error_handler(ForbiddenAction)