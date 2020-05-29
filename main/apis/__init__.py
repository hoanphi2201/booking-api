from flask_restplus import Api

from .version import api as version_ns
from .hotel import api as hotel_ns

api = Api(title='Seller API', version='0.0.1')

api.add_namespace(version_ns, path="/getversion")
api.add_namespace(hotel_ns, path="/hotels")
