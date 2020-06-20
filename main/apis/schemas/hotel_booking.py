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
from .hotel import HotelSchema

class HotelBookingCreateRequestSchema(BaseRequestSchema):
    hotel_id = Integer(data_key='hotelId', required=True)
    checkin_date = DateTime(data_key='checkinDate', format='%d-%m-%Y', required=True)
    checkout_date = DateTime(data_key='checkoutDate', format='%d-%m-%Y', required=True)
    room_type = String(data_key='roomType', required=True, validate=[
        ValidateLength(min=1, max=10)
    ])
    note = String(validate=[
        ValidateLength(max=255)
    ])
    user_id = String(data_key='userId', required=True, validate=[
        ValidateLength(min=1, max=255)
    ])
    rooms = Integer(required=True)
    guests = Integer(required=True)
    room_price = Integer(data_key='roomPrice', required=True)
    room_tax = Float(data_key='roomTax', required=True)
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
    bank_code = String(data_key='bankCode', allow_none=True)
    painded = Integer(allow_none=True)
    image = String(allow_none=True)

    @post_load()
    def refine_data(self, data, **kwargs):
        data['checkin_date'] = data.get('checkin_date').strftime('%Y-%m-%d')
        data['checkout_date'] = data.get('checkout_date').strftime('%Y-%m-%d')
        data['status'] = 'PENDING_PAYMENT'
        return data


class HotelBookingsGetRequestSchema(Schema):
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


class HotelBookingSchema(Schema):
    id = Integer(required=True)
    status = String(required=True)
    note = String()
    checkin_date = DateTime(data_key='checkinDate', format='%d-%m-%Y', required=True)
    checkout_date = DateTime(data_key='checkoutDate', format='%d-%m-%Y', required=True)
    room_type = String(data_key='roomType', required=True, validate=[
        ValidateLength(min=1, max=10)
    ])
    note = String()
    user_id = String(data_key='userId')
    rooms = Integer()
    guests = Integer()
    room_price = Integer(data_key='roomPrice')
    room_tax = Float(data_key='roomTax')
    grand_total = Integer(data_key='grandTotal')
    guest_name = String(data_key='guestName')
    guest_phone_number = String(data_key='guestPhoneNumber')
    guest_email = String(data_key='guestEmail')
    bank_code = String(data_key='bankCode')
    painded = Integer()
    image_witness = String(data_key='imageWitness')

class HotelBookingWithNestedHotelSchema(HotelBookingSchema):
    hotel = Nested(nested=HotelSchema(many=False))


class HotelBookingWithHotelSchema(HotelBookingSchema):
    hotel_booking = Nested(nested=HotelBookingWithNestedHotelSchema)


class HotelBookingsGetResponseSchema(BaseResponseSchema):
    page = Integer(required=True)
    page_size = Integer(data_key='pageSize', required=True, validate=[
        ValidateRange(min=1, max=200)
    ])
    total = Integer(required=True)
    hotel_bookings = Nested(data_key='hotelBookings', nested=HotelBookingWithNestedHotelSchema(many=True))


class HotelBookingUpdateRequestSchema(BaseRequestSchema):
    status = String(required=False, allow_none=True)
    paided = Integer(required=False, allow_none=True)
    image_witness = String(data_key='imageWitness', required=False, allow_none=True)