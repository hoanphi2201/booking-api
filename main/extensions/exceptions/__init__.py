from http import HTTPStatus

from ..api_codes import APICode


class APIException(Exception):
    """"
    Base class for all handled exception on Seller API
    ...
    Attributes
    ----------
    code: APICode
        one of APICode which summarize result of operation
    http_status: HTTPStatus
        one of HTTPStatus which will be
    message: str
        brief message described the error
        can use `APICode.description` as default message
    extra: dict
        extra information related to the error
    """

    code = APICode.DEFAULT
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    message = APICode.DEFAULT.description
    extra = None

    def __init__(self, code=APICode.DEFAULT,
                 http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                 message=APICode.DEFAULT.description, extra=None):
        """
        Parameters
        ----------
        :param code: APICode
            one of APICode which summarize result of operation
        :param http_status: HTTPStatus
            one of HTTPStatus which will be
        :param message: str
            brief message described the error
            can use `APICode.description` as default message
        :param extra: dict
            extra information related to the error
        """
        super().__init__()
        self.code = code
        self.http_status = http_status
        self.message = message
        self.extra = extra
