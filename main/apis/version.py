import os

from flask_restplus import Namespace, Resource

api = Namespace('Version')


@api.route('', methods=['GET'])
class VersionCheck(Resource):
    def get(self):
        return os.environ.get('IMAGE_TAG', '1234567')
