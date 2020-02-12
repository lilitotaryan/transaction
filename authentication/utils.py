from enum import Enum
from datetime import datetime, timezone
from rest_framework.response import Response

class BaseEnum(Enum):
    @classmethod
    def members(cls):
        for i in cls:
            return (i.value, i.name)


class StateEnum(BaseEnum):
    REGISTER = 1
    UNSUCCESSFUL_REGISTER = 2
    FIRST_LOGIN = 3
    LOGIN = 4
    UNSUCCESSFUL_LOGIN = 5
    LOGOUT = 6
    RESET_PASSWORD = 7
    UPDATE_DATA = 8


# TODO CHANGE
def get_current_time():
    return datetime.utcnow()


def error_handler(error):
    data = {
            'data': error.default_detail,
            'status': error.status_code
            }
    return Response(**data)