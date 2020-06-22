from flask import request
from flask_restplus import Resource, Namespace
from flask_accepts import responds
from main.helpers.decorators import accepts
from main.extensions.api_codes import APICode
from .schemas.tour import (
    TourPaymentInformationCreateRequestSchema,
)
from .schemas.base import (
    BaseResponseSchema,
    IdOnlySchema
)
from main.services.tour_payment_information import TourPaymentInformationsService

api = Namespace('Tour Payment Information')


@api.route('', methods=['POST'])
class TourPaymentInformation(Resource):
    @accepts(schema=TourPaymentInformationCreateRequestSchema)
    @responds(schema=IdOnlySchema)
    def post(self):
        params = request.parse_obj
        pi = TourPaymentInformationsService.create(params)

        return IdOnlySchema(
            id=pi.id,
            context={
                'code': APICode.CREATE_SUCCESS,
                'message': APICode.CREATE_SUCCESS.description
            }
        )


@api.route('/<int:pi_id>', methods=['DELETE'])
class TourPaymentInformationDelete(Resource):
    @responds(schema=BaseResponseSchema)
    def delete(self, pi_id):
        TourPaymentInformationsService.delete_by(pi_id=pi_id)
        return BaseResponseSchema(
            context={
                'code': APICode.DELETE_SUCCESS,
                'message': APICode.DELETE_SUCCESS.description
            }
        )
