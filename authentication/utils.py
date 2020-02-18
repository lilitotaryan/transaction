from enum import Enum
from datetime import datetime, timezone

from django.http import JsonResponse
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


def response(data="", errors="", success=True):
    return JsonResponse(data={"errors": errors,
                              "OK": success,
                              "data": data})


def send_verification_email(email):
    pass