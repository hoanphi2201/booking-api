# coding=utf-8
from .base import BaseEnumModel


class BookingStatus(BaseEnumModel):
    PENDING_PAYMENT = 'pending_payment'
    PENDING_CONFIRM = 'pending_confirm'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    DONE = 'done'
