# coding=utf-8
import json
import re
import random
import string


def get_or_create(session, model, **kwargs):
    """
    Get an instance of sqlalchemy model, or create a new one if not
    existed yet.

    :param session:
    :param model:
    :param kwargs:
    :return:
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model()
        for k, v in kwargs.items():
            setattr(instance, k, v)
        session.add(instance)

        return instance

