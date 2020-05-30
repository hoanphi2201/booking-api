from marshmallow import ValidationError

from main.models import Hotel
from main.repositories.hotel import HotelRepository
from main.helpers.validators.validate_error_code import ValidateErrorCode

class HotelValidator:
    @staticmethod
    def is_existed(**kwargs) -> Hotel:
        hotel = HotelRepository.get_by(**kwargs)
        return hotel

    @staticmethod
    def is_existed_except_by_id(hotel_id: int, **kwargs) -> bool:
        hotel = HotelRepository.get_by(**kwargs)

        if not hotel or hotel.id == hotel_id:
            return False
        return True

    @staticmethod
    def validate_uniqueness(field_name: str = None, **kwargs):
        hotel = HotelRepository.get_by(**kwargs)

        if hotel is not None:
            key, value = next(iter(kwargs.items()))
            field_name = field_name if field_name else key

            raise ValidationError(field_name=field_name, message=ValidateErrorCode.IS_UNIQUE)

        return hotel

    @staticmethod
    def validate_non_existence(field_name: str = None, **kwargs):
        hotel = HotelRepository.get_by(**kwargs)

        if hotel is None:
            key, value = next(iter(kwargs.items()))
            field_name = field_name if field_name else key

            raise ValidationError(field_name=field_name, message=ValidateErrorCode.NOT_EXIST)

        return hotel

    @staticmethod
    def validate_uniqueness_except_current_hotel_id(hotel_id: int, field_name: str = None, **kwargs):
        hotel = HotelRepository.get_by(**kwargs)

        if hotel is not None and hotel.id != hotel_id:
            key, value = next(iter(kwargs.items()))
            field_name = field_name if field_name else key

            raise ValidationError(field_name=field_name, message=ValidateErrorCode.IS_UNIQUE)

        return hotel