from http import HTTPStatus

from ..api_codes import APICode
from main.extensions.exceptions import APIException


class PhysicalValidationException(APIException):
    code = APICode.PHYSICAL_VALIDATOR_ERROR
    http_status = HTTPStatus.BAD_REQUEST

    def __init__(self, message=APICode.PHYSICAL_VALIDATOR_ERROR.description,
                 extra=None):
        super().__init__(
            code=APICode.PHYSICAL_VALIDATOR_ERROR,
            http_status=HTTPStatus.BAD_REQUEST,
            message=message,
            extra=extra
        )

    def __str__(self):
        return "physical validation errors"
