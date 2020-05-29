# coding=utf-8
import sqlalchemy as _sa
from sqlalchemy.ext.declarative import declared_attr


class IDMixin:
    """
    Adds `id` common columns to a derived
    declarative model.
    """

    # pylint: disable=invalid-name

    @declared_attr
    def id(self):
        return _sa.Column(_sa.Integer, primary_key=True, autoincrement=True)