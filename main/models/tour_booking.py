from main.models import db
from main.models.mixins import TimestampMixin, IDMixin
from .enums import BookingStatus, Bank


class TourBooking(db.Model, TimestampMixin, IDMixin):
    __tablename__ = 'tour_bookings'

    status = db.Column(db.Enum(BookingStatus), nullable=False)
    start_date = db.Column(db.DATE(), nullable=False)
    user_id = db.Column(db.VARCHAR(255), nullable=False)
    guests = db.Column(db.INTEGER, nullable=True)
    price_per_participant = db.Column(db.INTEGER, nullable=False)
    guest_name = db.Column(db.VARCHAR(255), nullable=False)
    guest_phone_number = db.Column(db.VARCHAR(255), nullable=False)
    guest_email = db.Column(db.VARCHAR(255), nullable=False)
    note = db.Column(db.VARCHAR(255), nullable=True)
    image_witness = db.Column(db.VARCHAR(255), nullable=True)
    grand_total = db.Column(db.INTEGER, nullable=False)

    tour_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'tours.id',
            name='FK_tours__booking__id',
            ondelete='RESTRICT',
            onupdate='CASCADE'
        )
    )

    tour = db.relationship(
        'Tour',
        back_populates='tour_bookings'
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
