from rest_framework.exceptions import APIException


class IncompatibleCurrencies(APIException):
    status_code = 406
    default_detail = 'The currency is not compatible with partner account\'s currency.'
    default_code = 'the_incompatible_currencies'


class ForbiddenAction(APIException):
    status_code = 403
    default_detail = 'The action is forbidden.'
    default_code = 'forbidden'
