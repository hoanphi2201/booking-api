from flask_restplus import Api

from .version import api as version_ns
from .hotel import api as hotel_ns
from .payment_information import api as payment_information_ns
from .hotel_booking import api as hotel_booking_ns
from .tour import api as tour_ns
from .tour_payment_information import api as tour_payment_information_ns

api = Api(title='Booking API', version='0.0.1')

api.add_namespace(version_ns, path="/getversion")
api.add_namespace(hotel_ns, path="/hotels")
api.add_namespace(payment_information_ns, path="/payment-informations")
api.add_namespace(hotel_booking_ns, path="/hotel-bookings")
api.add_namespace(tour_ns, path="/tours")
api.add_namespace(tour_payment_information_ns, path="/tour-payment-informations")
