from typing import List

from sqlalchemy import func, asc, desc, or_
from datetime import datetime

from main.models import db
from main.models import Tour


class TourRepository:
    @staticmethod
    def get_by(**kwargs):
        key, value = next(iter(kwargs.items()))
        tour = Tour.query.filter(
            func.lower(getattr(Tour, key)) == str(value).lower()
        ).first()
        return tour

    @staticmethod
    def create(tour_params: dict) -> Tour:
        tour_params['created_at'] = datetime.now()
        tour = Tour(**tour_params)
        db.session.add(tour)
        db.session.commit()

        return tour

    @staticmethod
    def get_all_by_query(**kwargs):
        query = Tour.query
        city_or_province = kwargs.get('city_or_province', None)
        if city_or_province is not None:
            query = query.filter(Tour.city_or_province == city_or_province)
        total = query.count()
        return {
            'total': total,
            'tours': query.all()
        }


    @staticmethod
    def common_paginate_query(queryset, descending=True, **kwargs):
        query = queryset
        if kwargs.get('query'):
            _like_expr = '%{}%'.format(kwargs.get('query'))

            query = query.filter(
                or_(
                    Tour.name.ilike(_like_expr),
                )
            )

        city_or_province = kwargs.get('city_or_province', None)
        if city_or_province is not None:
            query = query.filter(Tour.city_or_province == city_or_province)

        if kwargs.get('is_active') is not None:
            query = query.filter(Tour.is_active == kwargs.get('is_active'))

        if descending:
            query = query.order_by(desc(Tour.updated_at))
        else:
            query = query.order_by(asc(Tour.updated_at))

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
        query = Tour.query

        temp = TourRepository.common_paginate_query(query, descending, **kwargs)

        return {
            'total': temp.get('total'),
            'tours': temp.get('query').all(),
            'page': temp.get('page'),
            'page_size': temp.get('page_size')
        }

    @staticmethod
    def update_by(tour_id: int, **payload):
        Tour.query.filter_by(
            id=tour_id
        ).update(
            {**payload}
        )
        db.session.commit()
        return TourRepository.get_by(id=tour_id)

