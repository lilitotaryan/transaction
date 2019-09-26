from rest_framework.response import Response


def error_handler(error):
    data = {
            'data': error.default_detail,
            'status': error.status_code
            }
    return Response(**data)