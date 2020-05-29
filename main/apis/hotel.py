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
    HotelsSearchResponseSchema
)
from .schemas.base import IdOnlySchema
from main.services.hotel import HotelsService

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


@api.route('/search', methods=['GET'])
class HotelsSearch(Resource):
    @accepts(schema=HotelsSearchRequestSchema, has_request_params=True)
    @responds(schema=HotelsSearchResponseSchema)
    def get(self):
        params = request.parse_args
        return HotelsService.get_all_by(request.parse_args, paginate=False)
