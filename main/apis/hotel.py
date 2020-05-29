from flask import request
from flask_restplus import Resource, Namespace
from flask_accepts import responds
from main.helpers.decorators import accepts
from .schemas.hotel import (
    HotelCreateRequestSchema
)
from .schemas.base import IdOnlySchema

api = Namespace('Hotels')


@api.route('', methods=['POST', 'GET'])
class Hotels(Resource):
    @accepts(schema=HotelCreateRequestSchema)
    @responds(schema=IdOnlySchema)
    def post(self):
        params = request.parse_obj
        print(params);

        return IdOnlySchema(
            id="10",
            context={
                'code': APICode.CREATE_SUCCESS,
                'message': APICode.CREATE_SUCCESS.description
            }
        )