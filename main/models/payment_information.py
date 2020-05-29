from main.models import db
from main.models.mixins import TimestampMixin, IDMixin
from .enums import Bank


class PaymentInformation(db.Model, TimestampMixin, IDMixin):
    __tablename__ = 'payment_informations'

    bank_code = db.Column(db.Enum(Bank), nullable=False)
    account_number = db.Column(db.VARCHAR(255), nullable=False)
    account_name = db.Column(db.VARCHAR(255), nullable=False)
    hotel_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'hotels.id',
            name='FK_hotels__id',
            ondelete='RESTRICT',
            onupdate='CASCADE'
        )
    )

    hotel = db.relationship(
        'Hotel',
        back_populates='payment_informations'
    )
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
