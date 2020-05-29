import typing
from datetime import date
from enum import Enum
from typing import Type

from marshmallow import ValidationError
from marshmallow.fields import Nested
from marshmallow.validate import Length, Regexp, Validator, Email, Range

from ..utils.string import StringUtils
from .validate_error_code import ValidateErrorCode


class ValidateLength(Length):
    message_min = ValidateErrorCode.MIN_LENGTH
    message_max = ValidateErrorCode.MAX_LENGTH

    def __call__(self, value):
        length = len(value)

        if self.equal is not None:
            self.min = self.equal
            self.max = self.equal

        if self.min is not None and length < self.min:
            message = self.message_min
            raise ValidationError(self._format_error(value, message))

        if self.max is not None and length > self.max:
            message = self.message_max
            raise ValidationError(self._format_error(value, message))

        return value


class ValidateRange(Range):
    message_min = ValidateErrorCode.MIN_VALUE
    message_max = ValidateErrorCode.MAX_VALUE

    def __call__(self, value) -> typing.Any:
        if self.min is not None and value < self.min:
            message = self.message_min
            raise ValidationError(self._format_error(value, message))

        if self.max is not None and value > self.max:
            message = self.message_max
            raise ValidationError(self._format_error(value, message))

        return value


class ValidateNumbersAndLettersOnly(Regexp):
    default_message = ValidateErrorCode.INVALID_FORMAT
    regex = '^[A-Za-z0-9]*$'

    def __init__(self):
        super().__init__(self.regex)


class ValidateNumbersOnly(Regexp):
    default_message = ValidateErrorCode.INVALID_FORMAT
    regex = '^[0-9]*$'

    def __init__(self):
        super().__init__(self.regex)

    def __call__(self, value) -> typing.Any:
        list_values = StringUtils.string_split_by_comma_to_list(value, str)

        for val in list_values:
            if val == '' or self.regex.match(val) is None:
                raise ValidationError(self._format_error(value))

        return value


class ValidateCodeRegex(Regexp):
    default_message = ValidateErrorCode.INVALID_FORMAT
    regex = '^[A-Za-z0-9_]*$'

    def __init__(self):
        super().__init__(self.regex)

    def __call__(self, value) -> typing.Any:
        if self.regex.match(value) is None:
            raise ValidationError(self._format_error(value))

        return value


class ValidateAcceptableDate(Validator):
    default_message = ValidateErrorCode.INVALID_DATE

    def __call__(self, value):
        if str(value) > str(date.today()) or str(value.year) < '1900':
            raise ValidationError(self.default_message)


class ValidateEnum(Validator):
    default_message = ValidateErrorCode.INVALID_TYPE

    def __init__(self, enum: Type[Enum]):
        self.enum = enum.__dict__

    def __call__(self, value):
        list_values = StringUtils.string_split_by_comma_to_list(value, str)

        for val in list_values:
            if val not in self.enum:
                raise ValidationError(self.default_message)


class ValidateEmail(Email):
    default_message = ValidateErrorCode.INVALID_FORMAT


class ValidateList(Validator):

    def __call__(self, values):
        if not len(values):
            raise ValidationError(ValidateErrorCode.IS_REQUIRED)


class ValidateDuplicateItem(Validator):
    def __call__(self, values):
        if len(values) != len(set(values)):
            raise ValidationError(ValidateErrorCode.DUPLICATE)
