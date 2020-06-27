from typing import List, Union, Dict
from main.repositories.tour_booking import TourBookingRepository
from main.models import TourBooking
from .schemas.tour_booking import (
    TourBookingCreate,
)
from main.helpers.decorators.accepts_logic import accepts_logic
from main.extensions.exceptions.tour_booking import TourBookingNotFoundException

class TourBookingService:
    @staticmethod
    def get_by(booking_id: int) -> TourBooking:
        booking = TourBookingRepository.get_by(id=booking_id)
        if booking is None:
            raise TourBookingNotFoundException
        booking.tour = booking.tour
        return booking

    @staticmethod
    def create(payload: dict) -> TourBooking:
        payload = accepts_logic(payload=payload, schema=TourBookingCreate)
        booking = TourBookingRepository.create(payload)
        return booking

    @staticmethod
    def get_all_by(query_params: dict) -> Dict[str, Union[int, List[TourBooking]]]:
        result = TourBookingRepository.paginate_with(**query_params)
        return {
            'total': result.get('total'),
            'tour_bookings': result.get('tour_bookings'),
            'page': result.get('page'),
            'page_size': result.get('page_size')
        }

    @staticmethod
    def update_by(booking_id: int, **payload):
        TourBookingRepository.update_by(booking_id, **payload)
