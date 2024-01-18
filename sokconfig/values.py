from typing import Optional, Callable, TypeVar, Any

T = TypeVar("T")


class Value:
    def __init__(
        self,
        default,
        extra_validator: Optional[Callable[[T], bool]] = None,
        pre_mutator: Optional[Callable[[T], T]] = None,
        post_mutator: Optional[Callable[[T], T]] = None,
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
        self._pre_mutator = pre_mutator
        self._post_mutator = post_mutator
        self._description = description
        self._validate_callable(extra_validator)
        self._validate(default)
        if default is None:
            self._value = default
        else:
            self._value = self._post_mutate(default)

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

    def _pre_mutate(self, value: T):
        if self._pre_mutator is not None:
            return self._pre_mutator(value)
        return value

    def _post_mutate(self, value: T):
        if self._post_mutator is not None:
            return self._post_mutator(value)
        return value

    @value.setter
    def value(self, value):
        value = self._pre_mutate(value)
        self._validate(value)
        self._value = self._post_mutate(value)

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
        pre_mutator: Optional[Callable[[Any], int]] = None,
        post_mutator: Optional[Callable[[int], int]] = None,
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
            pre_mutator=pre_mutator,
            post_mutator=post_mutator,
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
        pre_mutator: Optional[Callable[[Any], float]] = None,
        post_mutator: Optional[Callable[[float], float]] = None,
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
            pre_mutator=pre_mutator,
            post_mutator=post_mutator,
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
        pre_mutator: Optional[Callable[[Any], bool]] = None,
        post_mutator: Optional[Callable[[bool], bool]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        super().__init__(
            name=name,
            default=default,
            extra_validator=extra_validator,
            pre_mutator=pre_mutator,
            post_mutator=post_mutator,
            value_type=self._value_type,
            description=description,
        )


class StringValue(Value):
    _value_type = str

    def __init__(
        self,
        default: str | None,
        extra_validator: Optional[Callable[[str], bool]] = None,
        pre_mutator: Optional[Callable[[Any], str]] = None,
        post_mutator: Optional[Callable[[str], str]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        super().__init__(
            name=name,
            default=default,
            extra_validator=extra_validator,
            pre_mutator=pre_mutator,
            post_mutator=post_mutator,
            value_type=self._value_type,
            description=description,
        )


class ListValue(Value):
    def __init__(
        self,
        default: list | None,
        element_type: type | None = None,
        extra_validator: Optional[Callable[[list], bool]] = None,
        pre_mutator: Optional[Callable[[Any], list]] = None,
        post_mutator: Optional[Callable[[list], list]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self._value_type = list
        self._element_type = element_type
        super().__init__(
            name=name,
            default=default,
            extra_validator=extra_validator,
            pre_mutator=pre_mutator,
            post_mutator=post_mutator,
            value_type=self._value_type,
            description=description,
        )

    def _validate(self, value):
        super()._validate(value)
        if value is None:
            return
        if self._element_type is None:
            return

        if not all(isinstance(element, self._element_type) for element in value):
            raise ValueError(f"All elements in the list must be of type {self._element_type}")

    def append(self, value):
        if self._element_type is not None and not isinstance(value, self._element_type):
            raise ValueError(f"Value({value}) must be of type {self._element_type}")
        self.value.append(value)

    def extend(self, value):
        if self._element_type is not None and not all(isinstance(element, self._element_type) for element in value):
            raise ValueError(f"All elements in the list must be of type {self._element_type}")
        self.value.extend(value)
