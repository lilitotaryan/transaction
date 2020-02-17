from functools import wraps

from authentication.errors import AuthException
from authentication.utils import response


def error_handler(func):
    @wraps(func)
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AuthException as e:
            return response(errors=[e.serialize()], success=False)
    return inner_function
