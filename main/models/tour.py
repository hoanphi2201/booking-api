from main.models import db
from main.models.mixins import TimestampMixin, IDMixin


class Tour(db.Model, TimestampMixin, IDMixin):
    __tablename__ = 'tours'

    is_active = db.Column(db.Boolean, default=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    description = db.Column(db.VARCHAR(5000), nullable=False)
    city_or_province = db.Column(db.VARCHAR(255), nullable=False)
    common_address = db.Column(db.VARCHAR(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    min_size = db.Column(db.Integer, nullable=False)
    max_size = db.Column(db.Integer, nullable=False)
    price_per_participant = db.Column(db.Integer, nullable=False)
    transportations = db.Column(db.VARCHAR(255), nullable=False)
    images = db.Column(db.VARCHAR(500), nullable=False)
    organizer_name = db.Column(db.VARCHAR(255), nullable=False)
    organizer_email = db.Column(db.VARCHAR(255), nullable=False)
    organizer_phone_number = db.Column(db.VARCHAR(255), nullable=False)
    organizer_avatar = db.Column(db.VARCHAR(255), nullable=False)

    tour_payment_informations = db.relationship(
        'TourPaymentInformation',
        back_populates='tour'
    )

    tour_bookings = db.relationship(
        'TourBooking',
        back_populates='tour'
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
