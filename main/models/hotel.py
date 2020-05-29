from main.models import db
from main.models.mixins import TimestampMixin, IDMixin


class Hotel(db.Model, TimestampMixin, IDMixin):
    __tablename__ = 'hotels'

    is_active = db.Column(db.Boolean, default=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    description = db.Column(db.VARCHAR(255), nullable=False)
    city_or_province = db.Column(db.VARCHAR(255), nullable=False)
    address = db.Column(db.VARCHAR(255), nullable=False)
    phone_number = db.Column(db.VARCHAR(255), nullable=False)
    email = db.Column(db.VARCHAR(255), nullable=False)
    room_types = db.Column(db.VARCHAR(255), nullable=False)
    utilities = db.Column(db.VARCHAR(255), nullable=False)
    checkin = db.Column(db.TIME(), nullable=False)
    checkout = db.Column(db.TIME(), nullable=False)
    image = db.Column(db.VARCHAR(255), nullable=False)
    longitude = db.Column(db.FLOAT, nullable=False)
    latitude = db.Column(db.FLOAT, nullable=False)
    price_standard = db.Column(db.INTEGER, nullable=True)
    available_room_standard = db.Column(db.INTEGER, nullable=True)
    tax_standard = db.Column(db.FLOAT, nullable=True)
    image_standard = db.Column(db.VARCHAR(255), nullable=True)
    price_deluxe = db.Column(db.INTEGER, nullable=True)
    available_room_deluxe = db.Column(db.INTEGER, nullable=True)
    tax_deluxe = db.Column(db.FLOAT, nullable=True)
    image_deluxe = db.Column(db.VARCHAR(255), nullable=True)

    payment_informations = db.relationship(
        'PaymentInformation',
        back_populates='hotel'
    )

    hotel_bookings = db.relationship(
        'HotelBooking',
        back_populates='hotel'
    )
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
