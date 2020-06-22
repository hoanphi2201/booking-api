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
from main.helpers.utils.string import StringUtils
from main.models.enums import Bank
from .base import (
    BaseRequestSchema,
    BaseResponseSchema
)

class TourCreateRequestSchema(BaseRequestSchema):
    name = String(required=True, validate=[
        ValidateLength(min=1, max=255)
    ])

    is_active = Boolean(data_key='isActive', required=True)

    description = String(required=True, validate=[
        ValidateLength(min=1, max=5000)
    ])

    city_or_province = String(data_key='cityOrProvince', required=True, validate=[
        ValidateLength(min=1, max=10)
    ])

    common_address = String(data_key='commonAddress', required=True, validate=[
        ValidateLength(min=1, max=255)
    ])

    duration = Integer(required=True)
    min_size = Integer(data_key='minSize', required=True)
    max_size = Integer(data_key='maxSize', required=True)
    price_per_participant = Integer(data_key='pricePerParticipant', required=True)
    transportations = String(required=True, validate=[
        ValidateLength(min=1, max=255)
    ])
    images = String(required=True, validate=[
        ValidateLength(min=1, max=500)
    ])
    organizer_name = String(data_key='organizerName', required=True, validate=[
        ValidateLength(min=1, max=255)
    ])
    organizer_phome_number = String(data_key='organizerPhoneNumber', required=True, validate=[
        ValidateLength(min=1, max=255)
    ])
    organizer_email = String(data_key='organizerEmail', required=True, validate=[
        ValidateLength(min=1, max=255)
    ])
    organizer_avatar = String(data_key='organizerAvatar', required=True, validate=[
        ValidateLength(min=1, max=255)
    ])


class TourUpdateRequestSchema(BaseRequestSchema):
    name = String(required=False, validate=[
        ValidateLength(min=1, max=255)
    ])

    is_active = Boolean(data_key='isActive', required=False)

    description = String(required=False, validate=[
        ValidateLength(min=1, max=5000)
    ])

    city_or_province = String(data_key='cityOrProvince', required=False, validate=[
        ValidateLength(min=1, max=10)
    ])

    common_address = String(data_key='commonAddress', required=False, validate=[
        ValidateLength(min=1, max=255)
    ])

    duration = Integer(required=False)
    min_size = Integer(data_key='minSize', required=False)
    max_size = Integer(data_key='maxSize', required=False)
    price_per_participant = Integer(data_key='pricePerParticipant', required=False)
    transportations = String(required=False, validate=[
        ValidateLength(min=1, max=255)
    ])
    images = String(required=False, validate=[
        ValidateLength(min=1, max=500)
    ])
    organizer_name = String(data_key='organizerName', required=False, validate=[
        ValidateLength(min=1, max=255)
    ])
    organizer_phome_number = String(data_key='organizerPhoneNumber', required=False, validate=[
        ValidateLength(min=1, max=255)
    ])
    organizer_email = String(data_key='organizerEmail', required=False, validate=[
        ValidateLength(min=1, max=255)
    ])
    organizer_avatar = String(data_key='organizerAvatar', required=False, validate=[
        ValidateLength(min=1, max=255)
    ])


class ToursGetRequestSchema(Schema):
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


class TourSchema(Schema):
    id = Integer(required=True)
    name = String(required=True)
    is_active = Boolean(data_key='isActive', required=True)
    description = String(required=True)
    city_or_province = String(data_key='cityOrProvince', required=True)
    common_address = String(data_key='commonAddress', required=True)
    duration = Integer(required=True)
    min_size = Integer(data_key='minSize', required=True)
    max_size = Integer(data_key='maxSize', required=True)
    transportations = Method(serialize='get_transportations')
    images = Method(serialize='get_images')
    organizer_name = String(data_key='organizerName', required=True)
    organizer_email = String(data_key='organizerEmail', required=True)
    organizer_phone_number = String(data_key='organizerPhoneNumber', required=True)
    organizer_avatar = String(data_key='organizerAvatar', required=True)

    def get_transportations(self, obj):
        transportations = obj.transportations
        if transportations is not None:
            transportations = transportations.split(',')
        return transportations

    def get_images(self, obj):
        images = obj.images
        if images is not None:
            images = images.split(',')
        return images


class TourResponseSchema(BaseResponseSchema):
    tour = Nested(TourSchema)


class ToursGetResponseSchema(BaseResponseSchema):
    page = Integer(required=True)
    page_size = Integer(data_key='pageSize', required=True, validate=[
        ValidateRange(min=1, max=200)
    ])
    total = Integer(required=True)
    tours = Nested(TourSchema(many=True))


class ToursSearchRequestSchema(BaseRequestSchema):
    city_or_province = String(data_key='cityOrProvince', required=True, validate=[
        ValidateLength(min=1, max=10)
    ])


class ToursSearchResponseSchema(BaseResponseSchema):
    total = Integer(required=True)
    tours = Nested(TourSchema(many=True))


class TourPaymentInformationCreateRequestSchema(BaseRequestSchema):
    bank_code = String(data_key='bankCode', required=True, validate=[
        ValidateEnum(Bank)
    ])

    tour_id = Integer(data_key='tourId', required=True)

    account_number = String(data_key='accountNumber', required=False, validate=[
        ValidateLength(min=1, max=255)
    ])

    account_name = String(data_key='accountName', required=False, validate=[
        ValidateLength(min=1, max=255)
    ])



class TourPaymentInformationSchema(Schema):
    id = Integer()
    bank_code = String(data_key='bankCode')
    account_number = String(data_key='accountNumber')
    account_name = String(data_key='accountName')    


class TourPaymentInformationsResponseSchema(BaseResponseSchema):
    tour_payment_informations = Nested(data_key='tourPaymentInformations', nested=TourPaymentInformationSchema(many=True))
    

class TourWithPaymentSchema(TourSchema):
    tour_payment_informations = Nested(data_key='tourPaymentInformations', nested=TourPaymentInformationSchema(many=True))


class TourResponseWithPaymentSchema(BaseResponseSchema):
    tour = Nested(TourWithPaymentSchema)
