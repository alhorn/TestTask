from django.conf import settings
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


class BaseException(Exception):
    code = "base_tournament_exception"


exceptions = {
    BaseException: status.HTTP_400_BAD_REQUEST,
}


def project_exceptions_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError) and not response:
        response_body = {
            'message': 'There is a conflict between the data you are trying to save and current data. '
                       'Please review your entries and try again.'
        }
        if settings.DEBUG:
            response_body['exc'] = str(exc)
        return Response(response_body, status=status.HTTP_400_BAD_REQUEST)
    if not response:
        if hasattr(exc, 'twotuples'):
            return Response(data={exc_tuple[0]: exc_tuple[1] for exc_tuple in exc.twotuples}, status=exc.status_code)

    for exc_type, status_code in exceptions.items():
        if isinstance(exc, exc_type):
            data = {"detail": str(exc), "status_code": status_code}
            code = getattr(exc, "code", None)
            if code:
                data["code"] = code
            return Response(data=data, status=status_code)

    return response
