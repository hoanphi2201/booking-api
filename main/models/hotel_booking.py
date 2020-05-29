from main.models import db
from main.models.mixins import TimestampMixin, IDMixin
from .enums import BookingStatus, Bank


class HotelBooking(db.Model, TimestampMixin, IDMixin):
    __tablename__ = 'hotel_bookings'

    status = db.Column(db.Enum(BookingStatus), nullable=False)
    checkin_date = db.Column(db.DATE(), nullable=False)
    checkout_date = db.Column(db.DATE(), nullable=False)
    room_type = db.Column(db.VARCHAR(255), nullable=False)
    note = db.Column(db.VARCHAR(255), nullable=True)
    user_id = db.Column(db.VARCHAR(255), nullable=False)
    rooms = db.Column(db.INTEGER, nullable=True)
    guests = db.Column(db.INTEGER, nullable=True)
    room_price = db.Column(db.INTEGER, nullable=False)
    room_tax = db.Column(db.FLOAT, nullable=False)
    guest_name = db.Column(db.VARCHAR(255), nullable=False)
    guest_phone_number = db.Column(db.VARCHAR(255), nullable=False)
    guest_email = db.Column(db.VARCHAR(255), nullable=True)
    bank_code = db.Column(db.Enum(Bank), nullable=True)
    paided = db.Column(db.INTEGER, nullable=True)
    image_witness = db.Column(db.VARCHAR(255), nullable=True)

    hotel_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'hotels.id',
            name='FK_hotels__booking__id',
            ondelete='RESTRICT',
            onupdate='CASCADE'
        )
    )

    hotel = db.relationship(
        'Hotel',
        back_populates='hotel_bookings'
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
