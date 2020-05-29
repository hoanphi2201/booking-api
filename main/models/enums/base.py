from enum import Enum


class BaseEnumModel(str, Enum):

    def __str__(self):
        return self.value

    def __new__(cls, value, description=''):
        obj = str.__new__(cls, value)
        obj._value_ = value

        obj.description = description
        return obj

    @classmethod
    def get_extra(cls):
        result = []
        for item in cls:
            result.append({
                'code': item.value,
                'name': item.description
            })
        return result

    @classmethod
    def get_list_of_code(cls):
        result = []
        for item in cls:
            result.append(item.value)
        return result
