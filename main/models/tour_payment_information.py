from main.models import db
from main.models.mixins import TimestampMixin, IDMixin
from .enums import Bank


class TourPaymentInformation(db.Model, TimestampMixin, IDMixin):
    __tablename__ = 'tour_payment_informations'

    bank_code = db.Column(db.Enum(Bank), nullable=False)
    account_number = db.Column(db.VARCHAR(255), nullable=False)
    account_name = db.Column(db.VARCHAR(255), nullable=False)
    tour_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'tours.id',
            name='FK_tours__id',
            ondelete='RESTRICT',
            onupdate='CASCADE'
        )
    )

    tour = db.relationship(
        'Tour',
        back_populates='tour_payment_informations'
    )
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
