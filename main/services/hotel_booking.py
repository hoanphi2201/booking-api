from typing import List, Union, Dict
from main.repositories.hotel_booking import HotelBookingRepository
from main.models import HotelBooking
from .schemas.hotel_booking import (
    HotelBookingCreate,
)
from main.helpers.decorators.accepts_logic import accepts_logic
from main.extensions.exceptions.hotel_booking import HotelBookingNotFoundException

class HotelBookingService:
    @staticmethod
    def get_by(booking_id: int) -> HotelBooking:
        booking = HotelBookingRepository.get_by(id=booking_id)
        if booking is None:
            raise HotelBookingNotFoundException
        booking.hotel = booking.hotel
        return booking

    @staticmethod
    def create(payload: dict) -> HotelBooking:
        payload = accepts_logic(payload=payload, schema=HotelBookingCreate)
        booking = HotelBookingRepository.create(payload)
        return booking

    @staticmethod
    def get_all_by(query_params: dict) -> Dict[str, Union[int, List[HotelBooking]]]:
        result = HotelBookingRepository.paginate_with(**query_params)
        return {
            'total': result.get('total'),
            'hotel_bookings': result.get('hotel_bookings'),
            'page': result.get('page'),
            'page_size': result.get('page_size')
        }

    @staticmethod
    def update_by(booking_id: int, **payload):
        HotelBookingRepository.update_by(booking_id, **payload)
