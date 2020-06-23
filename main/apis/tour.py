from flask import request
from flask_restplus import Resource, Namespace
from flask_accepts import responds
from main.helpers.decorators import accepts
from main.extensions.api_codes import APICode
from .schemas.tour import (
    TourCreateRequestSchema,
    ToursGetRequestSchema,
    ToursGetResponseSchema,
    ToursSearchRequestSchema,
    ToursSearchResponseSchema,
    TourPaymentInformationsResponseSchema,
    TourUpdateRequestSchema,
    TourResponseWithPaymentSchema
)
from .schemas.base import IdOnlySchema, BaseResponseSchema
from main.services.tour import ToursService
from main.services.payment_information import PaymentInformationsService

api = Namespace('Tours')


@api.route('', methods=['POST', 'GET'])
class Tours(Resource):
    @accepts(schema=TourCreateRequestSchema)
    @responds(schema=IdOnlySchema)
    def post(self):
        params = request.parse_obj
        tour = ToursService.create(params)

        return IdOnlySchema(
            id=tour.id,
            context={
                'code': APICode.CREATE_SUCCESS,
                'message': APICode.CREATE_SUCCESS.description
            }
        )

    @accepts(schema=ToursGetRequestSchema, has_request_params=True)
    @responds(schema=ToursGetResponseSchema)
    def get(self):
        return ToursService.get_all_by(request.parse_args)


@api.route('/<int:tour_id>', methods=['GET', 'PATCH'])
class Tour(Resource):
    @responds(schema=TourResponseWithPaymentSchema)
    def get(self, tour_id):
        return {
            'tour': ToursService.get_by(tour_id=tour_id)
        }

    @accepts(schema=TourUpdateRequestSchema)
    @responds(schema=BaseResponseSchema)
    def patch(self, tour_id):
        payload = request.parse_obj
        ToursService.update_by(tour_id, **payload)

        return BaseResponseSchema(context={
            'code': APICode.UPDATE_SUCCESS,
            'message': APICode.UPDATE_SUCCESS.description
        })


@api.route('/search', methods=['GET'])
class ToursSearch(Resource):
    @accepts(schema=ToursSearchRequestSchema, has_request_params=True)
    @responds(schema=ToursSearchResponseSchema)
    def get(self):
        params = request.parse_args
        return ToursService.get_all_by(request.parse_args, paginate=False)


@api.route('/<int:tour_id>/payment/get-all', methods=['GET'])
class TOurPaymentInformations(Resource):
    @responds(schema=TourPaymentInformationsResponseSchema)
    def get(self, tour_id):
        return {
            'tour_payment_informations': ToursService.get_all_tour_payment_information(tour_id)
        }
