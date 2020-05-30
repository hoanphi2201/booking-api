from flask import request
from flask_restplus import Resource, Namespace
from flask_accepts import responds
from main.helpers.decorators import accepts
from main.extensions.api_codes import APICode
from .schemas.hotel_booking import (
    HotelBookingCreateRequestSchema,
    HotelBookingWithHotelSchema,
    HotelBookingsGetRequestSchema,
    HotelBookingsGetResponseSchema,
    HotelBookingUpdateRequestSchema
)
from .schemas.base import IdOnlySchema, BaseResponseSchema
from main.services.hotel_booking import HotelBookingService

api = Namespace('Hotel Bookings')


@api.route('/<int:booking_id>', methods=['GET', 'PATCH'])
class HotelBooking(Resource):
    @responds(schema=HotelBookingWithHotelSchema)
    def get(self, booking_id):
        return {
            'hotel_booking': HotelBookingService.get_by(booking_id)
        }

    @accepts(schema=HotelBookingUpdateRequestSchema)
    @responds(schema=BaseResponseSchema)
    def patch(self, booking_id):
        payload = request.parse_obj
        HotelBookingService.update_by(booking_id, **payload)

        return BaseResponseSchema(context={
            'code': APICode.UPDATE_SUCCESS,
            'message': APICode.UPDATE_SUCCESS.description
        })


@api.route('', methods=['POST', 'GET'])
class HotelBookings(Resource):
    @accepts(schema=HotelBookingCreateRequestSchema)
    @responds(schema=IdOnlySchema)
    def post(self):
        params = request.parse_obj
        booking = HotelBookingService.create(params)

        return IdOnlySchema(
            id=booking.id,
            context={
                'code': APICode.CREATE_SUCCESS,
                'message': APICode.CREATE_SUCCESS.description
            }
        )

    @accepts(schema=HotelBookingsGetRequestSchema, has_request_params=True)
    @responds(schema=HotelBookingsGetResponseSchema)
    def get(self):
        return HotelBookingService.get_all_by(request.parse_args)