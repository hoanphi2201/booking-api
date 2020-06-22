from typing import List, Union, Dict
from main.repositories.tour_payment_information import TourPaymentInformationRepository
from main.models import TourPaymentInformation
from .schemas.tour_payment_information import (
    TourPaymentInformationCreate
)
from main.helpers.decorators.accepts_logic import accepts_logic

class TourPaymentInformationsService:
    @staticmethod
    def create(payload: dict) -> TourPaymentInformation:
        payload = accepts_logic(payload=payload, schema=TourPaymentInformationCreate)
        result = TourPaymentInformationRepository.create(payload)
        return result

    @staticmethod
    def delete_by(pi_id: int):
        TourPaymentInformationRepository.delete_by(pi_id)