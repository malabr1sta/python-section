from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:

    def __init__(self, path: str) -> None:
        self.path = path

    @classmethod
    def get_value(cls, data: JSON, key_list: list) -> Any:
        if not key_list:
            return data
        if not (isinstance(data, dict) and key_list[0] in data):
            return None
        return cls.get_value(data[key_list[0]], key_list[1:])

    @classmethod
    def set_value(cls, data: JSON, key_list: list, value: Any) -> None:
        if not key_list:
            return None
        key = key_list[0]
        if len(key_list) == 1:
            data[key] = value
            return None
        if key not in data or not isinstance(data[key], dict):
            data[key] = {}
        cls.set_value(data[key], key_list[1:], value)

    def __get__(self, instance: Model, owner) -> Any:
        data = instance.payload
        return self.__class__.get_value(data, self.path.split("."))

    def __set__(self, instance, value: Any) -> None:
        data = instance.payload
        return self.__class__.set_value(data, self.path.split("."), value)
