from marshmallow import Schema, validates_schema, post_load, pre_load, ValidationError
from main.helpers.validators.hotel import HotelValidator

class PaymentInformationCreate(Schema):
    @validates_schema
    def hotel_id(self, payload, **kwargs):
        hotel = HotelValidator.validate_non_existence(field_name='hotel_id', id=payload.get('hotel_id'))
        payload['temp']['hotel'] = hotel
