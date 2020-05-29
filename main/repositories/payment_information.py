from typing import List

from sqlalchemy import func, asc, desc, or_
from datetime import datetime

from main.models import db
from main.models import PaymentInformation


class PaymentInformationRepository:
    @staticmethod
    def get_by(**kwargs):
        key, value = next(iter(kwargs.items()))
        payment_infor = PaymentInformation.query.filter(
            func.lower(getattr(PaymentInformation, key)) == str(value).lower()
        ).first()
        return payment_infor

    @staticmethod
    def create(payment_infor_params: dict) -> PaymentInformation:
        payment_infor_params['created_at'] = datetime.now()
        payment_infor = PaymentInformation(**payment_infor_params)
        db.session.add(payment_infor)
        db.session.commit()

        return payment_infor

    @staticmethod
    def delete_by(pi_id: int):
        query = PaymentInformation.query.filter(
            PaymentInformation.id == pi_id,
        )
        pi = query.first()
        query.delete()
        db.session.commit()
        return pi

    @staticmethod
    def update_by(pi_id: int, **payload):
        PaymentInformation.query.filter_by(
            id=pi_id
        ).update(
            {**payload}
        )

        db.session.commit()

        return PaymentInformation.get_by(id=pi_id)

    

