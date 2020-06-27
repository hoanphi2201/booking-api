from http import HTTPStatus

from ..api_codes import APICode
from ..exceptions import APIException

class TourBookingNotFoundException(APIException):
    code = APICode.TOUR_BOOKING_NOT_FOUND
    http_status = HTTPStatus.NOT_FOUND

    def __init__(self, message=APICode.TOUR_BOOKING_NOT_FOUND.description,
                 extra=None):
        super().__init__(
            code=APICode.TOUR_BOOKING_NOT_FOUND,
            http_status=HTTPStatus.NOT_FOUND,
            message=message,
            extra=extra
        )

    def __str__(self):
        return "tour booking not found"