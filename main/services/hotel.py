from typing import List, Union, Dict
from main.repositories.hotel import HotelRepository
from main.models import Hotel
from .schemas.hotel import (
    HotelCreate,
    HotelUpdateBy
)
from main.helpers.decorators.accepts_logic import accepts_logic
from main.extensions.exceptions.hotel import HotelNotFoundException

class HotelsService:
    @staticmethod
    def get_by(hotel_id):
        hotel = HotelRepository.get_by(id=hotel_id)
        if hotel is None:
            raise HotelNotFoundException
        return hotel


    @staticmethod
    def create(payload: dict) -> Hotel:
        payload = accepts_logic(payload=payload, schema=HotelCreate)
        hotel = HotelRepository.create(payload)
        return hotel

    @staticmethod
    def get_all_by(query_params: dict, paginate=True) -> Dict[str, Union[int, List[Hotel]]]:
        if not paginate:
            result = HotelRepository.get_all_by_query(**query_params)
            return {
                'total': result.get('total'),
                'hotels': result.get('hotels'),
            }
        result = HotelRepository.paginate_with(**query_params)
        return {
            'total': result.get('total'),
            'hotels': result.get('hotels'),
            'page': result.get('page'),
            'page_size': result.get('page_size')
        }

    @staticmethod
    def get_all_payment_information(hotel_id):
        hotel = HotelRepository.get_by(id=hotel_id)
        if hotel is None:
            raise HotelNotFoundException
        return list(hotel.payment_informations)

    @staticmethod
    def update_by(hotel_id: int, **payload):
        payload = accepts_logic(
            payload=payload,
            temp={
                'hotel_id': hotel_id
            },
            schema=HotelUpdateBy
        )
        HotelRepository.update_by(hotel_id, **payload)

