from rest_framework.exceptions import APIException


class ErrorFields:
    def __init__(self, field='', message='', default_code="", code=''):
            if message and type(message) is str:
                self.message = message
            if default_code and type(default_code) is str:
                self.default_code = default_code
            if code and type(code) is int:
                self.code = code
            if field and type(field) is str:
                self.field = field

    def serialize(self):
        return dict(
            error_code=self.code,
            error_message=self.message,
            error_detail=self.default_code,
            field=self.field
        )


class PasswordIsNotStrong(ErrorFields):
    pass

class AuthException(Exception):
    massage=""
    code=1
    default_code=""
    fields=[]

    def __init__(self, code=1, message='', default_code="", fields=[]):
            if message and type(message) is str:
                self.message = message
            if default_code and type(default_code) is str:
                self.default_code = default_code
            if code and type(code) is int:
                self.code = code
            if fields and type(fields) is list:
                self.fields = fields

    def serialize(self):
        return dict(
            error_code=self.code,
            error_message=self.message,
            error_detail=self.default_code,
            fields=self.fields
        )


class ValidationError(AuthException):
    def __init__(self, errors):
        for i in errors:
        # Todo add ErrorFields foe each case
            field_error = PasswordIsNotStrong
            self.fields.push(field_error.serialize())



class UserNotFound(AuthException):
    def __init__(self):
        super().__init__(code=2,
                         message='User is not found.',
                         default_code='user_not_found')

# class InvalidInput(AuthException):
#     status_code = 400
#     default_detail = 'Invalid input.'
#     default_code = 'invalid_exists'


# class UserAlreadyExists(AuthException):
#     status_code = 400
#     default_detail = 'User already exists.'
#     default_code = 'user_exists'


class InvalidUsernamePassword(AuthException):
    status_code = 404
    default_detail = 'Invalid username or password.'
    default_code = 'invalid_username_password'


class SessionAlreadyExpired(AuthException):
    status_code = 404
    default_detail = 'Session is already expired'
    default_code = 'session_expired'


class UserLoggedIn(AuthException):
    status_code = 401
    default_detail = 'User is already logged in unauthorized request'
    default_code = 'user_logged_in'


class NoUserLoggedIn(AuthException):
    status_code = 401
    default_detail = 'No user logged in unauthorized request'
    default_code = 'no_user_logged_in'

