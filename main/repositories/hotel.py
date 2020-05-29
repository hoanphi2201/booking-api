from typing import List

from sqlalchemy import func, asc, desc, or_

from main.models import db
from main.models import Hotel


class HotelRepository:
    @staticmethod
    def get_by(**kwargs):
        key, value = next(iter(kwargs.items()))
        hotel = Hotel.query.filter(
            func.lower(getattr(Hotel, key)) == str(value).lower()
        ).first()
        return hotel

    @staticmethod
    def create(hotel_params: dict) -> Hotel:
        hotel = Hotel(**hotel_params)
        db.session.add(hotel)
        db.session.commit()

        return hotel

    @staticmethod
    def get_all_by_query(**kwargs):
        query = Hotel.query
        city_or_province = kwargs.get('city_or_province', None)
        if city_or_province is not None:
            query = query.filter(Hotel.city_or_province == city_or_province)
        total = query.count()
        return {
            'total': total,
            'hotels': query.all()
        }


    @staticmethod
    def common_paginate_query(queryset, descending=True, **kwargs):
        query = queryset
        if kwargs.get('query'):
            _like_expr = '%{}%'.format(kwargs.get('query'))

            query = query.filter(
                or_(
                    Hotel.name.ilike(_like_expr),
                )
            )

        city_or_province = kwargs.get('city_or_province', None)
        if city_or_province is not None:
            query = query.filter(Hotel.city_or_province == city_or_province)

        if kwargs.get('is_active') is not None:
            query = query.filter(Hotel.is_active == kwargs.get('is_active'))

        if descending:
            query = query.order_by(desc(Hotel.updated_at))
        else:
            query = query.order_by(asc(Hotel.updated_at))

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
        query = Hotel.query

        temp = HotelRepository.common_paginate_query(query, descending, **kwargs)

        return {
            'total': temp.get('total'),
            'hotels': temp.get('query').all(),
            'page': temp.get('page'),
            'page_size': temp.get('page_size')
        }
