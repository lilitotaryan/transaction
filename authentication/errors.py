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
    massage = ""
    code = 1
    default_code = ""
    fields = []

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


class UserAlreadyExists(AuthException):
    def __init__(self):
        super().__init__(code=5,
                         message='User with specified email or Pnone Number already exists.',
                         default_code='user_exists')


class DeviceDataNotValid(AuthException):
    def __init__(self):
        super().__init__(code=3,
                         message='Device Data is not Valid.',
                         default_code='device_data_not_valid')


class UserDataNotValid(AuthException):
    def __init__(self):
        super().__init__(code=5,
                         message='User Data is not Valid.',
                         default_code='user_data_not_valid')


class CategoryDataNotValid(AuthException):
    def __init__(self):
        super().__init__(code=8,
                         message='Category data is not valid.',
                         default_code='category_data_not_valid')


class InvalidUsernamePassword(AuthException):
    def __init__(self):
        super().__init__(code=4,
                         message='Invalid Username or Password.',
                         default_code='invalid_username_password')


class SessionAlreadyExpired(AuthException):
    def __init__(self):
        super().__init__(code=6,
                         message='Session is already expired.',
                         default_code='session_expired')


class UserHasNoCategory(AuthException):
    def __init__(self):
        super().__init__(code=7,
                         message='User has no selected categories.',
                         default_code='user_has_no_categories')


class CategoriesNotFound(AuthException):
    def __init__(self):
        super().__init__(code=9,
                         message='No categories found.',
                         default_code='no_categories_found')

class AddressDataNotValid(AuthException):
    def __init__(self):
        super().__init__(code=10,
                         message='Address data is not valid.',
                         default_code='address_data_not_valid')

class UserHasNoAddress(AuthException):
    def __init__(self):
        super().__init__(code=11,
                         message='User has no addred address.',
                         default_code='user_has_no_address')


class CompanyUserShouldHaveName(AuthException):
    def __init__(self):
        super().__init__(code=11,
                         message='CompanyUser should have name specified.',
                         default_code='comapny_user_should_have_name')