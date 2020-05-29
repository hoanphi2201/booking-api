# coding=utf-8
from uuid import uuid4

import sqlalchemy as _sa
from sqlalchemy.ext.declarative import declared_attr


class UUIDMixin:
    """
    Adds `id` common columns to a derived
    declarative model.
    """

    # pylint: disable=invalid-name

    @declared_attr
    def id(self):
        return _sa.Column(_sa.CHAR(36), primary_key=True, default=uuid4())
