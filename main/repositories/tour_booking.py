from typing import List

from sqlalchemy import func, asc, desc, or_
from datetime import datetime

from main.models import db
from main.models import TourBooking


class TourBookingRepository:
    @staticmethod
    def get_by(**kwargs):
        key, value = next(iter(kwargs.items()))
        booking = TourBooking.query.filter(
            func.lower(getattr(TourBooking, key)) == str(value).lower()
        ).first()
        return booking

    @staticmethod
    def create(tour_booking_params: dict) -> TourBooking:
        tour_booking_params['created_at'] = datetime.now()
        booking = TourBooking(**tour_booking_params)
        db.session.add(booking)
        db.session.commit()

        return booking

    @staticmethod
    def common_paginate_query(queryset, descending=True, **kwargs):
        query = queryset
        if kwargs.get('query'):
            _like_expr = '%{}%'.format(kwargs.get('query'))

            query = query.filter(
                or_(
                    TourBooking.guest_name.ilike(_like_expr),
                    TourBooking.guest_email.ilike(_like_expr),
                    TourBooking.guest_phone_number.ilike(_like_expr)
                )
            )

        user_id = kwargs.get('user_id')
        if user_id:
            query = query.filter(TourBooking.user_id.ilike(user_id))
        
        for key in ['status']:
            if kwargs.get(key):
                query = query.filter(getattr(TourBooking, key).in_(kwargs.get(key)))

        if descending:
            query = query.order_by(desc(TourBooking.updated_at))
        else:
            query = query.order_by(asc(TourBooking.updated_at))

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
        query = TourBooking.query

        temp = TourBookingRepository.common_paginate_query(query, descending, **kwargs)

        return {
            'total': temp.get('total'),
            'tour_bookings': temp.get('query').all(),
            'page': temp.get('page'),
            'page_size': temp.get('page_size')
        }

    @staticmethod
    def update_by(booking_id: int, **payload):
        TourBooking.query.filter_by(
            id=booking_id
        ).update(
            {**payload}
        )
        db.session.commit()
        return TourBookingRepository.get_by(id=booking_id)
