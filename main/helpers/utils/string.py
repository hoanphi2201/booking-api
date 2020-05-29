import re
import unicodedata
from typing import Any


class StringUtils:

    @staticmethod
    def trim_data(data: str) -> str:
        return str(data).strip()

    @staticmethod
    def capitalize_first_letter(data: str) -> str:
        return ' '.join([x.replace(x[0], x[0].upper(), 1) if len(x) > 0 else x.upper() for x in str(data).split(' ')])

    @staticmethod
    def upper_case(data: str) -> str:
        return str(data).upper()

    @staticmethod
    def list_to_string_split_by_comma(data: list) -> str:
        return ','.join(map(str, data))

    @staticmethod
    def string_split_by_comma_to_list(data : str, converted_to: Any = int) -> list:
        if data is None:
             data = ''
        return list(map(converted_to, data.split(',')))

    @staticmethod
    def remove_duplicate_space(data: str) -> str:
        return " ".join(data.split())

    @staticmethod
    def no_accent_vietnamese(s):
        s = re.sub(u'Đ', 'D', s)
        s = re.sub(u'đ', 'd', s)
        return unicodedata.normalize('NFKD', str(s)).encode('ASCII', 'ignore').decode('UTF-8')

    @staticmethod
    def list_to_bool_json(l: list, default_l: list) -> dict:
        result = {}
        for key in default_l:
            if key in l:
                result[key] = 1
            else:
                result[key] = 0
        return result

    @staticmethod
    def bool_json_to_list(d: dict) -> list:
        return [key for key, value in d.items() if value]
