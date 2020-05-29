from marshmallow import Schema, validates_schema, post_load, pre_load, ValidationError
from main.helpers.validators.hotel import HotelValidator

class HotelCreate(Schema):
    @validates_schema
    def name(self, payload, **kwargs):
        HotelValidator.validate_uniqueness(name=payload.get('name'))