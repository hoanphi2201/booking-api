from marshmallow import ValidationError

from main.models import Tour
from main.repositories.tour import TourRepository
from main.helpers.validators.validate_error_code import ValidateErrorCode

class TourValidator:
    @staticmethod
    def is_existed(**kwargs) -> Tour:
        tour = TourRepository.get_by(**kwargs)
        return tour

    @staticmethod
    def is_existed_except_by_id(tour_id: int, **kwargs) -> bool:
        tour = TourRepository.get_by(**kwargs)

        if not tour or tour.id == tour_id:
            return False
        return True

    @staticmethod
    def validate_uniqueness(field_name: str = None, **kwargs):
        tour = TourRepository.get_by(**kwargs)

        if tour is not None:
            key, value = next(iter(kwargs.items()))
            field_name = field_name if field_name else key

            raise ValidationError(field_name=field_name, message=ValidateErrorCode.IS_UNIQUE)

        return tour

    @staticmethod
    def validate_non_existence(field_name: str = None, **kwargs):
        tour = TourRepository.get_by(**kwargs)

        if tour is None:
            key, value = next(iter(kwargs.items()))
            field_name = field_name if field_name else key

            raise ValidationError(field_name=field_name, message=ValidateErrorCode.NOT_EXIST)

        return tour

    @staticmethod
    def validate_uniqueness_except_current_tour_id(tour_id: int, field_name: str = None, **kwargs):
        tour = TourRepository.get_by(**kwargs)

        if tour is not None and tour.id != tour_id:
            key, value = next(iter(kwargs.items()))
            field_name = field_name if field_name else key

            raise ValidationError(field_name=field_name, message=ValidateErrorCode.IS_UNIQUE)

        return tour