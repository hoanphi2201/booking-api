from typing import List, Union, Dict
from main.repositories.payment_information import PaymentInformationRepository
from main.models import PaymentInformation
from .schemas.payment_information import (
    PaymentInformationCreate
)
from main.helpers.decorators.accepts_logic import accepts_logic

class PaymentInformationsService:
    @staticmethod
    def create(payload: dict) -> PaymentInformation:
        payload = accepts_logic(payload=payload, schema=PaymentInformationCreate)
        print(payload)
        result = PaymentInformationRepository.create(payload)
        return result

    @staticmethod
    def delete_by(pi_id: int):
        PaymentInformationRepository.delete_by(pi_id)