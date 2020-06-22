from typing import List, Union, Dict
from main.repositories.tour import TourRepository
from main.models import Tour
from .schemas.tour import (
    TourCreate,
    TourUpdateBy
)
from main.helpers.decorators.accepts_logic import accepts_logic
from main.extensions.exceptions.tour import TourNotFoundException

class ToursService:
    @staticmethod
    def get_by(tour_id):
        tour = TourRepository.get_by(id=tour_id)
        if tour is None:
            raise TourNotFoundException
        tour.tour_payment_informations = tour.tour_payment_informations
        return tour


    @staticmethod
    def create(payload: dict) -> Tour:
        payload = accepts_logic(payload=payload, schema=TourCreate)
        tour = TourRepository.create(payload)
        return tour

    @staticmethod
    def get_all_by(query_params: dict, paginate=True) -> Dict[str, Union[int, List[Tour]]]:
        if not paginate:
            result = TourRepository.get_all_by_query(**query_params)
            return {
                'total': result.get('total'),
                'tours': result.get('tours'),
            }
        result = TourRepository.paginate_with(**query_params)
        return {
            'total': result.get('total'),
            'tours': result.get('tours'),
            'page': result.get('page'),
            'page_size': result.get('page_size')
        }

    @staticmethod
    def get_all_tour_payment_information(tour_id):
        tour = TourRepository.get_by(id=tour_id)
        if tour is None:
            raise TourNotFoundException
        return list(tour.tour_payment_informations)

    @staticmethod
    def update_by(tour_id: int, **payload):
        payload = accepts_logic(
            payload=payload,
            temp={
                'tour_id': tour_id
            },
            schema=TourUpdateBy
        )
        TourRepository.update_by(tour_id, **payload)

