from typing import List

from sqlalchemy import func, asc, desc, or_
from datetime import datetime

from main.models import db
from main.models import HotelBooking


class HotelBookingRepository:
    @staticmethod
    def get_by(**kwargs):
        key, value = next(iter(kwargs.items()))
        booking = HotelBooking.query.filter(
            func.lower(getattr(HotelBooking, key)) == str(value).lower()
        ).first()
        return booking

    @staticmethod
    def create(hotel_booking_params: dict) -> HotelBooking:
        hotel_booking_params['created_at'] = datetime.now()
        booking = HotelBooking(**hotel_booking_params)
        db.session.add(booking)
        db.session.commit()

        return booking

    @staticmethod
    def common_paginate_query(queryset, descending=True, **kwargs):
        query = queryset
        if kwargs.get('name_or_email'):
            _like_expr = '%{}%'.format(kwargs.get('name_or_email'))

            query = query.filter(
                or_(
                    HotelBooking.guess_name.ilike(_like_expr),
                    HotelBooking.guest_email.ilike(_like_expr)
                )
            )

        for key in ['status']:
            if kwargs.get(key):
                query = query.filter(getattr(HotelBooking, key).in_(kwargs.get(key)))

        if descending:
            query = query.order_by(desc(HotelBooking.updated_at))
        else:
            query = query.order_by(asc(HotelBooking.updated_at))

        total = query.count()

        page = kwargs.get('page', 1)
        page_size = kwargs.get('page_size', 10)

        if page * page_size > total:
            page = int((total - 1) / page_size) + 1

        return {
            'query': query.offset((page - 1) * page_size).limit(page_size),
            'total': total,
            'page': page,
            'page_size': page_size
        }

    @staticmethod
    def paginate_with(descending=True, **kwargs):
        query = HotelBooking.query

        temp = HotelBookingRepository.common_paginate_query(query, descending, **kwargs)

        return {
            'total': temp.get('total'),
            'hotel_bookings': temp.get('query').all(),
            'page': temp.get('page'),
            'page_size': temp.get('page_size')
        }

    @staticmethod
    def update_by(booking_id: int, **payload):
        HotelBooking.query.filter_by(
            id=booking_id
        ).update(
            {**payload}
        )
        db.session.commit()
        return HotelBookingRepository.get_by(id=booking_id)
