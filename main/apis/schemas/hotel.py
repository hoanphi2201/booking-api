from marshmallow import Schema, post_load, EXCLUDE
from marshmallow.fields import Nested, List, Integer, String, Date, Float
from main.helpers.validators.validate import (
    ValidateLength,
    ValidateNumbersOnly,
    ValidateList,
    ValidateEmail
)
from main.helpers.utils.camel_key_mapping import HotelCamelKey
from main.helpers.utils.string import StringUtils
from .base import BaseRequestSchema

class HotelCreateRequestSchema(BaseRequestSchema):
    name = String(required=True, validate=[
        ValidateLength(min=1, max=255)
    ])

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

    check_in = Date(format='%H:%M', data_key=HotelCamelKey.mapping['check_in'], required=True)

    check_out = Date(format='%H:%M', data_key=HotelCamelKey.mapping['check_out'], required=True)

    utilities = List(String(), required=True, validate=[
        ValidateList()
    ])

    roomTypes = List(String(), required=True, validate=[
        ValidateList()
    ])

    phone_number = String(data_key=HotelCamelKey.mapping['phone_number'], required=True, validate=[
        ValidateLength(min=1, max=255)
    ])

    email = String(validate=[
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
        return data