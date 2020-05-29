from typing import List, Union, Dict
from main.repositories.hotel import HotelRepository
from main.models import Hotel
from .schemas.hotel import (
    HotelCreate,
)
from main.helpers.decorators.accepts_logic import accepts_logic

class HotelsService:
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
