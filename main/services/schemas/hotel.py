from marshmallow import Schema, validates_schema, post_load, pre_load, ValidationError
from main.helpers.validators.hotel import HotelValidator
from main.extensions.exceptions.hotel import HotelNotFoundException

class HotelCreate(Schema):
    @validates_schema
    def name(self, payload, **kwargs):
        HotelValidator.validate_uniqueness(name=payload.get('name'))


class HotelUpdateBy(Schema):
    @validates_schema
    def name(self, payload, **kwargs):
        if payload.get('name'):
            HotelValidator.validate_uniqueness_except_current_hotel_id(
                hotel_id=payload.get('temp').get('hotel_id'),
                name=payload.get('name')
            )

    @pre_load()
    def hotel_id(self, payload, **kwargs):
        try:
            hotel = HotelValidator.validate_non_existence(id=payload.get('temp').get('hotel_id'))
            payload['temp']['hotel'] = hotel
        except ValidationError:
            raise HotelNotFoundException

        return payload