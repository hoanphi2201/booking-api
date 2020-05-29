from typing import Union, Type

from marshmallow import Schema, ValidationError

from main.extensions.exceptions.physical_validation import PhysicalValidationException


def accepts(schema: Schema = None, many=False, has_request_params=False):
    schema = _get_or_create_schema(schema, many=many)

    def decorator(func):
        def inner(*args, **kwargs):
            from flask import request

            if has_request_params:
                try:
                    obj = schema.load(request.args)
                    request.parse_args = obj
                except ValidationError:
                    raise PhysicalValidationException(message='The query param is not valid')

            else:
                try:
                    obj = schema.load(request.get_json())
                    request.parse_obj = obj
                except ValidationError as err:
                    raise PhysicalValidationException(extra=err.messages)

            return func(*args, **kwargs)

        return inner

    return decorator


def _get_or_create_schema(
        schema: Union[Schema, Type[Schema]], many: bool = False
) -> Schema:
    if isinstance(schema, Schema):
        return schema
    return schema(many=many)
