from flask import request
from flask_restplus import Resource, Namespace
from flask_accepts import responds
from main.helpers.decorators import accepts
from main.extensions.api_codes import APICode
from .schemas.hotel import (
    HotelCreateRequestSchema,
    HotelsGetRequestSchema,
    HotelsGetResponseSchema,
    HotelsSearchRequestSchema,
    HotelsSearchResponseSchema,
    HotelPaymentInformationsResponseSchema,
    HotelResponseSchema
)
from .schemas.base import IdOnlySchema
from main.services.hotel import HotelsService
from main.services.payment_information import PaymentInformationsService

api = Namespace('Hotels')


@api.route('', methods=['POST', 'GET'])
class Hotels(Resource):
    @accepts(schema=HotelCreateRequestSchema)
    @responds(schema=IdOnlySchema)
    def post(self):
        params = request.parse_obj
        hotel = HotelsService.create(params)

        return IdOnlySchema(
            id=hotel.id,
            context={
                'code': APICode.CREATE_SUCCESS,
                'message': APICode.CREATE_SUCCESS.description
            }
        )

    @accepts(schema=HotelsGetRequestSchema, has_request_params=True)
    @responds(schema=HotelsGetResponseSchema)
    def get(self):
        return HotelsService.get_all_by(request.parse_args)


@api.route('/<int:hotel_id>', methods=['GET'])
class Hotel(Resource):
    @responds(schema=HotelResponseSchema)
    def get(self, hotel_id):
        return {
            'hotel': HotelsService.get_by(hotel_id=hotel_id)
        }


@api.route('/search', methods=['GET'])
class HotelsSearch(Resource):
    @accepts(schema=HotelsSearchRequestSchema, has_request_params=True)
    @responds(schema=HotelsSearchResponseSchema)
    def get(self):
        params = request.parse_args
        return HotelsService.get_all_by(request.parse_args, paginate=False)


@api.route('/<int:hotel_id>/payment/get-all', methods=['GET'])
class HotelPaymentInformations(Resource):
    @responds(schema=HotelPaymentInformationsResponseSchema)
    def get(self, hotel_id):
        return {
            'payment_informations': HotelsService.get_all_payment_information(hotel_id)
        }
