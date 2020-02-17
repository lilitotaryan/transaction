from rest_framework.exceptions import APIException


class InvalidHeaders(APIException):
    status_code = 400
    default_detail = 'Invalid Headers are Specified.'
    default_code = 'invalid_headers'


class UserNotFound(APIException):
    status_code = 401
    default_detail = 'User is not found.'
    default_code = 'user_not_found'
