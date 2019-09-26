from rest_framework.exceptions import APIException

class UserNotFound(APIException):
    status_code = 404
    default_detail = 'User not found.'
    default_code = 'user_not_found'


class PartnerNotFound(APIException):
    status_code = 404
    default_detail = 'Partner not found.'
    default_code = 'partner_not_found'


class InvalidInput(APIException):
    status_code = 400
    default_detail = 'Invalid input.'
    default_code = 'invalid_exists'


class UserAlreadyExists(APIException):
    status_code = 400
    default_detail = 'User already exists.'
    default_code = 'user_exists'


class InvalidUsernamePassword(APIException):
    status_code = 404
    default_detail = 'Invalid username or password.'
    default_code = 'invalid_username_password'


class SessionAlreadyExpired(APIException):
    status_code = 404
    default_detail = 'Session is already expired'
    default_code = 'session_expired'


class UserLoggedIn(APIException):
    status_code = 401
    default_detail = 'User is already logged in unauthorized request'
    default_code = 'user_logged_in'


class NoUserLoggedIn(APIException):
    status_code = 401
    default_detail = 'No user logged in unauthorized request'
    default_code = 'no_user_logged_in'

