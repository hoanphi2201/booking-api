from marshmallow import Schema, post_load, EXCLUDE
from marshmallow.fields import Nested, List, Integer, String, Date, Float, Boolean, DateTime, Method
from main.helpers.validators.validate import (
    ValidateLength,
    ValidateNumbersOnly,
    ValidateList,
    ValidateEmail,
    ValidateRange,
    ValidateEnum
)
from main.helpers.utils.camel_key_mapping import HotelCamelKey
from main.helpers.utils.string import StringUtils
from main.models.enums import Bank
from .base import (
    BaseRequestSchema,
    BaseResponseSchema
)

class HotelCreateRequestSchema(BaseRequestSchema):
    name = String(required=True, validate=[
        ValidateLength(min=1, max=255)
    ])

    is_active = Boolean(data_key=HotelCamelKey.mapping['is_active'], required=True)

    description = String(required=True, validate=[
        ValidateLength(min=1, max=1000)
    ])

    city_or_province = String(data_key=HotelCamelKey.mapping['city_or_province'], required=True, validate=[
        ValidateLength(min=1, max=10)
    ])

    address = String(required=True, validate=[
        ValidateLength(min=1, max=255)
    ])

    longitude = Float(required=True)

    latitude = Float(required=True)

    checkin = DateTime(format='%H:%M', required=True)

    checkout = DateTime(format='%H:%M', required=True)

    utilities = String(required=True, validate=[
        ValidateLength(min=1, max=255)
    ])

    room_types = String(data_key='room_types', required=True, validate=[
        ValidateLength(min=1, max=255)
    ])

    phone_number = String(data_key=HotelCamelKey.mapping['phone_number'], required=True, validate=[
        ValidateLength(min=1, max=255)
    ])

    email = String(required=True, validate=[
        ValidateLength(min=1, max=255),
        ValidateEmail()
    ])

    image = String(required=True, validate=[
        ValidateLength(min=1, max=255)
    ])

    price_standard = Float(data_key=HotelCamelKey.mapping['price_standard'], allow_none=True)
    available_room_standard = Integer(data_key=HotelCamelKey.mapping['available_room_standard'], allow_none=True)
    tax_standard = Float(data_key=HotelCamelKey.mapping['tax_standard'], allow_none=True)
    image_standard = String(data_key=HotelCamelKey.mapping['image_standard'], validate=[
        ValidateLength(min=1, max=255)
    ], allow_none=True)

    price_deluxe = Float(data_key=HotelCamelKey.mapping['price_deluxe'], allow_none=True)
    available_room_deluxe = Integer(data_key=HotelCamelKey.mapping['available_room_deluxe'], allow_none=True)
    tax_deluxe = Float(data_key=HotelCamelKey.mapping['tax_deluxe'], allow_none=True)
    image_deluxe = String(data_key=HotelCamelKey.mapping['image_deluxe'], validate=[
        ValidateLength(min=1, max=255)
    ], allow_none=True)

    @post_load()
    def refine_data(self, data, **kwargs):
        for field in ['name', 'email', 'phone_number']:
            if field not in data:
                continue
            data[field] = StringUtils.remove_duplicate_space(data[field])
        data['checkin'] = data.get('checkin').strftime('%H:%M:%S')
        data['checkout'] = data.get('checkout').strftime('%H:%M:%S')
        return data


class HotelUpdateRequestSchema(BaseRequestSchema):
    name = String(required=False, validate=[
        ValidateLength(min=1, max=255)
    ])
    is_active = Boolean(data_key=HotelCamelKey.mapping['is_active'], required=False)
    description = String(required=False, validate=[
        ValidateLength(min=1, max=1000)
    ])

    city_or_province = String(data_key=HotelCamelKey.mapping['city_or_province'], required=False, validate=[
        ValidateLength(min=1, max=10)
    ])

    address = String(required=False, validate=[
        ValidateLength(min=1, max=255)
    ])

    longitude = Float(required=False)

    latitude = Float(required=False)

    checkin = DateTime(format='%H:%M', required=False)

    checkout = DateTime(format='%H:%M', required=False)

    utilities = String(required=False, validate=[
        ValidateLength(min=1, max=255)
    ])

    room_types = String(data_key=HotelCamelKey.mapping['room_types'], required=False, validate=[
        ValidateLength(min=1, max=255)
    ])

    phone_number = String(data_key=HotelCamelKey.mapping['phone_number'], required=False, validate=[
        ValidateLength(min=1, max=255)
    ])

    email = String(required=False, validate=[
        ValidateLength(min=1, max=255),
        ValidateEmail()
    ])

    image = String(required=False, validate=[
        ValidateLength(min=1, max=255)
    ])

    price_standard = Float(data_key=HotelCamelKey.mapping['price_standard'], required=False, allow_none=True)
    available_room_standard = Integer(data_key=HotelCamelKey.mapping['available_room_standard'], required=False, allow_none=True)
    tax_standard = Float(data_key=HotelCamelKey.mapping['tax_standard'], required=False, allow_none=True)
    image_standard = String(data_key=HotelCamelKey.mapping['image_standard'], validate=[
        ValidateLength(min=1, max=255)
    ], required=False, allow_none=True)

    price_deluxe = Float(data_key=HotelCamelKey.mapping['price_deluxe'], required=False, allow_none=True)
    available_room_deluxe = Integer(data_key=HotelCamelKey.mapping['available_room_deluxe'], required=False, allow_none=True)
    tax_deluxe = Float(data_key=HotelCamelKey.mapping['tax_deluxe'], required=False, allow_none=True)
    image_deluxe = String(data_key=HotelCamelKey.mapping['image_deluxe'], validate=[
        ValidateLength(min=1, max=255)
    ], required=False, allow_none=True)

    @post_load()
    def refine_data(self, data, **kwargs):
        for field in ['name', 'email', 'phone_number']:
            if field not in data:
                continue
            if data[field]:
                data[field] = StringUtils.remove_duplicate_space(data[field])
        if data.get('checkin'):
            data['checkin'] = data.get('checkin').strftime('%H:%M:%S')
        if data.get('checkin'):
            data['checkout'] = data.get('checkout').strftime('%H:%M:%S')
        return data


