from marshmallow import Schema, validates_schema, post_load, pre_load, ValidationError
from main.helpers.validators.tour import TourValidator
from main.extensions.exceptions.tour import TourNotFoundException

class TourCreate(Schema):
    @validates_schema
    def name(self, payload, **kwargs):
        TourValidator.validate_uniqueness(name=payload.get('name'))


class TourUpdateBy(Schema):
    @validates_schema
    def name(self, payload, **kwargs):
        if payload.get('name'):
            TourValidator.validate_uniqueness_except_current_tour_id(
                tour_id=payload.get('temp').get('tour_id'),
                name=payload.get('name')
            )

    @pre_load()
    def tour_id(self, payload, **kwargs):
        try:
            tour = TourValidator.validate_non_existence(id=payload.get('temp').get('tour_id'))
            payload['temp']['tour'] = tour
        except ValidationError:
            raise TourNotFoundException

        return payload