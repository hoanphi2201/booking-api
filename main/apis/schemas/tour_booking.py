from marshmallow import Schema, post_load, EXCLUDE
from marshmallow.fields import Nested, List, Integer, String, Date, Float, Boolean, DateTime, Method
from main.helpers.validators.validate import (
    ValidateLength,
    ValidateNumbersOnly,
    ValidateList,
    ValidateEmail,
    ValidateRange,
    ValidateEnum,
)
from main.helpers.utils.camel_key_mapping import HotelCamelKey
from main.helpers.utils.string import StringUtils
from main.models.enums import Bank, BookingStatus
from .base import (
    BaseRequestSchema,
    BaseResponseSchema
)
from .tour import TourSchema

class TourBookingCreateRequestSchema(BaseRequestSchema):
    tour_id = Integer(data_key='tourId', required=True)
    start_date = DateTime(data_key='startDate', format='%d-%m-%Y', required=True)
    note = String(validate=[
        ValidateLength(max=255)
    ])
    user_id = String(data_key='userId', required=True, validate=[
        ValidateLength(min=1, max=255)
    ])
    guests = Integer(required=True)
    price_per_participant = Integer(data_key='pricePerParticipant', required=True)
    grand_total = Integer(data_key='grandTotal', required=True)
    guest_name = String(data_key='guestName', required=True, validate=[
        ValidateLength(min=1, max=255)
    ])
    guest_phone_number = String(data_key='guestPhoneNumber', required=True, validate=[
        ValidateLength(min=1, max=255)
    ])
    guest_email = String(data_key='guestEmail', required=True, validate=[
        ValidateLength(min=1, max=255)
    ])

    @post_load()
    def refine_data(self, data, **kwargs):
        data['start_date'] = data.get('start_date').strftime('%Y-%m-%d')
        data['status'] = 'PENDING_PAYMENT'
        return data


class TourBookingsGetRequestSchema(Schema):
    page = Integer(default=1, missing=1, validate=[
        ValidateRange(min=1)
    ])

    page_size = Integer(data_key='pageSize', default=10, missing=10, validate=[
        ValidateRange(min=1, max=200)
    ])

    status = String(validate=[
        ValidateEnum(BookingStatus)
    ])

    query = String()

    user_id = String(data_key='userId')

    @post_load()
    def refine_data(self, data, **kwargs):
        for key, value in data.items():
            if key in ['status']:
                data[key] = StringUtils.string_split_by_comma_to_list(value, str)

        return data


class TourBookingSchema(Schema):
    id = Integer(required=True)
    status = String(required=True)
    note = String()
    start_date = DateTime(data_key='startDate', format='%d-%m-%Y', required=True)
    user_id = String(data_key='userId')
    guests = Integer()
    price_per_participant = Integer(data_key='pricePerParticipant')
    grand_total = Integer(data_key='grandTotal')
    guest_name = String(data_key='guestName')
    guest_phone_number = String(data_key='guestPhoneNumber')
    guest_email = String(data_key='guestEmail')
    image_witness = String(data_key='imageWitness')

class TourBookingWithNestedTourSchema(TourBookingSchema):
    tour = Nested(nested=TourSchema(many=False))


class TourBookingWithTourSchema(TourBookingSchema):
    tour_booking = Nested(nested=TourBookingWithNestedTourSchema)


class TourBookingsGetResponseSchema(BaseResponseSchema):
    page = Integer(required=True)
    page_size = Integer(data_key='pageSize', required=True, validate=[
        ValidateRange(min=1, max=200)
    ])
    total = Integer(required=True)
    tour_bookings = Nested(data_key='tourBookings', nested=TourBookingWithNestedTourSchema(many=True))


class TourBookingUpdateRequestSchema(BaseRequestSchema):
    status = String(required=False, allow_none=True)
    image_witness = String(data_key='imageWitness', required=False, allow_none=True)