from marshmallow import Schema, validates_schema, post_load, pre_load, ValidationError
from main.helpers.validators.tour import TourValidator

class TourBookingCreate(Schema):
    @validates_schema
    def tour_id(self, payload, **kwargs):
        tour = TourValidator.validate_non_existence(field_name='tour_id', id=payload.get('tour_id'))
        payload['temp']['tour'] = tour
