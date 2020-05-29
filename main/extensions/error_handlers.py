from http import HTTPStatus
from werkzeug.exceptions import HTTPException

from .api_codes import APICode
from .exceptions import APIException


def register_error_handler(app):
    # TODO: Log exception and notify engineers
    app.register_error_handler(Exception, application_error_handler)


def application_error_handler(exception):
    if isinstance(exception, APIException):
        return api_error_handler(exception)

    if isinstance(exception, HTTPException):
        return werkzeug_http_error_handler(exception)

    return unknown_error_handler(exception)


def api_error_handler(exception):
    response = {
        "code": exception.code,
        "message": exception.code.description,
    }

    if exception.message is not None:
        response["message"] = exception.message

    if exception.extra is not None:
        response["extra"] = exception.extra

    return response, exception.http_status


def werkzeug_http_error_handler(exception):
    response = {
        "code": APICode.UNHANDLED_ERROR,
        "message": exception.description
    }

    return response, exception.code


def unknown_error_handler(exception):
    response = {
        "code": APICode.UNHANDLED_ERROR,
        "message": APICode.UNHANDLED_ERROR.description,
        "extra": {
            "original_error": str(exception)
        }
    }

    return response, HTTPStatus.INTERNAL_SERVER_ERROR