class HotelsGetRequestSchema(Schema):
    page = Integer(default=1, missing=1, validate=[
        ValidateRange(min=1)
    ])

    page_size = Integer(data_key='pageSize', default=10, missing=10, validate=[
        ValidateRange(min=1, max=200)
    ])

    is_active = Integer(data_key='isActive', validate=[
        ValidateRange(min=0, max=1)
    ])

    city_or_province = String(data_key='cityOrProvince')

    query = String()


class HotelSchema(Schema):
    id = Integer(required=True)
    name = String(required=True)
    is_active = Boolean(data_key=HotelCamelKey.mapping['is_active'], required=True)
    description = String(required=True)
    city_or_province = String(data_key=HotelCamelKey.mapping['city_or_province'], required=True)
    address = String(required=True)
    longitude = Float(required=True)
    latitude = Float(required=True)
    checkin = DateTime(format='%H:%M', required=True)
    checkout = DateTime(format='%H:%M', required=True)
    utilities = Method(serialize='get_utilities')
    room_types = Method(serialize='get_room_types', data_key=HotelCamelKey.mapping['room_types'])
    phone_number = String(data_key=HotelCamelKey.mapping['phone_number'], required=True)
    email = String(required=True)
    image = String(required=True)
    price_standard = Float(data_key=HotelCamelKey.mapping['price_standard'])
    available_room_standard = Integer(data_key=HotelCamelKey.mapping['available_room_standard'])
    tax_standard = Float(data_key=HotelCamelKey.mapping['tax_standard'])
    image_standard = String(data_key=HotelCamelKey.mapping['image_standard'])
    price_deluxe = Float(data_key=HotelCamelKey.mapping['price_deluxe'])
    available_room_deluxe = Integer(data_key=HotelCamelKey.mapping['available_room_deluxe'], allow_none=True)
    tax_deluxe = Float(data_key=HotelCamelKey.mapping['tax_deluxe'])
    image_deluxe = String(data_key=HotelCamelKey.mapping['image_deluxe'])

    def get_utilities(self, obj):
        utilities = obj.utilities
        if utilities is not None:
            utilities = utilities.split(',')
        return utilities

    def get_room_types(self, obj):
        room_types = obj.room_types
        if room_types is not None:
            room_types = room_types.split(',')
        return room_types


class HotelResponseSchema(BaseResponseSchema):
    hotel = Nested(HotelSchema)


class HotelsGetResponseSchema(BaseResponseSchema):
    page = Integer(required=True)
    page_size = Integer(data_key='pageSize', required=True, validate=[
        ValidateRange(min=1, max=200)
    ])
    total = Integer(required=True)
    hotels = Nested(HotelSchema(many=True))


class HotelsSearchRequestSchema(BaseRequestSchema):
    city_or_province = String(data_key=HotelCamelKey.mapping['city_or_province'], required=True, validate=[
        ValidateLength(min=1, max=10)
    ])


class HotelsSearchResponseSchema(BaseResponseSchema):
    total = Integer(required=True)
    hotels = Nested(HotelSchema(many=True))


class HotelPaymentInformationCreateRequestSchema(BaseRequestSchema):
    bank_code = String(data_key=HotelCamelKey.mapping['bank_code'], required=True, validate=[
        ValidateEnum(Bank)
    ])

    hotel_id = Integer(data_key=HotelCamelKey.mapping['hotel_id'], required=True)

    account_number = String(data_key=HotelCamelKey.mapping['account_number'], required=False, validate=[
        ValidateLength(min=1, max=255)
    ])

    account_name = String(data_key=HotelCamelKey.mapping['account_name'], required=False, validate=[
        ValidateLength(min=1, max=255)
    ])



class HotelPaymentInformationSchema(Schema):
    id = Integer()
    bank_code = String(data_key=HotelCamelKey.mapping['bank_code'])
    account_number = String(data_key=HotelCamelKey.mapping['account_number'])
    account_name = String(data_key=HotelCamelKey.mapping['account_name'])    


class HotelPaymentInformationsResponseSchema(BaseResponseSchema):
    payment_informations = Nested(data_key='paymentInformations', nested=HotelPaymentInformationSchema(many=True))