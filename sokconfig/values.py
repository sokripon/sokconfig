from typing import Optional, Callable, TypeVar

T = TypeVar("T")


class Value:
    def __init__(
        self,
        default,
        extra_validator: Optional[Callable[[T], bool]] = None,
        mutator: Optional[Callable[[T], T]] = None,
        value_type: Optional[type] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        if value_type is None:
            self._value_type = type(default)
        if not isinstance(default, self._value_type) and default is not None:
            raise TypeError(f"default({default}) must be of type {self._value_type}")
        self._name = name
        self._extra_validator = extra_validator
        self._mutator = mutator
        self._description = description
        self._validate_callable(extra_validator)
        self._validate(default)
        self._value = self._mutate(default)

    @property
    def value(self):
        return self._value

    def _validate(self, value):
        if value is None:
            return
        if not isinstance(value, self._value_type):
            raise TypeError(f"value({value}) must be of type {self._value_type}")
        if self._extra_validator is not None and not self._extra_validator(value):
            raise ValueError(f"extra_validator returned False for value({value})")

    def _validate_callable(self, callable_: Optional[Callable[[T], bool]]):
        if not callable(callable_) and callable_ is not None:
            raise ValueError("callable must be callable")

    def _mutate(self, value: T):
        if self._mutator is not None:
            return self._mutator(value)
        return value

    @value.setter
    def value(self, value):
        self._validate(value)
        self._value = self._mutate(value)

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self._value})"

    @property
    def name(self):
        return self._name


class IntValue(Value):
    def __init__(
        self,
        default: int | None,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        extra_validator: Optional[Callable[[int], bool]] = None,
        mutator: Optional[Callable[[int], int]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self._value_type = int
        self._min_value = min_value
        self._max_value = max_value
        super().__init__(
            name=name,
            default=default,
            extra_validator=extra_validator,
            mutator=mutator,
            value_type=self._value_type,
            description=description,
        )

    def _validate(self, value):
        super()._validate(value)
        if value is None:
            return
        if self._min_value is not None and value < self._min_value:
            raise ValueError(f"Value({value}) must be greater than {self._min_value}")
        if self._max_value is not None and value > self._max_value:
            raise ValueError(f"Value({value}) must be less than {self._max_value}")

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self._value}, min_value={self._min_value}, max_value={self._max_value})"


class FloatValue(Value):
    _value_type = float

    def __init__(
        self,
        default: float | None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        extra_validator: Optional[Callable[[float], bool]] = None,
        mutator: Optional[Callable[[float], float]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self._value_type = float
        self._min_value = min_value
        self._max_value = max_value
        super().__init__(
            name=name,
            default=default,
            extra_validator=extra_validator,
            mutator=mutator,
            value_type=self._value_type,
            description=description,
        )

    def _validate(self, value):
        super()._validate(value)
        if value is None:
            return
        if self._min_value is not None and value < self._min_value:
            raise ValueError(f"Value({value}) must be greater than {self._min_value}")
        if self._max_value is not None and value > self._max_value:
            raise ValueError(f"Value({value}) must be less than {self._max_value}")


class BoolValue(Value):
    _value_type = bool

    def __init__(
        self,
        default: bool | None,
        extra_validator: Optional[Callable[[bool], bool]] = None,
        mutator: Optional[Callable[[bool], bool]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        super().__init__(
            name=name,
            default=default,
            extra_validator=extra_validator,
            mutator=mutator,
            value_type=self._value_type,
            description=description,
        )


class StringValue(Value):
    _value_type = str

    def __init__(
        self,
        default: str | None,
        extra_validator: Optional[Callable[[str], bool]] = None,
        mutator: Optional[Callable[[str], str]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        super().__init__(
            name=name,
            default=default,
            extra_validator=extra_validator,
            mutator=mutator,
            value_type=self._value_type,
            description=description,
        )
