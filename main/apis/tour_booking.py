from flask import request
from flask_restplus import Resource, Namespace
from flask_accepts import responds
from main.helpers.decorators import accepts
from main.extensions.api_codes import APICode
from .schemas.tour_booking import (
    TourBookingCreateRequestSchema,
    TourBookingWithTourSchema,
    TourBookingsGetRequestSchema,
    TourBookingsGetResponseSchema,
    TourBookingUpdateRequestSchema
)
from .schemas.base import IdOnlySchema, BaseResponseSchema
from main.services.hotel_booking import HotelBookingService
from main.services.tour_booking import TourBookingService

api = Namespace('Tour Bookings')


@api.route('/<int:booking_id>', methods=['GET', 'PATCH'])
class TourBooking(Resource):
    @responds(schema=TourBookingWithTourSchema)
    def get(self, booking_id):
        return {
            'tour_booking': TourBookingService.get_by(booking_id)
        }

    @accepts(schema=TourBookingUpdateRequestSchema)
    @responds(schema=BaseResponseSchema)
    def patch(self, booking_id):
        payload = request.parse_obj
        TourBookingService.update_by(booking_id, **payload)

        return BaseResponseSchema(context={
            'code': APICode.UPDATE_SUCCESS,
            'message': APICode.UPDATE_SUCCESS.description
        })


@api.route('', methods=['POST', 'GET'])
class TourBookings(Resource):
    @accepts(schema=TourBookingCreateRequestSchema)
    @responds(schema=IdOnlySchema)
    def post(self):
        params = request.parse_obj
        booking = TourBookingService.create(params)

        return IdOnlySchema(
            id=booking.id,
            context={
                'code': APICode.CREATE_SUCCESS,
                'message': APICode.CREATE_SUCCESS.description
            }
        )

    @accepts(schema=TourBookingsGetRequestSchema, has_request_params=True)
    @responds(schema=TourBookingsGetResponseSchema)
    def get(self):
        return TourBookingService.get_all_by(request.parse_args)