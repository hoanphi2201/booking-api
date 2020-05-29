from typing import Union, Type

from marshmallow import Schema, INCLUDE, ValidationError

from main.extensions.exceptions.logical_validation import LogicalValidationException
from ..utils.camel_key_mapping import GlobalCamelKey


def accepts_logic(payload: dict = {}, temp: dict = {}, schema: Schema = None, many=False):
    schema = _get_or_create_schema(schema, many=many)

    try:
        payload['temp'] = temp
        payload = schema.load(payload, unknown=INCLUDE)
        del payload['temp']
    except ValidationError as err:
        err.messages = _parse_error_to_camel_key(err.messages)
        raise LogicalValidationException(extra=err.messages)

    return payload


def _get_or_create_schema(
        schema: Union[Schema, Type[Schema]], many: bool = False
) -> Schema:
    if isinstance(schema, Schema):
        return schema
    return schema(many=many)


def _parse_error_to_camel_key(err: dict) -> dict:
    parsed_err = {}
    for key, value in err.items():
        if GlobalCamelKey.mapping.get(key):
            parsed_err[GlobalCamelKey.mapping[key]] = value
        else:
            parsed_err[key] = value
            
    return parsed_err
