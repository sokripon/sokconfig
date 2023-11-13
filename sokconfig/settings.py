from typing import Literal, Any

from sokconfig.values import Value


class Settings:
    @classmethod
    def get_values(cls):
        return {k: v for k, v in vars(cls).items() if isinstance(v, Value)}

    @classmethod
    def fill_empty_names(cls):
        for name, value in cls.get_values().items():
            if value.name is None:
                value._name = name

    @classmethod
    def validate_values(cls):
        for name, value in cls.get_values().items():
            if value.value is None:
                raise ValueError(f"{name}/{value.name} value is None")

    @classmethod
    def set_values(cls, new_values: dict[str, Any]):
        for name, value in new_values.items():
            for key, val in cls.get_values().items():
                if name == val.name:
                    cls.get_values()[key].value = value
                    break
            else:
                raise ValueError(f"{name} is not a valid value name")
